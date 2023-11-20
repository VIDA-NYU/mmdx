<script lang="ts">
  import { onMount } from "svelte";
  import * as api from "./Api";

  let result: Promise<api.LabelCountsResponse> | null = null;

  onMount(() => {
    result = api.labelCounts();
  });

  function handleClick() {
    api.downloadFile();
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
      <span class="badge rounded-pill bg-secondary">relevant</span>
      and
      <span class="badge rounded-pill bg-secondary">irrelevant</span>
      :
    </p>
    <button class="btn btn-primary" on:click={handleClick}>
      <icon class="fa fa-download" />
      Download as ZIP file
    </button>
  </div>
</div>
