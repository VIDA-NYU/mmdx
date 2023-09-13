<script lang="ts">
  import type { Hit } from "./Api";
  import { navigate } from "svelte-routing";

  export let hit: Hit;
</script>

<div class="card me-3 mb-3">
  <img
    src={"/images/" + hit.image}
    style="max-height: 350px;"
    class="card-img-top"
  />

  <div class="card-body">
    <p class="card-text">
      {hit.title}
    </p>
    <div class="btn-group mt-1" role="group" aria-label="">
      <button class="btn btn-sm btn-success">
        <i class="fa fa-thumbs-up" aria-hidden="true" />
        <!-- Relevant -->
      </button>
      <button class="btn btn-sm btn-warning">
        <i class="fa fa-thumbs-down" aria-hidden="true" />
        <!-- Irrelevant -->
      </button>
    </div>
    <div class="btn-group mt-1" role="group" aria-label="">
      <button
        class="btn btn-sm btn-info"
        on:click={() => navigate("/search/image?q=" + hit.image)}
      >
        <i class="fa fa-search" aria-hidden="true" />
        Find Similar
      </button>
    </div>
  </div>
</div>
