<script lang="ts">
  import type { Hit } from "./Api";
  import { navigate } from "svelte-routing";
  import { labelStore } from "./stores";
  import AutoComplete from "simple-svelte-autocomplete";
  import * as api from "./Api";

  export let hit: Hit;

  let allLabels: string[];
  let selectedLabel: string;

  // $: hitLabels = hit.labels?.filter((l) => l); // filter undefined labels
  $: hitLabels = hit.labels;

  // tableau10 colors
  const colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
  ];

  labelStore.subscribe((storeLabels) => {
    allLabels = storeLabels;
  });

  function addLabel(newLabel: string) {
    if (!newLabel || newLabel === "") {
      return;
    }
    let hitLabels = hit.labels;
    if (hitLabels && hitLabels.length > 0) {
      if (hitLabels.includes(newLabel)) {
        return;
      }
      if (newLabel === "relevant" && hitLabels.includes("irrelevant")) {
        api.removeLabel(hit.image_path, "irrelevant");
        hitLabels = hitLabels.filter((l) => l !== "irrelevant");
      } else if (newLabel === "irrelevant" && hitLabels.includes("relevant")) {
        api.removeLabel(hit.image_path, "relevant");
        hitLabels = hitLabels.filter((l) => l !== "relevant");
      }
      hitLabels = [...new Set([...hitLabels, newLabel])];
    } else {
      hitLabels = [newLabel];
    }
    hit.labels = hitLabels;
    try {
      api.addLabel(hit.image_path, newLabel);
    } catch (e) {
      console.log(e);
    }
  }

  function handleCreateLabel(newLabel: string) {
    console.log(hit);

    labelStore.update((storeLabels) => {
      return [...new Set([...storeLabels, newLabel])];
    });
    addLabel(newLabel);
    return newLabel; // return the new label to the autocomplete
  }

  function onChangeLabel(newLabel: string) {
    if (newLabel) {
      console.log("onChangeLabel", newLabel);
      addLabel(newLabel);
    } else {
      // console.log("undefined label: ", newLabel);
    }
  }
</script>

<div class="card me-3 mb-3">
  <img
    src={"/images/" + hit.image_path}
    style="max-height: 350px;"
    class="card-img-top"
  />

  <div class="card-body">
    <p class="card-text mb-2">
      {hit.image_path}
    </p>
    <div class="btn-toolbar mt-1">
      <div class="btn-group me-2" role="group" aria-label="">
        <button
          class="btn btn-sm btn-success"
          on:click={() => addLabel("relevant")}
        >
          <i class="fa fa-thumbs-up" aria-hidden="true" />
        </button>
        <button
          class="btn btn-sm btn-warning"
          on:click={() => addLabel("irrelevant")}
        >
          <i class="fa fa-thumbs-down" aria-hidden="true" />
        </button>
      </div>
      <div class="btn-group me-2" role="group" aria-label="">
        <AutoComplete
          debug={false}
          inputClassName="form-control"
          items={allLabels}
          bind:selectedItem={selectedLabel}
          create={true}
          onChange={onChangeLabel}
          onCreate={handleCreateLabel}
        />
        <!-- <button class="btn btn-sm btn-primary">
          <span class="fa fa-plus" />
        </button> -->
      </div>
    </div>
    {#if hitLabels && hitLabels.length > 0}
      <div class="btn-toolbar">
        {#each hitLabels as label, idx}
          <span class="badge rounded-pill bg-secondary me-1 mt-2">
            <!-- style="background-color: {colors[idx]} !important;" -->
            {label}
          </span>
        {/each}
      </div>
    {/if}
    <div class="btn-toolbar mt-2">
      <button
        class="btn btn-sm btn-info"
        on:click={() => navigate("/search/image?q=" + hit.image_path)}
      >
        <i class="fa fa-search" aria-hidden="true" />
        Find Similar
      </button>
    </div>
  </div>
</div>

<style>
  :global(.autocomplete-list) {
    --bs-dropdown-zindex: 1000;
    --bs-dropdown-min-width: 10rem;
    --bs-dropdown-padding-x: 0;
    --bs-dropdown-padding-y: 0.1rem;
    --bs-dropdown-spacer: 0.125rem;
    --bs-dropdown-font-size: 1rem;
    --bs-dropdown-color: var(--bs-body-color);
    --bs-dropdown-bg: var(--bs-body-bg);
    --bs-dropdown-border-color: var(--bs-border-color-translucent);
    --bs-dropdown-border-radius: var(--bs-border-radius);
    --bs-dropdown-border-width: var(--bs-border-width);
    --bs-dropdown-inner-border-radius: calc(
      var(--bs-border-radius) - var(--bs-border-width)
    );
    --bs-dropdown-divider-bg: var(--bs-border-color-translucent);
    --bs-dropdown-divider-margin-y: 0.1rem;
    --bs-dropdown-box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    --bs-dropdown-link-color: var(--bs-body-color);
    --bs-dropdown-link-hover-color: var(--bs-body-color);
    --bs-dropdown-link-hover-bg: var(--bs-tertiary-bg);
    --bs-dropdown-link-active-color: #fff;
    --bs-dropdown-link-active-bg: #7c6bb2;
    --bs-dropdown-link-disabled-color: var(--bs-tertiary-color);
    --bs-dropdown-item-padding-x: 1rem;
    --bs-dropdown-item-padding-y: 0.25rem;
    --bs-dropdown-header-color: #6c757d;
    --bs-dropdown-header-padding-x: 1rem;
    --bs-dropdown-header-padding-y: 0.1rem;

    color: var(--bs-dropdown-color) !important;
    text-align: left !important;
    list-style: none !important;
    background-color: var(--bs-dropdown-bg) !important;
    background-clip: padding-box !important;
    border: var(--bs-dropdown-border-width) solid
      var(--bs-dropdown-border-color) !important;
    border-radius: var(--bs-dropdown-border-radius) !important;
  }
  :global(.autocomplete-list-item) {
    color: var(--bs-dropdown-color) !important;
  }
  :global(
      .autocomplete-list .selected,
      .dropdown-item:hover,
      .dropdown-item:focus
    ) {
    color: var(--bs-dropdown-link-hover-color) !important;
    background-color: var(--bs-dropdown-link-hover-bg) !important;
  }
  :global(.input-container > .form-control) {
    padding: 0.25rem 0.5rem !important;
    font-size: 0.875rem !important;
    border-radius: var(--bs-border-radius-sm);
  }
  :global(.autocomplete) {
    height: 2em !important;
    min-width: 100px !important;
  }
  :global(.autocomplete-list-item-create) {
    width: 169px !important;
  }
  :global(.input-container) {
    /* width: 207px !important; */
    width: 171px !important;
  }
</style>
