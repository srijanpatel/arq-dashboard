import { createGlobalState, useLocalStorage } from "@vueuse/core";

export const useGlobalState = createGlobalState(() => {
  return useLocalStorage("arq-dashboard-state", {
    queue: "arq:queue",
  });
});
