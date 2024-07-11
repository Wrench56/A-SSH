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

      let ansi_text = sanitizeData(event.data);
      terminal.innerHTML += ansiUp.ansi_to_html(ansi_text);
      terminal.scroll({ top: terminal.scrollHeight, behavior: "smooth" });
    };

    /* Cleanup WebSocket on component destruction */
    return () => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
    };
  });

  function handleKeyPress(event: KeyboardEvent) {
    if (event.key == "Enter" || event.key.length == 1) {
      socket.send(event.key);
    }
  }

  function sanitizeData(text: string): string {
    const ansiEscapeRegex = /\x1b\[80C/g;
    console.log(ansiEscapeRegex.test(text));
    let output = "";
    for (let char of text) {
      if (char === "\x00") {
        /* NULL character */
        continue;
      } else if (char === "\x07") {
        /* BEL character */
        continue;
      } else if (char === "\b") {
        /* Simulate backspace behavior */
        output = output.slice(0, -1);
        terminal.removeChild(terminal.lastElementChild);
      } else {
        output += char;
      }
    }

    return output;
  }

  function getCharWidth() {
    // Create a temporary element to measure the width of a single character
    const tempSpan = document.createElement("span");
    tempSpan.style.fontFamily = "monospace";
    tempSpan.style.visibility = "hidden";
    tempSpan.style.whiteSpace = "nowrap";
    tempSpan.textContent = "M"; // Using "M" as a reference character
    document.body.appendChild(tempSpan);
    const charWidth = tempSpan.offsetWidth;
    document.body.removeChild(tempSpan);
    return charWidth;
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
  @font-face {
    font-family: "FiraCodeNerdFont";
    src: url("/plugins/api/A_SSH/nerdfont") format("truetype");
    font-weight: normal;
    font-style: normal;
  }

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
    font-family: "FiraCodeNerdFont", monaco, Consolas, "Lucida Console",
      monospace;
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
