import { createGlobalState, useLocalStorage } from "@vueuse/core";

export const useGlobalState = createGlobalState(() => {
  return useLocalStorage("arq-dashboard-locale-storage", {
    queue: "arq:queue",
  });
});
