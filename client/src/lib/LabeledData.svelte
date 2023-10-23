<script lang="ts">
    import { downloadFile } from "./Api";

    function handleClick() {
        downloadFile();
    }
</script>

<div class="container">
    <div class="py-5">
        <h1>Labeled Data</h1>
        <button class="btn btn-primary" on:click={handleClick}>
            <icon class="fa fa-download" />
            Download as ZIP file
        </button>
    </div>
</div>
