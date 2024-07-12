<script lang="ts">
  import { onMount } from "svelte";
  import LoginPopup from "./LoginPopup.svelte";
  import {
    type FitAddon,
    type ITerminalOptions,
    type ITerminalInitOnlyOptions,
    type Terminal,
    XtermAddon,
    Xterm,
  } from "@battlefieldduck/xterm-svelte";

  let socket: WebSocket;
  let enabled: boolean = false;
  let container: HTMLDivElement;
  let terminal: Terminal;
  let fitAddon: FitAddon;

  let options: ITerminalOptions & ITerminalInitOnlyOptions = {
    fontFamily: "FiraCodeNerdFont",
    fontSize: 15,
    customGlyphs: false,
  };

  function calculateRows() {
    const dummy = document.createElement("div");
    dummy.textContent = "M";

    const computedStyle = getComputedStyle(container);
    dummy.style.fontFamily = computedStyle.fontFamily;
    dummy.style.fontSize = computedStyle.fontSize;
    dummy.style.position = "absolute";

    document.body.appendChild(dummy);
    const rowHeight = dummy.offsetHeight;
    document.body.removeChild(dummy);

    return Math.floor(window.innerHeight / rowHeight) - 2;
  }

  async function onLoad(event: CustomEvent<{ terminal: Terminal }>) {
    terminal = event.detail.terminal;

    /* FitAddon Usage */
    fitAddon = new (await XtermAddon.FitAddon()).FitAddon();
    const webLinksAddon = new (
      await XtermAddon.WebLinksAddon()
    ).WebLinksAddon();
    terminal.loadAddon(fitAddon);
    terminal.loadAddon(webLinksAddon);
    terminal.write("\rLoading A-SSH...\r\n");
    terminal.write("Waiting for login\r\n");
    terminal.onResize(({ cols, rows }) => {
      if (!enabled) {
        return;
      }

      if (socket !== undefined && socket.OPEN) {
        socket.send(JSON.stringify({ type: "RESIZE", cols: cols, rows: rows }));
      }
    });

    terminal.resize(terminal.cols, calculateRows());
    fitAddon.fit();
  }

  function onKey(event: CustomEvent<{ key: string; domEvent: KeyboardEvent }>) {
    if (!enabled) {
      return;
    }

    socket.send(JSON.stringify({ type: "KEY", key: event.detail.key }));
  }

  onMount(() => {
    /* Initialize WebSocket connection */
    socket = new WebSocket(
      `ws://${window.location.host}/plugins/wsapi/A_SSH/ssh`
    );

    /* Incoming data from SSH */
    socket.onmessage = function (event: MessageEvent) {
      if (!enabled) {
        return;
      }

      terminal.write(event.data);
      terminal.scrollToBottom();
    };

    /* Resize terminal */
    window.addEventListener("resize", () => {
      terminal.resize(terminal.cols, calculateRows());
      fitAddon.fit();
    });

    /* Cleanup WebSocket on component destruction */
    return () => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
    };
  });
</script>

{#if !enabled}
  <LoginPopup
    {socket}
    onClose={() => {
      enabled = true;
      socket.send(
        JSON.stringify({
          type: "RESIZE",
          cols: terminal.cols,
          rows: terminal.rows,
        })
      );
    }}
  />
{/if}

<div bind:this={container} id="terminal-container">
  <Xterm {options} on:load={onLoad} on:key={onKey} />
</div>

<style>
  @font-face {
    font-family: "FiraCodeNerdFont";
    src: url("/plugins/api/A_SSH/nerdfont") format("truetype");
    font-weight: normal;
    font-style: normal;
  }

  #terminal-container {
    display: block;
    width: calc(100% - 1px);
    margin: 0 auto;
    padding: 2px;
    height: calc(100% - 1px);
    font-family: "FiraCodeNerdFont";
    font-size: 15px;
  }
</style>
