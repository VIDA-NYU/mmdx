<script lang="ts">
  //
  // This component is based on code from svelte-search's component (MIT license).
  // URL: https://github.com/metonym/svelte-search/blob/master/src/Search.svelte
  //
  import SearchForm from "./SearchForm.svelte";

  interface Hits {
    total: number;
    hits: Hit[];
  }

  interface Hit {
    image: string;
    title: string;
  }

  const limit = 4 * 3;
  let queryStr = "";
  let result: Hits | null = null;

  function onQuerySubmit() {
    result = search(queryStr, limit);
  }

  function search(queryStr: string, limit: number): Hits {
    function randomStr(len: number): string {
      var text = "";
      var charset = "abcdefghijklmnopqrstuvwxyz0123456789";
      for (var i = 0; i < len; i++) {
        text += charset.charAt(Math.floor(Math.random() * charset.length));
      }
      return text;
    }
    const imgs = [
      "image1.jpg",
      "image2.jpg",
      "breakfast-8200753_1920.jpg",
      "dahlias-8215514_1920.jpg",
      "dog-8199216_1920.jpg",
      "food-8151625_1920.jpg",
      "green-sea-turtle-8199770_1920.jpg",
      "plum-blossoms-7177367_1920.jpg",
      "bird-8175466_1920.jpg",
      "bird-8191339_1920.jpg",
      "oranges-8193789_1920.jpg",
      "bicycle-8029570_1920.jpg",
      "marshlands-8176000_1920.png",
      "plane-8145957_1920.jpg",
    ];
    let hits: Hit[] = [];
    for (let i = 0; i < limit; i++) {
      let idx = Math.floor(Math.random() * imgs.length);
      const [randomItem] = imgs.splice(idx, 1); // take out a random item from imgs
      hits.push({
        title: "/" + queryStr + "/" + randomStr(16) + "/" + randomItem,
        image: "src/assets/" + randomItem,
      });
    }
    return { total: hits.length, hits };
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

    {#if result}
      <div class="mt-2 mb-3">
        {#if queryStr}
          <button class="btn btn-secondary btn-sm me-1" on:click={clearSearch}>
            <span class="fa fa-close" aria-label="Close" /> Clear
          </button>
        {/if}
        <span
          >Showing {result.hits.length} ouf of {result.total} results for query "{queryStr}".</span
        >
      </div>
      <div class="d-flex flex-wrap">
        {#each result.hits as { image, title }, idx}
          <div class="w-25">
            <div class="card me-3 mb-3">
              <img
                src={image}
                style="max-height: 350px;"
                class="card-img-top"
                alt="Search result #{idx + 1}"
              />

              <div class="card-body">
                <!-- <h4 class="card-title text-sm">Card title</h4> -->
                <p class="card-text">
                  #{idx + 1}
                  {title}
                </p>
                <btn class="btn btn-sm btn-success">Relevant</btn>
                <btn class="btn btn-sm btn-secondary">Irrelevant</btn>
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  /* .w-33 {
    width: 33.33% !important;
  } */
</style>
