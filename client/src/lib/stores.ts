import { writable } from 'svelte/store';

export const labelStore = writable<string[]>(["example1", "example2"]);

export const animalStore = writable<string[]>(["Ostrich", "Wolf", "Silky shark", "Great white shark", "Sand tiger shark", "Hippoglossus", "Halibut", "Ground beetle", "Nile crocodile", "Redfish"]);

export const modal = writable(null);
export const windowStyle = writable({});

