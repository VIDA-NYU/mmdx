<script lang="ts">
  let rand = -1;
  function getRand() {
    fetch("./api/rand")
      .then((d) => d.json())
      .then((d) => (rand = d["number"]));
  }
</script>

<main>
  <h1>Your random number is {rand}!</h1>
  <button on:click={getRand}>Get a number</button>
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    font-size: 4em;
    font-weight: 100;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
