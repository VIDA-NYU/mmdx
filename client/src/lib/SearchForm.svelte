<script>
	/**
	 * Specify the input value
	 */
	export let value = "";

	/**
	 * Set to `true` to auto focus the input on mount
	 */
	export let autofocus = false;

	/**
	 * Specify the debounce value in milliseconds (ms)
	 */
	export let debounce = 0;

	/**
	 * Specify the input label text
	 */
	export let label = "Label";

	/**
	 * Set to `true` to visually hide the label
	 */
	export let hideLabel = false;

	/**
	 * Specify an `id` for the `input`
	 */
	export let id = "search" + Math.random().toString(36);

	/**
	 * Obtain a reference to the `input` element
	 * @type {HTMLInputElement}
	 */
	export let ref = null;

	/**
	 * Set to `true` to omit the form `role="search"` attribute
	 */
	export let removeFormAriaAttributes = false;

	import { createEventDispatcher, onMount, afterUpdate } from "svelte";

	const dispatch = createEventDispatcher();

	let prevValue = value;
	let timeout = undefined;
	let calling = false;

	/** @type {() => any;} */
	function debounceFn(fn) {
		if (calling) return;
		calling = true;
		timeout = setTimeout(() => {
			fn();
			calling = false;
		}, debounce);
	}

	onMount(() => {
		if (autofocus) window.requestAnimationFrame(() => ref.focus());
		return () => clearTimeout(timeout);
	});

	afterUpdate(() => {
		if (value.length > 0 && value !== prevValue) {
			if (debounce > 0) {
				debounceFn(() => dispatch("type", value));
			} else {
				dispatch("type", value);
			}
		}

		if (value.length === 0 && prevValue.length > 0) dispatch("clear");

		prevValue = value;
	});
</script>

<form
	data-svelte-search
	role={removeFormAriaAttributes ? null : "search"}
	aria-labelledby={removeFormAriaAttributes ? null : id}
	on:submit|preventDefault
>
	<div class="input-group">
		<span class="input-group-text">
			<svg
				style="fill: #cbd5e1; height: 1.25rem; width: 1.25rem;"
				viewBox="0 0 20 20"
			>
				<path
					fill-rule="evenodd"
					d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
					clip-rule="evenodd"
				/>
			</svg>
		</span>
		<label
			id="{id}-label"
			for={id}
			style={hideLabel &&
				"position: absolute;height: 1px;width: 1px;overflow: hidden;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);white-space: nowrap;"}
		>
			<slot name="label">{label}</slot>
		</label>
		<input
			bind:this={ref}
			name="search"
			type="search"
			placeholder="Search..."
			autocomplete="off"
			spellcheck="false"
			{...$$restProps}
			{id}
			bind:value
			on:input
			on:change
			on:focus
			on:blur
			on:keydown
		/>
	</div>
</form>
