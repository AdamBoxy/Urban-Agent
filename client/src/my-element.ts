// @ts-nocheck
import { LitElement, html, css } from 'lit';
import { customElement, query } from 'lit/decorators.js';
import { MessageProcessor } from '@a2ui/web_core/v0_9';
import { A2uiSurface, basicCatalog } from '@a2ui/lit/v0_9';

@customElement('app-root')
export class AppRoot extends LitElement {
  static styles = css`
    :host {
      display: block;
      width: 100vw;
      height: 100vh;
      font-family: sans-serif;
    }
    
    a2ui-surface {
      display: block;
      width: 100%;
      height: 100%;
    }
  `;

  @query('a2ui-surface')
  surface!: any;

  private processor!: MessageProcessor;

  firstUpdated() {
    this.processor = new MessageProcessor({
      catalog: basicCatalog,
      surface: this.surface
    });

    this.connectToBackend();
  }

  private async connectToBackend() {
    try {
      const response = await fetch('http://localhost:8080/v1/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: "initialize_ui" })
      });

      if (!response.body) throw new Error("No response body");
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        
        try {
          const payload = JSON.parse(chunk);
          this.processor.processMessage(payload);
        } catch (e) {
          console.error("Failed to parse A2A JSON payload:", chunk);
        }
      }
    } catch (error) {
      console.error('Connection to backend failed:', error);
    }
  }

  render() {
    return html`<a2ui-surface></a2ui-surface>`;
  }
}
