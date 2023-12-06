import { writable } from 'svelte/store';
import { descriptions } from './Descriptions';

export const labelStore = writable<string[]>(descriptions);

export const animalStore = writable<string[]>(["Ostrich", "Wolf", "Silky shark", "Great white shark", "Sand tiger shark", "Hippoglossus", "Halibut", "Ground beetle", "Nile crocodile", "Redfish"]);

export const negativeKeywordStore = writable<string[]>(["T-shirt", "Stamp", "Photograph"]);

export const modal = writable(null);
export const windowStyle = writable({});
