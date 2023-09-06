import './app.css'
import App from './App.svelte'

// This includes Popper and all of Bootstrap's JS plugins.
import bootstrap from "bootstrap/dist/js/bootstrap.bundle.min.js";

const app = new App({
  target: document.getElementById('app'),
})

export default app
