<script lang="ts">
  import type { Hits } from "./Api";
  import ImageCard from "./ImageCard.svelte";
  import { labeled } from "./Api";
  import { onMount } from "svelte";
  import * as api from "./Api";

  let result: Promise<api.LabelCountsResponse> | null = null;
  let resultHits: Promise<Hits> | null = null;
  let visibleResults: number = 10;

  onMount(() => {
    result = api.labelCounts();
  });

  function handleClick() {
    api.downloadFile();
  }

  function onQuerySubmit() {
    resultHits = labeled();
  }

  function loadMore() {
    visibleResults += 10; // Increase the number of visible results
  }

</script>

<div class="container">
  <div class="py-4">
    <h1>Statistics</h1>
    {#await result}
      <div class="mt-2 mb-3">
        <span>
          <i class="fa fa-spinner fa-spin" aria-hidden="true" />
          Loading...
        </span>
      </div>
    {:then result}
      {#if result}
        <span>Number of labeled items:</span>
        <ul>
          {#each Object.entries(result.counts) as [label, count]}
            <li>
              <span class="badge rounded-pill bg-secondary">
                {label}
              </span>
              ({count})
            </li>
          {/each}
        </ul>
      {/if}
    {/await}

    <h1>Downloads</h1>
    <p>
      Only images with labels
      <span class="badge rounded-pill bg-secondary">animal origin</span>
      and
      <span class="badge rounded-pill bg-secondary">not animal origin</span>
      :
    </p>
    <button class="btn btn-primary" on:click={handleClick}>
      <icon class="fa fa-download" />
      Download as ZIP file
    </button>
  </div>
    <div class="py-4">
      <div class="row gy-2 gx-2 align-items-center">
        <div class="col-auto me-2">
          <button class="btn btn-primary" on:click={onQuerySubmit}>
            <i class="fa fa-random" aria-hidden="true" />
            Show labeled images
          </button>
        </div>
        {#await resultHits}
          <div class="col-auto">
            <span>
              <i class="fa fa-spinner fa-spin" aria-hidden="true" />
              Loading...
            </span>
          </div>
        {:then resultHits}
          {#if resultHits}
            <div class="col-auto">
              <span class="form-text">
                Showing  {visibleResults} results from {resultHits.hits.length} in total.
              </span>
            </div>
          {/if}
        {/await}
      </div>

      {#await resultHits}
        <!-- Awaiting state is already handled above -->
      {:then resultHits}
        {#if resultHits}
          <div class="mt-3 d-flex flex-wrap">
            {#each resultHits.hits.slice(0, visibleResults) as hit (hit.image_path)}
              <div class="w-25">
                <ImageCard {hit} />
              </div>
            {/each}
          </div>
          {#if visibleResults < resultHits.hits.length}
          <button class="btn btn-primary"
            on:click={loadMore}>Load More</button>
        {/if}
        {/if}
      {:catch error}
        <div role="alert" class="mt-2 mb-2 alert alert-danger s-dffc7DbZVYr0">
          <strong class="s-dffc7DbZVYr0">Error:</strong>
          {error.message}
        </div>
      {/await}
    </div>
</div>
