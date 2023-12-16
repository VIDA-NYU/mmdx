import { writable } from 'svelte/store';
import { animals, descriptions, negativeKeywords } from "./Descriptions";

export const labelStore = writable<string[]>(descriptions);

export const animalStore = writable<string[]>(animals);

export const negativeKeywordStore = writable<string[]>(negativeKeywords);

export const selectedDataStore = writable({});

export const modal = writable(null);
export const windowStyle = writable({});
