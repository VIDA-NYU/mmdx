import { writable } from 'svelte/store';
import { descriptions, negativeKeywords } from './Descriptions';

export const labelStore = writable<string[]>(descriptions);

export const animalStore = writable<string[]>(["Ostrich", "Wolf", "Silky shark", "Great white shark", "Sand tiger shark", "Hippoglossus", "Halibut", "Ground beetle", "Nile crocodile", "Redfish"]);

export const negativeKeywordStore = writable<string[]>(negativeKeywords);

export const selectedDataStore = writable({});

export const modal = writable(null);
export const windowStyle = writable({});
