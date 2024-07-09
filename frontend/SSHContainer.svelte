<script lang="ts">
  import { onMount } from "svelte";
  import { Terminal } from "xterm";
  import { FitAddon } from "xterm-addon-fit";

  let socket: WebSocket;
  let terminal: Terminal;
  let terminalContainer: HTMLElement;

  onMount(() => {
    /* Initialize xterm.js terminal */
    terminal = new Terminal();
    const fitAddon = new FitAddon();
    terminal.loadAddon(fitAddon);
    terminal.open(terminalContainer);
    fitAddon.fit();

    /* Initialize WebSocket connection */
    socket = new WebSocket(
      `ws://${window.location.host}/plugins/api/A_SSH/ssh/`
    );

    socket.onmessage = function (event: MessageEvent) {
      terminal.write(event.data + "\r\n");
    };

    /* Cleanup WebSocket and xterm.js on component destruction */
    return () => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
      terminal.dispose();
    };
  });

  function sendMessage() {
    const message = { text: "echo \"Hello from client!\"" };
    socket.send(JSON.stringify(message));
  }
</script>

<main>
  <h1>SSH Terminal</h1>

  <div bind:this={terminalContainer} id="terminal-container"></div>
</main>

<style>
  main {
    height: 90vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  #terminal-container {
    width: 100%;
    height: 100%;
    border: 1px solid #ccc;
  }
</style>
