import { onUnmounted, ref } from "vue";

/**
 * Reactive tick counter that increments every `intervalMs`.
 * Components that use `tick` in their template will re-render,
 * causing dayjs `.fromNow()` calls to update.
 */
const tick = ref(0);
let intervalId: ReturnType<typeof setInterval> | null = null;
let subscribers = 0;

export function useLiveClock(intervalMs = 15000) {
  if (subscribers === 0) {
    intervalId = setInterval(() => {
      tick.value++;
    }, intervalMs);
  }
  subscribers++;

  onUnmounted(() => {
    subscribers--;
    if (subscribers === 0 && intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  });

  return { tick };
}
