<script>
  import * as api from "./Api";

  export let dataToCSV = [];
  let prevDataToCSV;

  export let allowedFileExtensions = ["csv"];

  let maxFileSize = 31457280;

  // this is the variable that the file gets bound to
  let uploader;

  let uploading = false; // Add a variable to track the uploading state
  let responseMessage = "";

  async function uploadFile(event) {
    event.preventDefault();
    const file = uploader.files[0];
    uploading = true; // Set uploading state to true
    await onUpload(file);
    uploading = false; // Reset uploading state
  }

  async function onUpload(file) {
    try {
      responseMessage = await api.loadCSV(file);
    } catch (error) {
      responseMessage = `Error loading CSV data: ${error.message}`;
    }
  }
</script>

<div class="container">
  <div class="py-4">
    <h1>Load CSV data</h1>
    <p>Select a CSV file</p>
    <input bind:this={uploader} type="file" class="form-control" style="max-width:400px"/>
    <div class="pt-2">
      <button class="btn btn-primary" on:click={uploadFile} >
        <span class="fa fa-download mr-2" type="file" />
        Load CSV
      </button>
    </div>

    <div class="mt-2">
    {#if uploading}
        <span>
          <i class="fa fa-spinner fa-spin" aria-hidden="true" />
          Loading...
        </span>
        {:else if responseMessage}
        <div>
          <p>{responseMessage}</p>
        </div>
        {/if}
      </div>
    </div>
  </div>
