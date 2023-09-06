<script lang="ts">
  import { Popover, Tooltip } from "bootstrap/dist/js/bootstrap.bundle.min.js";

  const onload = (el: HTMLElement) => {
    const popoverTriggerList = document.querySelectorAll(
      '[data-bs-toggle="popover"]'
    );
    const popoverList = [...popoverTriggerList].map(
      (popoverTriggerEl) => new Popover(popoverTriggerEl)
    );

    const tooltipTriggerList = document.querySelectorAll(
      '[data-bs-toggle="tooltip"]'
    );
    const tooltipList = [...tooltipTriggerList].map(
      (tooltipTriggerEl) => new Tooltip(tooltipTriggerEl)
    );
  };
</script>

<main use:onload>
  <div class="container">
    <div class="py-5">
      <h1>A Bootstrap 5 dark theme with a purple color palette.</h1>
      <p>
        This is a custom Bootstrap 5 theme with a custom color scheme designed
        to be used in applications with dark backgrounds.
        <br />
        The elements from this page were originally based on the HackerThemes's
        <a href="https://hackerthemes.com/bootstrap-buffet">buffet</a>, but have
        been modified for Bootstrap 5.
      </p>

      <div>
        <a id="alerts" class="ht-anchor">Main Buttons</a>
        <h5 class="mt-4 mb-3">Main Buttons</h5>

        <div class="row mt-3">
          <div class="col">
            <a href="#!" class="btn btn-primary">Default Button</a>
            <a href="#!" class="btn btn-outline-primary">Outline Button</a>
            <a href="#!" class="btn btn-secondary">Default Button</a>
            <a href="#!" class="btn btn-outline-secondary">Outline Button</a>
          </div>
        </div>

        <div class="row mt-3">
          <div class="col">
            <button type="button" class="btn btn-primary">Primary</button>
            <button type="button" class="btn btn-secondary">Secondary</button>
            <button type="button" class="btn btn-success">Success</button>
            <button type="button" class="btn btn-danger">Danger</button>
            <button type="button" class="btn btn-warning">Warning</button>
            <button type="button" class="btn btn-info">Info</button>
            <button type="button" class="btn btn-light">Light</button>
            <button type="button" class="btn btn-dark">Dark</button>
            <button type="button" class="btn btn-link">Link</button>
          </div>
        </div>
      </div>

      <!-- Elements from HackerThemes's buffet -->
      <div>
        <a id="alerts" class="ht-anchor">Alerts</a>
        <h5 class="mt-4 mb-3">Alerts</h5>

        <div class="mt-3">
          <div class="mt-2 mb-2 alert alert-primary" role="alert">
            <strong>Well done!</strong> You successfully read this important alert
            message.
          </div>

          <div
            class="mt-2 mb-2 alert alert-dismissible fade show alert-primary"
            role="alert"
          >
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="alert"
              aria-label="Close"
            >
              <span aria-hidden="true" class="visually-hidden">×</span>
            </button>
            <!-- <button
              type="button"
              class="close"
              data-dismiss="alert"
              aria-label="Close"
            >
              <span aria-hidden="true">×</span>
            </button> -->
            <strong>Well done!</strong> You can dismiss this message with the X button.
          </div>

          <div class="mt-2 mb-2 alert alert-primary" role="alert">
            <h4 class="alert-heading">Well done!</h4>
            You successfully read this important alert message.
            <a href="#!" class="alert-link">It contains a link and heading.</a>
          </div>
        </div>
      </div>
      <!-- alerts -->

      <div>
        <a id="badges" class="ht-anchor">Badges</a>
        <h5 class="mt-4 mb-3">Badges</h5>

        <div class="mt-3">
          <span class="badge text-bg-primary">Primary</span>
          <span class="badge text-bg-secondary">Secondary</span>
          <span class="badge text-bg-success">Success</span>
          <span class="badge text-bg-danger">Danger</span>
          <span class="badge text-bg-warning">Warning</span>
          <span class="badge text-bg-info">Info</span>
          <span class="badge text-bg-light">Light</span>
          <span class="badge text-bg-dark">Dark</span>
        </div>

        <div class="mt-3">
          <span class="badge rounded-pill text-bg-primary">Primary</span>
          <span class="badge rounded-pill text-bg-secondary">Secondary</span>
          <span class="badge rounded-pill text-bg-success">Success</span>
          <span class="badge rounded-pill text-bg-danger">Danger</span>
          <span class="badge rounded-pill text-bg-warning">Warning</span>
          <span class="badge rounded-pill text-bg-info">Info</span>
          <span class="badge rounded-pill text-bg-light">Light</span>
          <span class="badge rounded-pill text-bg-dark">Dark</span>
        </div>
      </div>
      <!-- Badges -->

      <div>
        <a id="buttons" class="ht-anchor">Buttons</a>
        <h5 class="mt-4 mb-3">Buttons</h5>

        <div>
          <div class="mt-3">
            <div class="row">
              <div class="col-md-6">
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-primary"
                  >Default Button</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-primary"
                  ><span class="fa fa-download mr-2" />With Icon</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-primary"
                  ><span class="fa fa-download" /></a
                >
              </div>
              <div class="col-md-6">
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-outline-primary"
                  >Outline Button</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-outline-primary">
                  <span class="fa fa-download mr-2" /> With Icon</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-outline-primary">
                  <span class="fa fa-download" /></a
                >
              </div>
            </div>
          </div>

          <div class="mt-3">
            <div class="row">
              <div class="col-md-6">
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-primary">
                  <span class="fa fa-twitter mr-2" /> Tweet</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-primary">
                  <span class="fa fa-twitter" /></a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-primary">
                  <span class="fa fa-facebook mr-2" /> Share</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-primary">
                  <span class="fa fa-facebook" /></a
                >
              </div>
              <div class="col-md-6">
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-outline-primary">
                  <span class="fa fa-twitter mr-2" /> Tweet</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-outline-primary">
                  <span class="fa fa-twitter" /></a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-outline-primary">
                  <span class="fa fa-facebook mr-2" /> Share</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-outline-primary">
                  <span class="fa fa-facebook" /></a
                >
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-primary">
                  <span class="fa fa-instagram mr-2" /> Instagram</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-primary">
                  <span class="fa fa-instagram" /></a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-primary">
                  <span class="fa fa-github mr-2" /> Git</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-primary">
                  <span class="fa fa-github" /></a
                >
              </div>
              <div class="col-md-6">
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-outline-primary">
                  <span class="fa fa-instagram mr-2" /> Instagram</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-outline-primary">
                  <span class="fa fa-instagram" /></a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-outline-primary">
                  <span class="fa fa-github mr-2" /> Git</a
                >
                <a href="#!" class="mt-2 mb-2 btn btn-sm btn-outline-primary">
                  <span class="fa fa-github" /></a
                >
              </div>
            </div>
          </div>

          <div class="mt-3">
            <div class="row">
              <div class="col-md-6">
                <a href="#!" class="mt-2 mb-2 btn btn-block btn-sm btn-primary"
                  >Block level button</a
                >
              </div>
              <div class="col-md-6">
                <a
                  href="#!"
                  class="mt-2 mb-2 btn btn-block btn-sm btn-outline-primary"
                  >Block level button</a
                >
              </div>
            </div>
          </div>

          <h6 class="mt-3 mb-2">Dropdowns</h6>
          <div class="row">
            <div class="col-lg-6">
              <div class="d-flex">
                <div class="dropdown me-1">
                  <button
                    type="button"
                    class="btn btn-secondary dropdown-toggle"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                    data-bs-offset="10,20"
                  >
                    Offset
                  </button>
                  <ul class="dropdown-menu">
                    <li>
                      <a class="dropdown-item" href="#!">Action</a>
                    </li>
                    <li>
                      <a class="dropdown-item" href="#!">Another action</a>
                    </li>
                    <li>
                      <a class="dropdown-item" href="#!">Something else here</a>
                    </li>
                  </ul>
                </div>
                <div class="btn-group">
                  <button type="button" class="btn btn-secondary"
                    >Reference</button
                  >
                  <button
                    type="button"
                    class="btn btn-secondary dropdown-toggle dropdown-toggle-split"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                    data-bs-reference="parent"
                  >
                    <span class="visually-hidden">Toggle Dropdown</span>
                  </button>
                  <ul class="dropdown-menu">
                    <li>
                      <a class="dropdown-item" href="#!">Action</a>
                    </li>
                    <li>
                      <a class="dropdown-item" href="#!">Another action</a>
                    </li>
                    <li>
                      <a class="dropdown-item" href="#!">Something else here</a>
                    </li>
                    <li><hr class="dropdown-divider" /></li>
                    <li>
                      <a class="dropdown-item" href="#!">Separated link</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="col-lg-6">
              <div class="mt-3 mb-4">
                <div class="btn-group btn-group-sm">
                  <button
                    type="button"
                    class="btn dropdown-toggle btn-sm btn-outline-primary"
                    data-bs-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false"
                  >
                    Action
                  </button>
                  <div class="dropdown-menu">
                    <a class="dropdown-item" href="#!">Action</a>
                    <a class="dropdown-item" href="#!">Another action</a>
                    <a class="dropdown-item" href="#!">Something else here</a>
                    <div class="dropdown-divider" />
                    <a class="dropdown-item" href="#!">Separated link</a>
                  </div>
                </div>
                <div class="btn-group btn-group-sm">
                  <button type="button" class="btn btn-sm btn-outline-primary"
                    >Action</button
                  >
                  <button
                    type="button"
                    class="btn dropdown-toggle dropdown-toggle-split btn-sm btn-outline-primary"
                    data-bs-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false"
                  >
                    <span class="sr-only">Toggle Dropdown</span>
                  </button>
                  <div class="dropdown-menu">
                    <a class="dropdown-item" href="#!">Action</a>
                    <a class="dropdown-item" href="#!">Another action</a>
                    <a class="dropdown-item" href="#!">Something else here</a>
                    <div class="dropdown-divider" />
                    <a class="dropdown-item" href="#!">Separated link</a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <h6 class="mt-3 mb-2">Grouping them</h6>
          <div class="row">
            <div class="col-xl-6">
              <div class="mt-3 mb-4">
                <div class="btn-group" role="group" aria-label="Basic example">
                  <button type="button" class="btn btn-sm btn-primary"
                    >Left</button
                  >
                  <button type="button" class="btn btn-sm btn-primary"
                    >Middle</button
                  >
                  <button type="button" class="btn btn-sm btn-primary"
                    >Right</button
                  >
                </div>
              </div>

              <div class="mt-3 mb-4">
                <div class="btn-group" role="group" aria-label="Basic example">
                  <button type="button" class="btn btn-sm btn-primary">1</button
                  >
                  <button type="button" class="btn btn-sm btn-primary">2</button
                  >

                  <div class="btn-group" role="group">
                    <button
                      type="button"
                      class="btn btn-sm btn-primary dropdown-toggle"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                    >
                      Dropdown
                    </button>
                    <ul class="dropdown-menu">
                      <li>
                        <a class="dropdown-item" href="#!">Dropdown link</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#!">Dropdown link</a>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div>
                <div
                  class="btn-group-vertical btn-group-sm"
                  role="group"
                  aria-label="Basic example"
                >
                  <a href="#!" class="btn btn-primary">Seven</a>
                  <a href="#!" class="btn btn-primary">Eleven</a>
                </div>

                <div
                  class="btn-group-vertical btn-group-sm"
                  role="group"
                  aria-label="Basic example"
                >
                  <a href="#!" class="btn btn-primary">Seven</a>

                  <div class="btn-group" role="group">
                    <button
                      type="button"
                      class="btn btn-sm btn-primary dropdown-toggle"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                    >
                      Dropdown
                    </button>
                    <ul class="dropdown-menu">
                      <li>
                        <a class="dropdown-item" href="#!">Dropdown link</a>
                      </li>
                      <li>
                        <a class="dropdown-item" href="#!">Dropdown link</a>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-xl-6">
              <div class="mt-3 mb-4">
                <div class="btn-group btn-group-sm">
                  <a href="#!" class="btn btn-outline-primary">One</a>
                  <a href="#!" class="btn btn-outline-primary">Two</a>
                  <a href="#!" class="btn btn-outline-primary">Three</a>
                </div>
              </div>
              <div class="mt-3 mb-4">
                <div
                  class="btn-group btn-group-sm"
                  role="group"
                  aria-label="Basic example"
                >
                  <a href="#!" class="btn btn-outline-primary">One</a>
                  <a href="#!" class="btn btn-outline-primary">Two</a>

                  <div class="btn-group btn-group-sm" role="group">
                    <button
                      id="btnGroupDrop1"
                      type="button"
                      class="btn dropdown-toggle btn-outline-primary"
                      data-bs-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="false"
                    >
                      Dropdown
                    </button>
                    <div class="dropdown-menu" aria-labelledby="btnGroupDrop1">
                      <a class="dropdown-item" href="#!">Dropdown link</a>
                      <a class="dropdown-item" href="#!">Dropdown link</a>
                    </div>
                  </div>
                </div>
              </div>
              <div class="mt-3 mb-4">
                <div
                  class="btn-group-vertical btn-group-sm"
                  role="group"
                  aria-label="Basic example"
                >
                  <a href="#!" class="btn btn-outline-primary">Seven</a>
                  <a href="#!" class="btn btn-outline-primary">Eleven</a>
                </div>

                <div
                  class="btn-group-vertical btn-group-sm"
                  role="group"
                  aria-label="Basic example"
                >
                  <a href="#!" class="btn btn-outline-primary">Seven</a>

                  <div class="btn-group btn-group-sm" role="group">
                    <button
                      id="btnGroupDrop2"
                      type="button"
                      class="btn dropdown-toggle btn-outline-primary"
                      data-bs-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="false"
                    >
                      Dropdown
                    </button>
                    <div class="dropdown-menu" aria-labelledby="btnGroupDrop2">
                      <a class="dropdown-item" href="#!">Dropdown link</a>
                      <a class="dropdown-item" href="#!">Dropdown link</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <h6 class="mt-3">Checkboxes and Radios</h6>
          <div class="row">
            <div class="col-xl-6">
              <div class="mt-3 mb-4">
                <div
                  class="btn-group btn-group-toggle btn-group-sm"
                  data-toggle="buttons"
                >
                  <label class="btn active btn-sm btn-primary">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      checked
                      autocomplete="off"
                    /> Checkbox 1
                  </label>
                  <label class="btn btn-sm btn-primary">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      autocomplete="off"
                    /> Checkbox 2
                  </label>
                </div>
                <div
                  class="btn-group btn-group-toggle btn-group-sm"
                  data-toggle="buttons"
                >
                  <label class="btn active btn-sm btn-primary">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="options"
                      id="option-1"
                      autocomplete="off"
                      checked
                    /> Radio 1
                  </label>
                  <label class="btn btn-sm btn-primary">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="options"
                      id="option-2"
                      autocomplete="off"
                    /> Radio 2
                  </label>
                </div>
              </div>
            </div>
            <div class="col-xl-6">
              <div class="mt-3 mb-4">
                <div
                  class="btn-group btn-group-toggle btn-group-sm"
                  data-toggle="buttons"
                >
                  <label class="btn active btn-sm btn-outline-primary">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      checked
                      autocomplete="off"
                    /> Checkbox 1
                  </label>
                  <label class="btn btn-sm btn-outline-primary">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      autocomplete="off"
                    /> Checkbox 2
                  </label>
                </div>
                <div
                  class="btn-group btn-group-toggle btn-group-sm"
                  data-toggle="buttons"
                >
                  <label class="btn active btn-sm btn-outline-primary">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="options"
                      id="radio-option-1"
                      autocomplete="off"
                      checked
                    /> Radio 1
                  </label>
                  <label class="btn btn-sm btn-outline-primary">
                    <input
                      class="form-check-input"
                      type="radio"
                      name="options"
                      id="radio-option-2"
                      autocomplete="off"
                    /> Radio 2
                  </label>
                </div>
              </div>
            </div>
            <div class="col-xl-6">
              <div class="mt-3 mb-4">
                <div class="form-check form-switch">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    role="switch"
                    id="flexSwitchCheckDefault"
                  />
                  <label class="form-check-label" for="flexSwitchCheckDefault"
                    >Default switch checkbox input</label
                  >
                </div>
                <div class="form-check form-switch">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    role="switch"
                    id="flexSwitchCheckChecked"
                    checked
                  />
                  <label class="form-check-label" for="flexSwitchCheckChecked"
                    >Checked switch checkbox input</label
                  >
                </div>
                <div class="form-check form-switch">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    role="switch"
                    id="flexSwitchCheckDisabled"
                    disabled
                  />
                  <label class="form-check-label" for="flexSwitchCheckDisabled"
                    >Disabled switch checkbox input</label
                  >
                </div>
                <div class="form-check form-switch">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    role="switch"
                    id="flexSwitchCheckCheckedDisabled"
                    checked
                    disabled
                  />
                  <label
                    class="form-check-label"
                    for="flexSwitchCheckCheckedDisabled"
                    >Disabled checked switch checkbox input</label
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- buttons -->

      <div>
        <a id="cards" class="ht-anchor">Cards</a>
        <h5 class="mt-4 mb-3">Cards</h5>

        <div class="row">
          <div class="col-lg-6">
            <div class="mt-3 mb-4">
              <div class="card mb-3 text-center bg-primary text-white">
                <div class="card-body">
                  <blockquote class="card-blockquote">
                    <p>
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                      Integer posuere erat a ante. Integer posuere erat a ante.
                    </p>
                    <footer>
                      Someone famous in <cite title="Source Title"
                        >Source Title</cite
                      >
                    </footer>
                  </blockquote>
                </div>
              </div>
            </div>

            <div class="mt-3 mb-4">
              <div class="card">
                <img
                  class="card-img-top"
                  src="image1.jpg"
                  alt="Card image cap"
                />
                <div class="card-body">
                  <h4 class="card-title">Card title</h4>
                  <p class="card-text">
                    Some quick example text to build on the card title and make
                    up the bulk of the card's content.
                  </p>
                  <a href="#!" class="btn btn-sm btn-primary">Go somewhere</a>
                </div>
              </div>
            </div>

            <div class="mt-3 mb-4">
              <div class="card">
                <div class="card-header">Quote</div>
                <div class="card-body">
                  <blockquote class="card-blockquote">
                    <p>
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                      Integer posuere erat a ante.
                    </p>
                    <footer>
                      Someone famous in <cite title="Source Title"
                        >Source Title</cite
                      >
                    </footer>
                  </blockquote>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="mt-3 mb-4">
              <div class="card mb-3 text-center border-primary">
                <div class="card-body">
                  <blockquote class="card-blockquote">
                    <p>
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                      Integer posuere erat a ante.
                    </p>
                    <footer>
                      Someone famous in <cite title="Source Title"
                        >Source Title</cite
                      >
                    </footer>
                  </blockquote>
                </div>
              </div>
            </div>

            <div class="mt-3 mb-4">
              <div class="card text-center">
                <div class="card-header">Featured</div>
                <div class="card-body">
                  <h4 class="card-title">Special title treatment</h4>
                  <p class="card-text">
                    With supporting text below as a natural lead-in to
                    additional content.
                  </p>
                  <a href="#!" class="btn btn-sm btn-primary">Go somewhere</a>
                </div>
                <div class="card-footer text-muted">2 days ago</div>
              </div>
            </div>

            <div class="mt-3 mb-4">
              <div class="card">
                <img
                  class="card-img-top"
                  src="image2.jpg"
                  alt="Card image cap"
                />
                <ul class="list-group list-group-flush">
                  <li class="list-group-item list-group-item-action">
                    Cras justo odio
                  </li>
                  <li class="list-group-item list-group-item-action">
                    Dapibus ac facilisis in
                  </li>
                  <li class="list-group-item list-group-item-action">
                    Vestibulum at eros
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-3 mb-4">
          <div class="card text-center">
            <div class="card-header">
              <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item">
                  <a class="nav-link active" aria-current="true" href="#!"
                    >Active</a
                  >
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#!">Link</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link disabled" aria-disabled="true" href="#!"
                    >Disabled</a
                  >
                </li>
              </ul>
            </div>
            <div class="card-body">
              <h5 class="card-title">Special title treatment</h5>
              <p class="card-text">
                With supporting text below as a natural lead-in to additional
                content.
              </p>
              <a href="#!" class="btn btn-primary">Go somewhere</a>
            </div>
          </div>
        </div>
        <!-- cards -->

        <div>
          <a id="carousel" class="ht-anchor">Carousel</a>
          <h5 class="mt-4 mb-3">Carousel</h5>

          <div
            id="carouselExampleRide"
            class="carousel slide"
            data-bs-ride="true"
          >
            <div class="carousel-inner">
              <div class="carousel-item active">
                <img
                  src="image1.jpg"
                  class="d-block img-fluid mx-auto w-50"
                  alt="..."
                />
              </div>
              <div class="carousel-item">
                <img
                  src="image2.jpg"
                  class="d-block img-fluid mx-auto w-50"
                  alt="..."
                />
              </div>
            </div>
            <button
              class="carousel-control-prev"
              type="button"
              data-bs-target="#carouselExampleRide"
              data-bs-slide="prev"
            >
              <span class="carousel-control-prev-icon" aria-hidden="true" />
              <span class="visually-hidden">Previous</span>
            </button>
            <button
              class="carousel-control-next"
              type="button"
              data-bs-target="#carouselExampleRide"
              data-bs-slide="next"
            >
              <span class="carousel-control-next-icon" aria-hidden="true" />
              <span class="visually-hidden">Next</span>
            </button>
          </div>
        </div>
        <!-- carousel -->

        <div>
          <a id="forms" class="ht-anchor">Forms</a>
          <h5 class="mt-4 mb-3">Forms</h5>

          <div class="row">
            <div class="col-xl-6">
              <div class="card">
                <div class="card-body">
                  <h6 class="card-title">Start with a small group form</h6>
                  <div>
                    <form>
                      <div class="form-group">
                        <label for="exampleInputEmail1">Email address</label>
                        <input
                          type="email"
                          class="form-control form-control-sm"
                          id="exampleInputEmail1"
                          aria-describedby="emailHelp"
                          placeholder="Enter email"
                        />
                        <small id="emailHelp" class="form-text text-muted"
                          >We'll never share your email</small
                        >
                      </div>
                      <button type="submit" class="btn btn-sm btn-primary"
                        >Submit</button
                      >
                    </form>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-xl-6">
              <div class="card">
                <div class="card-body ht-tm-superspecialcardcheat">
                  <h6 class="card-title">Or with an inline form</h6>

                  <div class="mt-3">
                    <form class="row row-cols-lg-auto g-3 align-items-center">
                      <div class="col-12">
                        <label
                          class="visually-hidden"
                          for="inlineFormInputGroupUsername">Username</label
                        >
                        <div class="input-group">
                          <div class="input-group-text">@</div>
                          <input
                            type="text"
                            class="form-control"
                            id="inlineFormInputGroupUsername"
                            placeholder="Username"
                          />
                        </div>
                      </div>

                      <div class="col-12">
                        <div class="form-check">
                          <input
                            class="form-check-input"
                            type="checkbox"
                            id="inlineFormCheck"
                          />
                          <label class="form-check-label" for="inlineFormCheck">
                            Remember me
                          </label>
                        </div>
                      </div>

                      <div class="col-12">
                        <button type="submit" class="btn btn-primary"
                          >Submit</button
                        >
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-3">
            <div class="row mb-4">
              <div class="col-xl-6">
                <div class="card">
                  <div class="card-body">
                    <form autocomplete="off">
                      <h6 class="card-title">Add some extras too..</h6>

                      <div class="mt-2 mb-2 mt-2 mb-2-inner">
                        <input
                          class="form-control form-control-sm"
                          type="text"
                          value="Text input"
                          id="example-text-input"
                        />
                      </div>

                      <div class="mt-2 mb-2 mt-2 mb-2-inner">
                        <input
                          class="form-control form-control-sm"
                          type="email"
                          value="email@example.com"
                          id="example-email-input"
                        />
                      </div>

                      <div class="mt-2 mb-2 mt-2 mb-2-inner">
                        <input
                          class="form-control form-control-sm"
                          type="url"
                          value="https://getbootstrap.com"
                          id="example-url-input"
                        />
                      </div>

                      <div class="mt-2 mb-2 mt-2 mb-2-inner">
                        <input
                          class="form-control form-control-sm"
                          type="date"
                          value="2011-08-19"
                          id="example-date-input"
                        />
                      </div>

                      <div class="mt-2 mb-2 mt-2 mb-2-inner">
                        <input
                          class="form-control form-control-sm"
                          type="password"
                          value="hunter2"
                          id="example-password-input"
                        />
                      </div>

                      <div class="mt-2 mb-2 mt-2 mb-2-inner">
                        <input
                          class="form-control form-control-sm"
                          type="number"
                          value="42"
                          id="example-number-input"
                        />
                      </div>
                    </form>
                  </div>
                </div>
              </div>
              <div class="col-xl-6">
                <div class="card">
                  <div class="card-body">
                    <h6 class="card-title">Even more form controls</h6>
                    <div class="mt-3">
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="flexCheckDefault"
                        />
                        <label class="form-check-label" for="flexCheckDefault">
                          Default checkbox
                        </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value=""
                          id="flexCheckChecked"
                          checked
                        />
                        <label class="form-check-label" for="flexCheckChecked">
                          Checked checkbox
                        </label>
                      </div>
                    </div>

                    <div class="mt-3">
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="radio"
                          name="flexRadioDefault"
                          id="flexRadioDefault1"
                        />
                        <label class="form-check-label" for="flexRadioDefault1">
                          Default radio
                        </label>
                      </div>
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="radio"
                          name="flexRadioDefault"
                          id="flexRadioDefault2"
                          checked
                        />
                        <label class="form-check-label" for="flexRadioDefault2">
                          Default checked radio
                        </label>
                      </div>
                    </div>

                    <div class="mt-3">
                      <div class="d-inline-block">
                        <div class="form-floating">
                          <select
                            class="form-select"
                            id="floatingSelect"
                            aria-label="Floating label select example"
                          >
                            <option selected>Open this select menu</option>
                            <option value="1">One</option>
                            <option value="2">Two</option>
                            <option value="3">Three</option>
                          </select>
                          <label for="floatingSelect">Works with selects</label>
                        </div>
                      </div>
                    </div>

                    <div class="mt-3">
                      <div>
                        <label for="formFile" class="form-label"
                          >Default file input example</label
                        >
                        <input class="form-control" type="file" id="formFile" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="row mb-4">
            <div class="col-xl-6">
              <div class="mt-3">
                <div class="input-group input-group-sm mb-3">
                  <button
                    class="btn btn-primary"
                    type="button"
                    id="button-addon1">Button</button
                  >
                  <input
                    type="text"
                    class="form-control"
                    placeholder=""
                    aria-label="Example text with button addon"
                    aria-describedby="button-addon1"
                  />
                </div>

                <div class="input-group input-group-sm mb-3">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="Recipient's username"
                    aria-label="Recipient's username"
                    aria-describedby="button-addon2"
                  />
                  <button
                    class="btn btn-primary"
                    type="button"
                    id="button-addon2">Button</button
                  >
                </div>

                <div class="input-group input-group-sm mb-3">
                  <button class="btn btn-primary" type="button">Button</button>
                  <button class="btn btn-primary" type="button">Button</button>
                  <input
                    type="text"
                    class="form-control"
                    placeholder=""
                    aria-label="Example text with two button addons"
                  />
                </div>

                <div class="input-group input-group-sm mb-3">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="Recipient's username"
                    aria-label="Recipient's username with two button addons"
                  />
                  <button class="btn btn-primary" type="button">Button</button>
                  <button class="btn btn-primary" type="button">Button</button>
                </div>

                <div class="input-group input-group-sm mb-3">
                  <button
                    class="btn btn-primary dropdown-toggle"
                    type="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false">Dropdown</button
                  >
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#!">Action</a></li>
                    <li>
                      <a class="dropdown-item" href="#!">Another action</a>
                    </li>
                    <li>
                      <a class="dropdown-item" href="#!">Something else here</a>
                    </li>
                    <li><hr class="dropdown-divider" /></li>
                    <li>
                      <a class="dropdown-item" href="#!">Separated link</a>
                    </li>
                  </ul>
                  <input
                    type="text"
                    class="form-control"
                    aria-label="Text input with dropdown button"
                  />
                </div>

                <div class="input-group input-group-sm mb-3">
                  <input
                    type="text"
                    class="form-control"
                    aria-label="Text input with dropdown button"
                  />
                  <button
                    class="btn btn-primary dropdown-toggle"
                    type="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false">Dropdown</button
                  >
                  <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="#!">Action</a></li>
                    <li>
                      <a class="dropdown-item" href="#!">Another action</a>
                    </li>
                    <li>
                      <a class="dropdown-item" href="#!">Something else here</a>
                    </li>
                    <li><hr class="dropdown-divider" /></li>
                    <li>
                      <a class="dropdown-item" href="#!">Separated link</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="col-xl-6">
              <div class="mt-3">
                <div class="input-group input-group-sm mb-3">
                  <button
                    class="btn btn-outline-primary"
                    type="button"
                    id="button-addon1">Button</button
                  >
                  <input
                    type="text"
                    class="form-control"
                    placeholder=""
                    aria-label="Example text with button addon"
                    aria-describedby="button-addon1"
                  />
                </div>

                <div class="input-group input-group-sm mb-3">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="Recipient's username"
                    aria-label="Recipient's username"
                    aria-describedby="button-addon2"
                  />
                  <button
                    class="btn btn-outline-primary"
                    type="button"
                    id="button-addon2">Button</button
                  >
                </div>

                <div class="input-group input-group-sm mb-3">
                  <button class="btn btn-outline-primary" type="button"
                    >Button</button
                  >
                  <button class="btn btn-outline-primary" type="button"
                    >Button</button
                  >
                  <input
                    type="text"
                    class="form-control"
                    placeholder=""
                    aria-label="Example text with two button addons"
                  />
                </div>

                <div class="input-group input-group-sm mb-3">
                  <input
                    type="text"
                    class="form-control"
                    placeholder="Recipient's username"
                    aria-label="Recipient's username with two button addons"
                  />
                  <button class="btn btn-outline-primary" type="button"
                    >Button</button
                  >
                  <button class="btn btn-outline-primary" type="button"
                    >Button</button
                  >
                </div>

                <div class="input-group input-group-sm mb-3">
                  <button
                    class="btn btn-outline-primary dropdown-toggle"
                    type="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false">Dropdown</button
                  >
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#!">Action</a></li>
                    <li>
                      <a class="dropdown-item" href="#!">Another action</a>
                    </li>
                    <li>
                      <a class="dropdown-item" href="#!">Something else here</a>
                    </li>
                    <li><hr class="dropdown-divider" /></li>
                    <li>
                      <a class="dropdown-item" href="#!">Separated link</a>
                    </li>
                  </ul>
                  <input
                    type="text"
                    class="form-control"
                    aria-label="Text input with dropdown button"
                  />
                </div>

                <div class="input-group input-group-sm mb-3">
                  <input
                    type="text"
                    class="form-control"
                    aria-label="Text input with dropdown button"
                  />
                  <button
                    class="btn btn-outline-primary dropdown-toggle"
                    type="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false">Dropdown</button
                  >
                  <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="#!">Action</a></li>
                    <li>
                      <a class="dropdown-item" href="#!">Another action</a>
                    </li>
                    <li>
                      <a class="dropdown-item" href="#!">Something else here</a>
                    </li>
                    <li><hr class="dropdown-divider" /></li>
                    <li>
                      <a class="dropdown-item" href="#!">Separated link</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- forms -->

        <div>
          <a id="jumbotron" class="ht-anchor">Jumbotron</a>
          <h5 class="mt-4 mb-3">Jumbotron</h5>

          <div class="mt-3">
            <div class="p-5 mb-4 bg-body-tertiary rounded-3">
              <div class="container-fluid py-5">
                <h1 class="display-5 fw-bold">Custom jumbotron</h1>
                <p class="col-md-8 fs-4">
                  Using a series of utilities, you can create this jumbotron,
                  just like the one in previous versions of Bootstrap. Check out
                  the examples below for how you can remix and restyle it to
                  your liking.
                </p>
                <button class="btn btn-primary btn-lg" type="button"
                  >Example button</button
                >
              </div>
            </div>
          </div>
        </div>
        <!-- jumbotron -->

        <div>
          <a id="lists" class="ht-anchor">Lists</a>
          <h5 class="mt-4 mb-3">Lists</h5>

          <div class="row">
            <div class="col-xl-6">
              <div class="mt-3">
                <ul class="list-group mt-2 mb-2">
                  <li class="list-group-item">Cras justo odio</li>
                  <li class="list-group-item">Dapibus ac facilisis in</li>
                  <li class="list-group-item">Porta ac consectetur ac</li>
                  <li class="list-group-item justify-content-between">
                    Cras justo odio <span
                      class="badge rounded-pill text-bg-primary">14</span
                    >
                  </li>
                  <li class="list-group-item">Vestibulum at eros</li>
                  <li class="list-group-item list-group-item-primary">
                    Dapibus ac facilisis in
                  </li>
                </ul>
              </div>
            </div>
            <div class="col-xl-6">
              <div class="mt-3">
                <div class="list-group mt-2 mb-2">
                  <a href="#!" class="list-group-item active">
                    Cras justo odio
                  </a>
                  <a href="#!" class="list-group-item list-group-item-action"
                    >Dapibus ac facilisis in</a
                  >
                  <a href="#!" class="list-group-item list-group-item-action"
                    >Morbi leo risus</a
                  >
                  <a
                    href="#!"
                    class="list-group-item list-group-item-action justify-content-between"
                  >
                    Cras justo odio <span
                      class="badge rounded-pill text-bg-primary">14</span
                    >
                  </a>
                  <a href="#!" class="list-group-item list-group-item-action"
                    >Porta ac consectetur ac</a
                  >
                  <a
                    href="#!"
                    class="list-group-item list-group-item-action list-group-item-primary"
                    >Vestibulum at eros</a
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- lists -->

        <div>
          <a id="navigation" class="ht-anchor">Navigation</a>
          <h5 class="mt-4 mb-3">Navigation</h5>

          <div class="row">
            <div class="col-lg-6">
              <div class="mt-3">
                <ul class="nav nav-tabs mt-2 mb-2">
                  <li class="nav-item">
                    <a class="nav-link active" href="#!">Active</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" href="#!">Link</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" href="#!">Link</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link disabled" href="#!">Disabled</a>
                  </li>
                </ul>
              </div>
              <div class="mt-3">
                <ul
                  class="nav nav-underline mt-2 mb-2"
                  style="font-family: Roboto;font-weight: 400;text-transform: uppercase;"
                >
                  <li class="nav-item">
                    <a class="nav-link px-3 active" href="#!">Active</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link px-3" href="#!">Link</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link px-3" href="#!">Link</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link px-3 disabled" href="#!">Disabled</a>
                  </li>
                </ul>
              </div>
            </div>
            <div class="col-lg-6">
              <div class="mt-3">
                <ul class="nav nav-pills mt-2 mb-2">
                  <li class="nav-item">
                    <a class="nav-link active" href="#!">Active</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" href="#!">Link</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" href="#!">Link</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link disabled" href="#!">Disabled</a>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <div class="mt-3 mb-4">
            <nav class="navbar navbar-expand-lg bg-body-tertiary">
              <div class="container-fluid">
                <a class="navbar-brand" href="#/">Navbar</a>
                <button
                  class="navbar-toggler"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#navbarNavDropdown"
                  aria-controls="navbarNavDropdown"
                  aria-expanded="false"
                  aria-label="Toggle navigation"
                >
                  <span class="navbar-toggler-icon" />
                </button>
                <div class="collapse navbar-collapse" id="navbarNavDropdown">
                  <ul class="navbar-nav">
                    <li class="nav-item">
                      <a class="nav-link active" aria-current="page" href="#/"
                        >Home</a
                      >
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" href="#/">Features</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" href="#/">Pricing</a>
                    </li>
                    <li class="nav-item dropdown">
                      <a
                        class="nav-link dropdown-toggle"
                        href="#/"
                        role="button"
                        data-bs-toggle="dropdown"
                        aria-expanded="false"
                      >
                        Dropdown link
                      </a>
                      <ul class="dropdown-menu">
                        <li>
                          <a class="dropdown-item" href="#/">Action</a>
                        </li>
                        <li>
                          <a class="dropdown-item" href="#/">Another action</a>
                        </li>
                        <li>
                          <a class="dropdown-item" href="#/"
                            >Something else here</a
                          >
                        </li>
                      </ul>
                    </li>
                  </ul>
                </div>
                <div class="d-flex">
                  <div class="input-group">
                    <input
                      class="form-control"
                      type="search"
                      placeholder="Search"
                      aria-label="Search"
                    />
                    <button
                      class="input-group-text btn btn-outline-primary"
                      type="submit">Search</button
                    >
                  </div>
                </div>
              </div>
            </nav>
          </div>
        </div>
        <!-- navigation -->

        <div>
          <a id="pagination" class="ht-anchor">Pagination</a>
          <h5 class="mt-4 mb-3">Pagination</h5>

          <div class="row">
            <div class="col-xl-6">
              <div class="mt-3 mt-2 mb-2 mt-2 mb-2-inner">
                <nav aria-label="Page navigation example">
                  <ul class="pagination pagination-sm">
                    <li class="page-item">
                      <a class="page-link" href="#!">Previous</a>
                    </li>
                    <li class="page-item">
                      <a class="page-link" href="#!">1</a>
                    </li>
                    <li class="page-item active">
                      <a class="page-link" href="#!">2</a>
                    </li>
                    <li class="page-item">
                      <a class="page-link" href="#!">3</a>
                    </li>
                    <li class="page-item">
                      <a class="page-link" href="#!">Next</a>
                    </li>
                  </ul>
                </nav>
              </div>
              <div class="mt-3 mt-2 mb-2 mt-2 mb-2-inner">
                <nav aria-label="Page navigation example">
                  <ul class="pagination pagination-sm">
                    <li class="page-item">
                      <a class="page-link rounded border-0" href="#!"
                        >« Previous</a
                      >
                    </li>
                    <li class="page-item">
                      <a class="page-link rounded border-0" href="#!">1</a>
                    </li>
                    <li class="page-item active">
                      <a class="page-link rounded border-0" href="#!">2</a>
                    </li>
                    <li class="page-item">
                      <a class="page-link rounded border-0" href="#!">3</a>
                    </li>
                    <li class="page-item">
                      <a class="page-link rounded border-0" href="#!">Next »</a>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
            <div class="col-xl-6">
              <div class="mt-3 mt-2 mb-2 mt-2 mb-2-inner">
                <nav aria-label="...">
                  <ul class="pagination pagination-sm">
                    <li class="page-item disabled">
                      <span class="page-link">Previous</span>
                    </li>
                    <li class="page-item">
                      <a class="page-link" href="#!">1</a>
                    </li>
                    <li class="page-item active">
                      <span class="page-link">
                        2 <span class="sr-only">(current)</span>
                      </span>
                    </li>
                    <li class="page-item">
                      <a class="page-link" href="#!">3</a>
                    </li>
                    <li class="page-item">
                      <a class="page-link" href="#!">Next</a>
                    </li>
                  </ul>
                </nav>
              </div>
              <div class="mt-3 mt-2 mb-2 mt-2 mb-2-inner">
                <nav aria-label="Page navigation example">
                  <ul class="pagination pagination-sm">
                    <li class="page-item disabled">
                      <a
                        class="page-link rounded border-0 bg-transparent"
                        href="#!">« Previous</a
                      >
                    </li>
                    <li class="page-item">
                      <a class="page-link rounded border-0" href="#!">1</a>
                    </li>
                    <li class="page-item active">
                      <a class="page-link rounded border-0" href="#!">2</a>
                    </li>
                    <li class="page-item">
                      <a class="page-link rounded border-0" href="#!">3</a>
                    </li>
                    <li class="page-item">
                      <a class="page-link rounded border-0" href="#!">Next »</a>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
        <!-- pagination -->

        <div class="">
          <a id="popovers" class="ht-anchor">Popovers</a>
          <h5 class="mt-4 mb-3">Popovers</h5>

          <div class="mt-3">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-container="body"
              data-bs-toggle="popover"
              data-bs-placement="top"
              data-bs-content="Top popover"
            >
              Popover on top
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-container="body"
              data-bs-toggle="popover"
              data-bs-placement="right"
              data-bs-content="Right popover"
            >
              Popover on right
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-container="body"
              data-bs-toggle="popover"
              data-bs-placement="bottom"
              data-bs-content="Bottom popover"
            >
              Popover on bottom
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-container="body"
              data-bs-toggle="popover"
              data-bs-placement="left"
              data-bs-content="Left popover"
            >
              Popover on left
            </button>
          </div>
        </div>
        <!-- popovers -->

        <div>
          <a id="progress" class="ht-anchor">Progress</a>
          <h5 class="mt-4 mb-3">Progress</h5>

          <div class="mt-3">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar bg-primary"
                role="progressbar"
                aria-valuenow="0"
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>
          <div class="mt-3">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar bg-primary"
                role="progressbar"
                style="width: 25%"
                aria-valuenow="25"
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>
          <div class="mt-3">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar bg-primary"
                role="progressbar"
                style="width: 50%"
                aria-valuenow="50"
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>
          <div class="mt-3">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar bg-primary"
                role="progressbar"
                style="width: 75%"
                aria-valuenow="75"
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>
          <div class="mt-3">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar bg-primary"
                role="progressbar"
                style="width: 100%"
                aria-valuenow="100"
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>

          <div class="mt-3 mt-5">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar progress-bar-striped bg-primary"
                role="progressbar"
                aria-valuenow="0"
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>
          <div class="mt-3">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar progress-bar-striped bg-primary"
                role="progressbar"
                style="width: 25%"
                aria-valuenow="25"
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>
          <div class="mt-3">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar progress-bar-striped bg-primary"
                role="progressbar"
                style="width: 50%"
                aria-valuenow="50"
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>
          <div class="mt-3">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar progress-bar-striped bg-primary"
                role="progressbar"
                style="width: 75%"
                aria-valuenow="75"
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>
          <div class="mt-3">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar progress-bar-striped bg-primary"
                role="progressbar"
                style="width: 100%"
                aria-valuenow="100"
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>

          <div class="mt-3 mt-5">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar progress-bar-striped progress-bar-animated bg-primary"
                role="progressbar"
                aria-valuenow="75"
                aria-valuemin="0"
                aria-valuemax="100"
                style="width: 75%"
              />
            </div>
          </div>

          <div class="my-5">
            <div class="progress mt-2 mb-2">
              <div
                class="progress-bar"
                role="progressbar"
                style="width: 15%"
                aria-valuenow="15"
                aria-valuemin="0"
                aria-valuemax="100"
              />
              <div
                class="progress-bar bg-success"
                role="progressbar"
                style="width: 30%"
                aria-valuenow="30"
                aria-valuemin="0"
                aria-valuemax="100"
              />
              <div
                class="progress-bar bg-info"
                role="progressbar"
                style="width: 20%"
                aria-valuenow="20"
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>
        </div>
        <!-- progress -->

        <div>
          <a id="tables" class="ht-anchor">Tables</a>
          <h5 class="mt-4 mb-3">Tables</h5>

          <div class="mt-3">
            <table class="table table-striped table-hover table-borderless">
              <thead class="thead-dark">
                <tr>
                  <th>#</th>
                  <th>First Name</th>
                  <th>Last Name</th>
                  <th>Username</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">1</th>
                  <td>Mark</td>
                  <td>Otto</td>
                  <td>@mdo</td>
                </tr>
                <tr>
                  <th scope="row">2</th>
                  <td>Jacob</td>
                  <td>Thornton</td>
                  <td>@fat</td>
                </tr>

                <tr>
                  <th scope="row">3</th>
                  <td>Contextual</td>
                  <td>Row</td>
                  <td>@hackerthemes</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="mt-3">
            <table class="table table-hover">
              <thead class="thead-dark">
                <tr>
                  <th>#</th>
                  <th>First Name</th>
                  <th>Last Name</th>
                  <th>Username</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">1</th>
                  <td>Mark</td>
                  <td>Otto</td>
                  <td>@mdo</td>
                </tr>
                <tr>
                  <th scope="row">2</th>
                  <td>Jacob</td>
                  <td>Thornton</td>
                  <td>@fat</td>
                </tr>

                <tr>
                  <th scope="row">3</th>
                  <td>Contextual</td>
                  <td>Row</td>
                  <td>@hackerthemes</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="mt-3 mt-4">
            <table class="table table-striped table-primary table-hover">
              <thead>
                <tr>
                  <th>#</th>
                  <th>First Name</th>
                  <th>Last Name</th>
                  <th>Username</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">1</th>
                  <td>Mark</td>
                  <td>Otto</td>
                  <td>@mdo</td>
                </tr>
                <tr>
                  <th scope="row">2</th>
                  <td>Jacob</td>
                  <td>Thornton</td>
                  <td>@fat</td>
                </tr>
                <tr class="bg-primary">
                  <th scope="row">3</th>
                  <td colspan="2">Contextual Row</td>
                  <td>@hackerthemes</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <!-- tables -->

        <div>
          <a id="tooltips" class="ht-anchor">Tooltips</a>
          <h5 class="mt-4 mb-3">Tooltips</h5>

          <div class="mt-3">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              data-bs-title="Tooltip on top"
            >
              Tooltip on top
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-toggle="tooltip"
              data-bs-placement="right"
              data-bs-title="Tooltip on right"
            >
              Tooltip on right
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-toggle="tooltip"
              data-bs-placement="bottom"
              data-bs-title="Tooltip on bottom"
            >
              Tooltip on bottom
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-toggle="tooltip"
              data-bs-placement="left"
              data-bs-title="Tooltip on left"
            >
              Tooltip on left
            </button>
          </div>
        </div>
        <!-- tooltips -->

        <div>
          <a id="typography" class="ht-anchor">Typography</a>
          <h5 class="mt-4 mb-3">Typography</h5>

          <div class="row">
            <div class="col-xl-12">
              <div class="mt-3">
                <h1 class="display-1 mt-2 mb-2">Display 1</h1>
                <h1 class="display-2 mt-2 mb-2">Display 2</h1>
                <h1 class="display-3 mt-2 mb-2">Display 3</h1>
                <h1 class="display-4 mt-2 mb-2">Display 4</h1>
              </div>
              <div class="mt-3">
                <div class="mt-2 mb-2 mt-2 mb-2-inner">
                  <h1>h1. Bootstrap heading</h1>
                </div>
                <div class="mt-2 mb-2 mt-2 mb-2-inner">
                  <h2>h2. Bootstrap heading</h2>
                </div>
                <div class="mt-2 mb-2 mt-2 mb-2-inner">
                  <h3>h3. Bootstrap heading</h3>
                </div>
                <div class="mt-2 mb-2 mt-2 mb-2-inner">
                  <h4>h4. Bootstrap heading</h4>
                </div>
                <div class="mt-2 mb-2 mt-2 mb-2-inner">
                  <h5>h5. Bootstrap heading</h5>
                </div>
                <div class="mt-2 mb-2 mt-2 mb-2-inner">
                  <h6>h6. Bootstrap heading</h6>
                </div>
              </div>
              <div class="mt-3">
                <p class="lead mt-2 mb-2">
                  Lead Text - Vivamus sagittis lacus vel augue laoreet rutrum
                  faucibus dolor auctor. Duis mollis, est non commodo luctus.
                </p>
              </div>
              <div class="mt-3">
                <div class="mt-2 mb-2 mt-2 mb-2-inner">
                  <h6>Body text</h6>
                  <p>
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                    Ad, cumque delectus deleniti dolor esse ex fugiat, id in
                    ipsum modi molestiae mollitia, nulla numquam provident quasi
                    soluta sunt tempora vel. Lorem ipsum dolor sit amet,
                    consectetur adipisicing elit. Accusamus, aspernatur
                    consequuntur cumque dolor ducimus earum eos, expedita, fuga
                    harum incidunt maxime modi mollitia numquam praesentium
                    sapiente suscipit temporibus ut vero. Lorem ipsum dolor sit
                    amet, consectetur adipisicing elit. Amet nam nostrum
                    pariatur praesentium tempore. Ad architecto at aut dicta
                    enim, eveniet expedita libero magnam minus, nihil, non sequi
                    sunt voluptates!
                  </p>
                </div>
              </div>
            </div>

            <div class="col-xl-6">
              <div class="mt-3">
                <blockquote class="blockquote mt-2 mb-2">
                  <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    Integer posuere erat a ante.
                  </p>
                </blockquote>
              </div>
            </div>
            <div class="col-xl-6">
              <blockquote class="blockquote blockquote-reverse mt-2 mb-2">
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Integer posuere erat a ante.
                </p>
                <footer class="blockquote-footer">
                  Someone famous in <cite title="Source Title"
                    >Source Title</cite
                  >
                </footer>
              </blockquote>
            </div>
          </div>
        </div>
        <!-- typography -->
      </div>
    </div>
  </div>
</main>

<style>
  a.ht-anchor {
    display: block;
    position: relative;
    top: -50px;
    height: 1px;
    visibility: hidden;
  }
</style>
