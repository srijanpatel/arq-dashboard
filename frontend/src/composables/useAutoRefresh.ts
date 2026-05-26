import { onUnmounted, ref, watch } from "vue";

export type RefreshInterval = 0 | 10 | 30 | 60;

const STORAGE_KEY = "arq-dash-refresh-interval";

export function useAutoRefresh(callback: () => void) {
  const stored = parseInt(localStorage.getItem(STORAGE_KEY) || "0");
  const interval = ref<RefreshInterval>(
    [0, 10, 30, 60].includes(stored) ? (stored as RefreshInterval) : 0
  );
  let timerId: ReturnType<typeof setInterval> | null = null;

  function start() {
    stop();
    if (interval.value > 0) {
      timerId = setInterval(callback, interval.value * 1000);
    }
  }

  function stop() {
    if (timerId) {
      clearInterval(timerId);
      timerId = null;
    }
  }

  function setInterval_(val: RefreshInterval) {
    interval.value = val;
    localStorage.setItem(STORAGE_KEY, String(val));
    start();
  }

  watch(interval, () => start(), { immediate: true });

  onUnmounted(() => stop());

  return { interval, setInterval: setInterval_ };
}
