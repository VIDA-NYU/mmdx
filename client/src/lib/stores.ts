import { writable } from 'svelte/store';

export const labelStore = writable<string[]>(["relevant", "irrelevant"]);