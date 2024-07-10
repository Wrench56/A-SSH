<script lang="ts">
  import { onMount } from "svelte";
  import { AnsiUp } from "ansi_up";
  import LoginPopup from "./LoginPopup.svelte";

  const ansiUp = new AnsiUp();

  let socket: WebSocket;
  let terminal: HTMLElement;
  let commandInput: HTMLInputElement;
  let enabled: boolean = false;

  onMount(() => {
    /* Initialize WebSocket connection */
    socket = new WebSocket(
      `ws://${window.location.host}/plugins/wsapi/A_SSH/ssh`
    );

    socket.onmessage = function (event: MessageEvent) {
      if (!enabled) {
        return;
      }
      terminal.innerHTML += ansiUp.ansi_to_html(event.data);
    };

    /* Cleanup WebSocket on component destruction */
    return () => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
    };
  });

  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === "Enter") {
      const command = commandInput.value.trim();
      if (command !== "") {
        socket.send(command);
        /* Clean the input field */
        commandInput.value = "";
      }
    }
  }
</script>

{#if !enabled}
  <LoginPopup {socket} onClose={() => (enabled = true)} />
{/if}
<main>
  <pre bind:this={terminal} id="terminal"></pre>
  <input
    type="text"
    disabled={!enabled}
    bind:this={commandInput}
    placeholder="Enter command"
    on:keypress={handleKeyPress}
  />
</main>

<style>
  main {
    height: 90vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  #terminal {
    width: 90%;
    height: 80%;
    overflow-y: auto;
    border: 1px solid whitesmoke;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
    padding: 10px;
    background-color: #1e1e1e;
  }

  input {
    width: 90%;
    padding: 8px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #f2f2f2;
    color: #333;
    box-sizing: border-box;
  }

  input:focus {
    outline: none;
    border-color: #007bff;
  }
</style>
