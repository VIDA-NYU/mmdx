<script lang="ts">
  import type { Hits } from "./Api";
  import { similarSearch } from "./Api";
  import ImageCard from "./ImageCard.svelte";

  let imagePath = "";
  let result: Promise<Hits> | null = null;
  let limit: string = "16";

  function searchSimilarImages(searchPath: string) {
    const params = new URLSearchParams(searchPath);
    const q = params.get("q");
    if (q) {
      imagePath = q;
      result = similarSearch(imagePath, +limit);
    }
  }

  function onQuerySubmit() {
    searchSimilarImages(location.search);
  }

  // location is received as component props
  export let location: Location;
  $: {
    // this block is reactively triggered whenever the location variable (which contains the URL) changes
    searchSimilarImages(location.search);
  }
</script>

<div class="container">
  <div class="py-5">
    <div class="row">
      <div class="input-group input-group-lg">
        <span class="input-group-text p-0">
          <img
            src={"/images/" + imagePath}
            class="card-img-left search-box-image"
            aria-hidden="true"
            alt="Image used as query used for similar image search"
          />
        </span>
        <input
          type="text"
          bind:value={imagePath}
          disabled
          class="form-control"
          placeholder="Search..."
        />
      </div>
    </div>
    <div class="row mt-2 mb-2 gx-2 align-items-center">
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
              Showing {result.hits.length} results for image query "{imagePath}".
            </span>
          </div>
        {/if}
      {/await}
    </div>
    {#await result}
      <!-- Awaiting state is already handled above -->
    {:then result}
      {#if result}
        <div class="d-flex flex-wrap">
          {#each result.hits as hit}
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

<style>
  .search-box-image {
    max-height: 48px;
    min-width: 48px;
    border-bottom-left-radius: var(--bs-border-radius-lg) !important;
    border-top-left-radius: var(--bs-border-radius-lg) !important;
  }
</style>
