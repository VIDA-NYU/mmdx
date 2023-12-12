<script lang="ts">
  import Modal from "./Modal.svelte";
  import type { Hit } from "./Api";
  import { navigate } from "svelte-routing";
  import { labelStore, animalStore, negativeKeywordStore } from "./stores";
  import AutoComplete from "simple-svelte-autocomplete";
  import * as api from "./Api";

  export let hit: Hit;
  $: parsedHitMetadata = hit.metadata;

  let showModal = false;

  let allLabels: string[];
  let allAnimals: string[];
  let allNegKeywords: string[];
  let selectedDescription: string;
  let selectedNegKeyword: string;
  let selectedAnimal: string;
  $: hitLabels = hit.labels;
  $: hittypes = hit.labels_types_dict;

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

  animalStore.subscribe((storeAnimals) => {
    allAnimals = storeAnimals;
  });

  negativeKeywordStore.subscribe((storeNegKeyword) => {
    allNegKeywords = storeNegKeyword;
  });

  function addLabel(newLabel: string) {
    if (!newLabel || newLabel === "") {
      return;
    }
    let hitLabels = hit.labels;
    let hitRelevants = hit.relevant;
    if (hitRelevants && hitRelevants.length > 0) {
      if (hitRelevants.includes(newLabel)) {
        return;
      }
      if (
        newLabel === "animal origin" &&
        hitRelevants.includes("not animal origin")
      ) {
        api.removeLabel(hit.image_path, "not animal origin", "relevant");
        hitLabels = hitLabels.filter((l) => l !== "not animal origin");
        hitRelevants = hitRelevants.filter((l) => l !== "not animal origin");
      } else if (
        newLabel === "not animal origin" &&
        hitLabels.includes("animal origin")
      ) {
        api.removeLabel(hit.image_path, "animal origin", "relevant");
        hitLabels = hitLabels.filter((l) => l !== "animal origin");
        hitRelevants = hitRelevants.filter((l) => l !== "animal origin");
      }
      hitLabels = [...new Set([...hitLabels, newLabel])];
      hitRelevants = [...new Set([...hitRelevants, newLabel])];
    } else {
      hitLabels = [...new Set([...hitLabels, newLabel])];
      hitRelevants = [newLabel];
    }
    hit.labels = hitLabels;
    hit.relevant = hitRelevants;
    try {
      api.addLabel(hit.image_path, newLabel, "relevant");
    } catch (e) {
      console.log(e);
    }
  }

  function addDescription(newDescription: string) {
    if (!newDescription || newDescription === "") {
      return;
    }
    let hitDescription = hit.description;
    let hitLabels = hit.labels;
    if (hitDescription && hitDescription.length > 0) {
      if (hitDescription.includes(newDescription)) {
        api.removeLabel(hit.image_path, newDescription, "description");
        hitDescription = hitDescription.filter((l) => l !== newDescription);
        if (
          hitLabels &&
          hitLabels.length > 0 &&
          hitLabels.includes(newDescription)
        ) {
          hitLabels = hitLabels.filter((l) => l !== newDescription);
        }
      } else {
        hitDescription = [...new Set([...hitDescription, newDescription])];
        hitLabels = [...new Set([...hitLabels, newDescription])];
      }
    } else {
      hitDescription = [newDescription];
      hitLabels = [...new Set([...hitLabels, newDescription])];
    }
    hit.description = hitDescription;
    hit.labels = hitLabels;
    try {
      api.addLabel(hit.image_path, newDescription, "description");
    } catch (e) {
      console.log(e);
    }
  }

  function addAnimal(newAnimal: string) {
    if (!newAnimal || newAnimal === "") {
      return;
    }
    let hitLabels = hit.labels;
    let hitAnimal = hit.animal;
    if (hitAnimal && hitAnimal !== newAnimal) {
      api.removeLabel(hit.image_path, hitAnimal, "animal");
    }

    if (hitLabels && hitLabels.length > 0) {
      if (hitAnimal && hitLabels.includes(hitAnimal)) {
        hitLabels = hitLabels.filter((l) => l !== hitAnimal);
        hitLabels = [...new Set([...hitLabels, newAnimal])];
      } else {
        hitLabels = [...new Set([...hitLabels, newAnimal])];
      }
    } else {
      hit.labels = [newAnimal];
      hitLabels = hit.labels;
    }
    hit.labels = hitLabels;
    hitAnimal = newAnimal;
    hit.animal = hitAnimal;

    try {
      api.addLabel(hit.image_path, newAnimal, "animal");
    } catch (e) {
      console.log(e);
    }
  }

  function addKeyword(newKeyword: string) {
    console.log("add", newKeyword);
    if (!newKeyword || newKeyword === "") {
      return;
    }
    let hitNegKeywords = hit.keywords;
    let hitLabels = hit.labels;
    if (hitNegKeywords && hitNegKeywords.length > 0) {
      if (hitNegKeywords.includes(newKeyword)) {
        api.removeLabel(hit.image_path, newKeyword, "keywords");
        if (
          hitLabels &&
          hitLabels.length > 0 &&
          hitLabels.includes(newKeyword)
        ) {
          hitLabels = hitLabels.filter((l) => l !== newKeyword);
        }
      } else {
        hitNegKeywords = [...new Set([...hitNegKeywords, newKeyword])];
        hitLabels = [...new Set([...hitLabels, newKeyword])];
      }
    } else {
      hitNegKeywords = [newKeyword];
      hitLabels = [...new Set([...hitLabels, newKeyword])];
    }
    hit.keywords = hitNegKeywords;
    hit.labels = hitLabels;
    try {
      api.addLabel(hit.image_path, newKeyword, "keywords");
    } catch (e) {
      console.log(e);
    }
  }

  function onChangeDescription(newLabel: string) {
    if (newLabel) {
      console.log("onChangeDescription", newLabel);
      addDescription(newLabel);
    } else {
      console.log("undefined Description: ", newLabel);
    }
  }

  function handleCreateDescription(newLabel: string) {
    labelStore.update((storeLabels) => {
      return [...new Set([...storeLabels, newLabel])];
    });
    return newLabel; // return the new label to the autocomplete
  }

  function onChangeKeyword(newKeyword: string) {
    if (newKeyword) {
      console.log("onChangeKeyword", newKeyword);
      addKeyword(newKeyword);
    } else {
      console.log("undefined Keyword: ", newKeyword);
    }
  }

  function handleCreateKeyword(newKeyword: string) {
    negativeKeywordStore.update((storeNegKeyword) => {
      return [...new Set([...storeNegKeyword, newKeyword])];
    });
    return newKeyword; // return the new label to the autocomplete
  }

  function onChangeAnimal(newAnimal: string) {
    if (newAnimal) {
      console.log("onChangeAnimal", newAnimal);
      addAnimal(newAnimal);
    } else {
      console.log("undefined label: ", newAnimal);
    }
  }

  function removeLabels(label: string) {
    let hitLabels = hit.labels;
    let hittypes = hit.labels_types_dict;
    if (hittypes && hittypes[label]) {
      api.removeLabel(hit.image_path, label, hittypes[label]);
      hittypes = hit.labels_types_dict;
    }
    if (hitLabels && hitLabels.includes(label)) {
      hitLabels = hitLabels.filter((l) => l !== label);
      hit.labels = hitLabels;
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
      {hit.title ? hit.title : hit.image_path}
    </p>
    <button class="btn btn-sm btn-info" on:click={() => (showModal = true)}
      >Metadata</button
    >
    <div class="btn-toolbar mt-1">
      <div class="btn-group me-2" role="group" aria-label="">
        <button
          class="btn btn-sm btn-success"
          on:click={() => addLabel("animal origin")}
        >
          <i class="fa fa-thumbs-up" aria-hidden="true" />
        </button>
        <button
          class="btn btn-sm btn-warning"
          on:click={() => addLabel("not animal origin")}
        >
          <i class="fa fa-thumbs-down" aria-hidden="true" />
        </button>
      </div>
      <div class="btn-group me-2 mt-1" role="group" aria-label="">
        <AutoComplete
          debug={false}
          inputClassName="form-control"
          items={allAnimals}
          bind:selectedItem={selectedAnimal}
          create={false}
          onChange={onChangeAnimal}
          placeholder="Animal"
        />
      </div>
      <div class="box-container">
        <div class="btn-group me-2" role="group" aria-label="">
          <AutoComplete
            debug={false}
            inputClassName="form-control"
            items={allLabels}
            bind:selectedItem={selectedDescription}
            create={true}
            onCreate={handleCreateDescription}
            onChange={onChangeDescription}
            placeholder="Description"
          />
        </div>
      </div>
      <div class="box-container">
        <div class="btn-group me-2" role="group" aria-label="">
          <AutoComplete
            debug={false}
            inputClassName="form-control"
            items={allNegKeywords}
            bind:selectedItem={selectedNegKeyword}
            create={true}
            onChange={onChangeKeyword}
            onCreate={handleCreateKeyword}
            placeholder="Negative Keyword"
          />
        </div>
      </div>
      {#if hitLabels && hitLabels.length > 0}
        <div class="btn-toolbar">
          {#each hitLabels as label, idx}
            <span
              class="badge rounded-pill bg-secondary me-1 mt-2 position-relative"
            >
              <!-- style="background-color: {colors[idx]} !important;" -->
              {label}
              <span
                role="button"
                on:click={() => removeLabels(label)}
                class="position-absolute top-0 start-100 translate-middle"
              >
                <i class="fa fa-times-circle" aria-hidden="true" />
                <span class="visually-hidden">Remove label</span>
              </span>
            </span>
          {/each}
        </div>
      {/if}
    </div>
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

<Modal bind:showModal>
  <h2 slot="header">Metadata</h2>

  <ul slot="body" class="definition-list___">
    <li>
      <strong>title:</strong>
      {hit.title ? hit.title : hit.image_path}
    </li>
    {#each Object.keys(parsedHitMetadata) as key}
      <li>
        {#if key == "url"}
          <strong>{key}:</strong>
          <a
            href={parsedHitMetadata[key]}
            target="_blank"
            referrerpolicy="no-referrer">{parsedHitMetadata[key]}</a
          >
        {:else}
          <strong>{key}:</strong> {parsedHitMetadata[key]}
        {/if}
      </li>
    {/each}
    <!-- Metadata:
    {hit.metadata} -->
  </ul>
</Modal>

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
    width: 171px !important;
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
  h1 {
    font-size: 1rem;
    text-align: center;
  }
</style>
