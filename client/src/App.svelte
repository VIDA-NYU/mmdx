<script lang="ts">
  import { Router, Link, Route } from "svelte-routing";
  import { onMount } from "svelte";
  import { labelStore } from "./lib/stores";
  import * as api from "./lib/Api";
  import BootstrapComponents from "./BootstrapComponents.svelte";
  import Search from "./lib/Search.svelte";
  import Random from "./lib/Random.svelte";
  import ImageSearch from "./lib/ImageSearch.svelte";
  import LabeledData from "./lib/LabeledData.svelte";

  export let url = "";

  onMount(async () => {
    console.log("Loading labels...");
    const remoteLabels = await api.loadLabels();
    labelStore.update((labels: string[]) => [
      ...new Set([...labels, ...remoteLabels.labels]),
    ]);
    console.log("Labels loaded: ", remoteLabels);
  });

  function getLinkProps(args: Object): Object {
    const { href, isPartiallyCurrent, isCurrent } = args as {
      href: string;
      isPartiallyCurrent: boolean;
      isCurrent: boolean;
    };
    const isActive = href === "/" ? isCurrent : isPartiallyCurrent || isCurrent;
    return isActive ? { class: "nav-link active" } : { class: "nav-link" };
  }
</script>

<main>
  <Router {url}>
    <nav class="navbar navbar-expand-lg sticky-top">
      <div class="container-fluid">
        <Link class="navbar-brand fw-bold" to="/">MMDX</Link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavAltMarkup"
          aria-controls="navbarNavAltMarkup"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon" />
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav nav-underline">
            <Link to="/" getProps={getLinkProps}>Keyword Search</Link>
            <Link to="/search/random" getProps={getLinkProps}
              >Random Search</Link
            >
            <Link to="/search/image" getProps={getLinkProps}>Image Search</Link>
            <Link to="/labels" getProps={getLinkProps}>Labels</Link>
            <!-- <Link to="/bootstrap" getProps={getLinkProps}>Bootstrap</Link> -->
          </div>
        </div>
      </div>
    </nav>

    <div>
      <Route path="/" component={Search} />
      <Route path="/search/random" component={Random} />
      <Route
        path="/search/image"
        component={ImageSearch}
        location={window.location}
      />
      <Route path="/labels" component={LabeledData} />
      <Route path="/bootstrap" component={BootstrapComponents} />
    </div>
  </Router>
</main>
