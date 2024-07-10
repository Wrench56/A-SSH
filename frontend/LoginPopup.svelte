<script lang="ts">
  export let socket: WebSocket;
  export let onClose: CallableFunction;

  let user_loc: string = "";
  let password: string = "";

  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === "Enter") {
      socket.send(
        JSON.stringify({
          user_and_location: user_loc,
          password: password,
        })
      );
      onClose();
    }
  }
</script>

<div class="popup-container">
  <div class="popup-content">
    <h3>Login to SSH</h3>
    <input
      type="text"
      placeholder="Enter username@host[:port | 22]"
      bind:value={user_loc}
      on:keypress={handleKeyPress}
    />
    <input
      type="password"
      placeholder="Enter password"
      bind:value={password}
      on:keypress={handleKeyPress}
    />
  </div>
</div>

<style>
  .popup-container {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    z-index: 1000;
  }

  .popup-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  h3 {
    margin-bottom: 10px;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
  }

  input {
    width: 300px;
    margin-bottom: 10px;
    padding: 8px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    font-family: monaco, Consolas, "Lucida Console", monospace;
    color: whitesmoke;
    background-color: #1e1e1e;
  }

  input:focus {
    outline: none;
    border-color: #007bff;
  }
</style>
