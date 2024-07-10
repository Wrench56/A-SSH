<script lang="ts">
  import { onMount } from "svelte";
  import { AnsiUp } from "ansi_up";

  const ansiUp = new AnsiUp();

  let socket: WebSocket;
  let terminal: HTMLElement;

  onMount(() => async () => {
    /* Initialize WebSocket connection */
    socket = new WebSocket(
      `ws://${window.location.host}/plugins/wsapi/A_SSH/ssh`
    );

    socket.onmessage = function (event: MessageEvent) {
      terminal.innerHTML += ansiUp.ansi_to_html(event.data);
    };

    /* Cleanup WebSocket on component destruction */
    return () => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
    };
  });

  function onKeyDown(e: KeyboardEvent) {
    if (socket == undefined) {
      return;
    }

    socket.send(e.key);
  }
</script>

<svelte:window on:keydown|preventDefault={onKeyDown} />

<main>
  <pre bind:this={terminal} id="terminal"></pre>
</main>

<style>
  main {
    height: 90vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  #terminal {
    width: 100%;
    height: 100%;
    border: 1px solid whitesmoke;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
  }
</style>
