<script>
  import PapaParse from 'papaparse'
  import * as api from "./Api";

  export let dataToCSV = [];
  let prevDataToCSV;

  export let allowedFileExtensions = ['csv'];

  let maxFileSize = 31457280;

  // this is the variable that the file gets bound to
  let uploader;

  $: {
    // called on props change
    if (dataToCSV !== prevDataToCSV && dataToCSV.length !== 0) {
      prevDataToCSV = dataToCSV;
      const csvData = PapaParse.unparse(dataToCSV);
      onUpload ? onUpload(csvData) : console.log("Remember to define an onUpload function as props. CSV Data:", csvData);
    }
  }

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
  <h1>Load CSV data</h1>
  <p>Select a CSV file</p>
  <input bind:this={uploader} type="file" />
  <div>
    <button class="btn btn-primary" on:click={uploadFile} type="file">
      Load CSV
    </button>
  </div>

  {#if uploading}
    <div>
      <p>Uploading...</p>
    </div>
  {:else if responseMessage}
    <div>
      <p>{responseMessage}</p>
    </div>
  {/if}
</div>
