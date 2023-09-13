<script lang="ts">
  import type { Hits } from "./Api";
  import { similar } from "./Api";
  import ImageCard from "./ImageCard.svelte";

  const limit = 4 * 3;
  let imagePath = "";
  let result: Promise<Hits> | null = null;

  function searchSimilarImages(searchPath: string) {
    const params = new URLSearchParams(searchPath);
    const q = params.get("q");
    if (q) {
      imagePath = q;
      result = similar(imagePath, limit);
    }
  }

  // received as component props
  export let location: Location;
  $: {
    // this is triggered whenever the location variable (which contains the URL) changes
    searchSimilarImages(location.search);
  }
</script>

<div class="container">
  <div class="py-5">
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
    {#await result}
      <div class="mt-2 mb-3">
        <span>
          <i class="fa fa-spinner fa-spin" aria-hidden="true" />
          Loading...
        </span>
      </div>
    {:then result}
      {#if result}
        <div class="mt-2 mb-3">
          <span>
            Showing {result.hits.length} out of {result.total} results for image
            query "{imagePath}".
          </span>
        </div>
        <div class="d-flex flex-wrap">
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

<style>
  .search-box-image {
    max-height: 48px;
    min-width: 48px;
    border-bottom-left-radius: var(--bs-border-radius-lg) !important;
    border-top-left-radius: var(--bs-border-radius-lg) !important;
  }
</style>
