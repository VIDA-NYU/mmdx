<script lang="ts">
  import SearchForm from "./SearchForm.svelte";
  import type { Hits } from "./Api";
  import { keywordSearch } from "./Api";
  import ImageCard from "./ImageCard.svelte";

  let limit: string = "16";
  let queryStr = "";
  let result: Promise<Hits> | null = null;

  function onQuerySubmit() {
    result = keywordSearch(queryStr, +limit);
  }

  function clearSearch() {
    queryStr = "";
    result = null;
  }
</script>

<div class="container">
  <div class="py-5">
    <div class="row">
      <SearchForm
        bind:value={queryStr}
        on:submit={onQuerySubmit}
        autofocus={true}
        class="form-control"
        hideLabel={true}
        label="Image search:"
        placeholder="Search..."
      />
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
        <div class="col-auto">
          {#if queryStr}
            <button
              class="btn btn-secondary btn-sm me-1"
              on:click={clearSearch}
            >
              <span class="fa fa-close" aria-label="Close" /> Clear
            </button>
          {/if}
        </div>
        {#if result}
          <div class="col-auto">
            <span class="form-text">
              Showing {result.hits.length} results for query "{queryStr}".
            </span>
          </div>
        {/if}
      {/await}
    </div>

    {#await result}
      <!-- Awaiting state is already handled above -->
    {:then result}
      {#if result}
        <div class="d-flex flex-wrap mt-2 mb-2">
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
