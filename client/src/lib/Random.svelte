<script lang="ts">
  import { onMount } from "svelte";
  import type { Hits, Hit } from "./Api";
  import { random } from "./Api";
    import ImageCard from "./ImageCard.svelte";

  const limit = 4 * 2;
  let queryStr = "";
  let result: Promise<Hits> | null = null;

  function onQuerySubmit() {
    result = random(limit);
  }

  onMount(() => {
    onQuerySubmit();
  });
</script>

<div class="container">
  <div class="py-5">
    <button class="btn btn-primary" on:click={onQuerySubmit}>
      <i class="fa fa-random" aria-hidden="true" />
      Reload samples
    </button>
    {#await result}
      <p>
        <i class="fa fa-spinner fa-spin" aria-hidden="true" />
        Loading...
      </p>
    {:then result}
      {#if result}
        <div class="mt-2 mb-3">
          <span>
            Showing {result.hits.length} ouf of {result.total} random samples.
          </span>
        </div>
        <div class="d-flex flex-wrap">
          {#each result.hits as hit, idx}
            <div class="w-25">
              <ImageCard hit={hit} />
              <!-- <div class="card me-3 mb-3">
                <img
                  src={"/images/" + image}
                  style="max-height: 350px;"
                  class="card-img-top"
                  alt="Search result #{idx + 1}"
                />

                <div class="card-body">
                  <p class="card-text">
                    #{idx + 1}
                    {title}
                  </p>
                  <btn class="btn btn-sm btn-success">Relevant</btn>
                  <btn class="btn btn-sm btn-secondary">Irrelevant</btn>
                </div>
              </div> -->
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
