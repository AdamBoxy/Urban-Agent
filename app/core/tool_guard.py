import concurrent.futures
from functools import wraps
from typing import Callable, Any, Dict, List

AGENCY_TOOL_ALLOWLIST: Dict[str, List[str]] = {
    "family_services": ["verify_case_status"],
    "water_utility": ["check_main_pressure"],
    "orchestrator": ["route_to_subagent", "log_audit_trail", "request_agency_approval"]
}

class ToolGuard:
    def __init__(self, timeout_seconds: int = 5, max_failures: int = 2):
        self.timeout_seconds = timeout_seconds
        self.max_failures = max_failures
        self.tool_failure_counts: Dict[str, int] = {}
        
    def validate_allowlist(self, agency_id: str, tool_name: str) -> bool:
        allowed_tools = AGENCY_TOOL_ALLOWLIST.get(agency_id, [])
        return tool_name in allowed_tools

    def _execute_with_timeout(self, func: Callable, *args, **kwargs) -> Any:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=self.timeout_seconds)
            except concurrent.futures.TimeoutError:
                return f"TOOL_ERROR: Execution timed out after {self.timeout_seconds} seconds."
            except Exception as e:
                raise e

    def safe_execute(self, agency_id: str, tool_name: str, func: Callable, *args, **kwargs) -> Any:
        if not self.validate_allowlist(agency_id, tool_name):
            return f"SECURITY_ERROR: Tool '{tool_name}' is not authorized for agency '{agency_id}'."
        failure_count = self.tool_failure_counts.get(tool_name, 0)
        if failure_count >= self.max_failures:
            return f"CIRCUIT_BREAKER: Tool '{tool_name}' has failed {failure_count} times and is now blocked."
        try:
            result = self._execute_with_timeout(func, *args, **kwargs)
            if isinstance(result, str) and result.startswith("TOOL_ERROR: Execution timed out"):
                self.tool_failure_counts[tool_name] = failure_count + 1
            return result
        except Exception as e:
            self.tool_failure_counts[tool_name] = failure_count + 1
            return f"TOOL_ERROR: An unexpected error occurred: {str(e)}"
            
    def decorator(self, agency_id: str):
        def wrapper_decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return self.safe_execute(agency_id, func.__name__, func, *args, **kwargs)
            return wrapper
        return wrapper_decorator
