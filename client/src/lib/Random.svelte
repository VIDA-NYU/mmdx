<script lang="ts">
  import { onMount } from "svelte";
  import type { Hits } from "./Api";
  import { random } from "./Api";
  import ImageCard from "./ImageCard.svelte";

  let result: Promise<Hits> | null = null;
  let limit: string = "16";

  function onQuerySubmit() {
    result = random(+limit);
  }

  onMount(() => {
    onQuerySubmit();
  });
</script>

<div class="container">
  <div class="py-4">
    <div class="row gy-2 gx-2 align-items-center">
      <div class="col-auto me-2">
        <button class="btn btn-primary" on:click={onQuerySubmit}>
          <i class="fa fa-random" aria-hidden="true" />
          Load new samples
        </button>
      </div>
      <div class="col-auto">
        <label class="col-form-label" for="limitSelect">
          Number of results:
        </label>
      </div>
      <div class="col-auto">
        <select
          class="form-select form-select-sm"
          id="limitSelect"
          bind:value={limit}
          on:change={onQuerySubmit}
        >
          <option value="4">4</option>
          <option value="8">8</option>
          <option value="16">16</option>
          <option value="32">32</option>
          <option value="64">64</option>
        </select>
      </div>
      {#await result}
        <div class="col-auto">
          <span>
            <i class="fa fa-spinner fa-spin" aria-hidden="true" />
            Loading...
          </span>
        </div>
      {:then result}
        {#if result}
          <div class="col-auto">
            <span class="form-text">
              Showing {result.hits.length} random samples.
            </span>
          </div>
        {/if}
      {/await}
    </div>

    {#await result}
      <!-- Awaiting state is already handled above -->
    {:then result}
      {#if result}
        <div class="mt-3 d-flex flex-wrap">
          {#each result.hits as hit, idx}
            <div class="w-25">
              <ImageCard {hit} />
            </div>
          {/each}
        </div>
      {/if}
    {:catch error}
      <div role="alert" class="mt-2 mb-2 alert alert-danger s-dffc7DbZVYr0">
        <strong class="s-dffc7DbZVYr0">Error:</strong>
        {error.message}
      </div>
    {/await}
  </div>
</div>
