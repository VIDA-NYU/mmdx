<script lang="ts">
  import type { Hit } from "./Api";
  import {
    labelStore,
    animalStore,
    negativeKeywordStore,
    selectedDataStore,
  } from "./stores";
  import AutoComplete from "simple-svelte-autocomplete";
  import * as api from "./Api";

  export let allHits: Hit[];

  let allLabels: string[];
  let allAnimals: string[];
  let allNegKeywords: string[];
  let selectedDescription: string;
  let selectedNegKeyword: string;
  let selectedAnimal: string;
  let allSelectedData: { [key: string]: boolean };
  let hitLabelsall = {};

  labelStore.subscribe((storeLabels) => {
    allLabels = storeLabels;
  });

  animalStore.subscribe((storeAnimals) => {
    allAnimals = storeAnimals;
  });

  negativeKeywordStore.subscribe((storeNegKeyword) => {
    allNegKeywords = storeNegKeyword;
  });

  selectedDataStore.subscribe((storeSelectedData) => {
    allSelectedData = storeSelectedData;
  });

  function addLabelExclusive(newLabel: string, type: keyof Hit) {
    if (!newLabel || newLabel === "") {
      return;
    }
    console.log(hitLabelsall)
    if (
      hitLabelsall &&
      Object.keys(hitLabelsall).length !== 0
    ) {
      const labelKey = Object.keys(hitLabelsall).find((key) => hitLabelsall[key] === type);
      if (labelKey && labelKey !== newLabel) {
        delete hitLabelsall[labelKey];
      }
    }
    hitLabelsall[newLabel] = `${type}`;
    // Send label for all hits marked
    for (let hit of allHits) {
      if (allSelectedData[hit.image_path] === true) {
        let hitLabels = hit.labels_types_dict;
        let hitKey = hit[type]; // label from table type
        if (typeof hitKey === 'string') {
          if (hitKey === newLabel) {
            return; // label already applied
          }
          if (
            hitKey !== newLabel
          ){
            api.removeLabel(hit.image_path, hitKey, `${type}`);
            delete hitLabels[hitKey];
          }
        }
        hitLabels[newLabel] = `${type}`;
        hitKey = newLabel;
        hit.labels_types_dict = hitLabels;
        hit[type] = hitKey;
        try {
          api.addLabel(hit.image_path, newLabel, `${type}`);
        } catch (e) {
          console.log(e);
        }
      }
    }
    console.log(hitLabelsall)
  }

  function addLabelInclusive(newLabel: string, type: keyof Hit) {
    if (!newLabel || newLabel === "") {
      return;
    }
    hitLabelsall[newLabel] =  `${type}`;
    // add label for each hit on page
    for (let hit of allHits) {
      if (allSelectedData[hit.image_path] === true) {
        let hitKey = hit[type];
        let hitLabels = hit.labels_types_dict;
        if ((Array.isArray(hitKey)) && hitKey.length > 0) {
          if (hitKey.includes(newLabel)) {
            return;
          } else {
            hitKey = [...new Set([...hitKey, newLabel])];
          }
        } else {
          hitKey = [newLabel];
        }
        hitLabels[newLabel] = `${type}`;
        hit[type] = hitKey; // TODO: future remove all from HIT and use only the dict
        hit.labels_types_dict = hitLabels;
        try {
          api.addLabel(hit.image_path, newLabel, `${type}`);
        } catch (e) {
          console.log(e);
        }
      }
    }
  }

  function onChangeDescription(newLabel: string) {
    if (newLabel) {
      console.log("onChangeDescription", newLabel);
      addLabelInclusive(newLabel, "description");
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
      addLabelInclusive(newKeyword, "keywords");
    } else {
      console.log("undefined Keyword: ", newKeyword);
    }
  }

  function handleCreateKeyword(newKeyword: string) {
    negativeKeywordStore.update((storeNegKeyword) => {
      return [...new Set([...storeNegKeyword, newKeyword])];
    });
    return newKeyword;
  }

  function onChangeAnimal(newAnimal: string) {
    console.log("change", hitLabelsall, newAnimal);
    if (newAnimal) {
      console.log("onChangeAnimal", newAnimal);
      addLabelExclusive(newAnimal, "animal");
    } else {
      console.log("undefined label: ", newAnimal);
    }
  }

  function removeLabels(label: string) {
    delete hitLabelsall[label];
    hitLabelsall = hitLabelsall;
    for (let hit of allHits) {
      if (allSelectedData[hit.image_path] === true) {
        let hitLabels = hit.labels_types_dict;
        let type =  hitLabels[label] as keyof Hit;
        if (hitLabels && hitLabels[label]) {
          api.removeLabel(hit.image_path, label, `${type}`);
          delete hitLabels[label];
          hitLabels = hitLabels;
          hit.labels_types_dict = hitLabels;
          if (typeof hit[type] === 'string'){
            hit[type] = undefined
          }else if (Array.isArray(hit[type])){
            hit[type] = hit[type].filter((l) => l !== label);
          }
        }
      }
    }
  }

</script>

<div class="card me-3 mb-3">
  <div class="card-header">Label All Ads</div>
  <div class="box-container">
    <div class="card-body">
      <div class="btn-toolbar mt-1">
        <div class="btn-group me-2" role="group" aria-label="">
          <button
            class="btn btn-sm btn-success"
            on:click={() => addLabelExclusive("animal origin", "relevant")}
          >
            <i class="fa fa-thumbs-up" aria-hidden="true" />
          </button>
          <button
            class="btn btn-sm btn-warning"
            on:click={() => addLabelExclusive("not animal origin", "relevant")}
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
      </div>
    </div>
  </div>
  {#if hitLabelsall && Object.keys(hitLabelsall).length > 0}
    <div class="btn-toolbar">
      {#each Object.entries(hitLabelsall) as [label, value], idx}
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
