<script lang="ts">
  import SearchForm from "./SearchForm.svelte";
  import type { Hits } from "./Api";
  import { keywordSearch } from "./Api";
  import ImageCard from "./ImageCard.svelte";

  const limit = 4 * 3;
  let queryStr = "";
  let result: Promise<Hits> | null = null;

  function onQuerySubmit() {
    result = keywordSearch(queryStr, limit);
  }

  function clearSearch() {
    queryStr = "";
    result = null;
  }
</script>

<div class="container">
  <div class="py-5">
    <SearchForm
      bind:value={queryStr}
      on:submit={onQuerySubmit}
      autofocus={true}
      class="form-control"
      hideLabel={true}
      label="Image search:"
      placeholder="Search..."
    />

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
          {#if queryStr}
            <button
              class="btn btn-secondary btn-sm me-1"
              on:click={clearSearch}
            >
              <span class="fa fa-close" aria-label="Close" /> Clear
            </button>
          {/if}
          <span>
            Showing {result.hits.length} out of {result.total} results for query
            "{queryStr}".
          </span>
        </div>
        <div class="d-flex flex-wrap">
          {#each result.hits as hit}
            <div class="w-25">
              <ImageCard {hit} />
            </div>
          {/each}
        </div>
      {/if}
    {:catch error}
      <div role="alert" class="alert alert-danger mt-2 mb-2">
        <strong>Error:</strong>
        {error.message}
      </div>
    {/await}
  </div>
</div>
