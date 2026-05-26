import { ref, shallowRef } from "vue";

export function useAsyncTask<T>(fn: (...args: unknown[]) => Promise<T>) {
  const data = shallowRef<T | null>(null);
  const error = shallowRef<unknown>(null);
  const isRunning = ref(false);
  const isError = ref(false);
  const performCount = ref(0);

  async function perform(...args: unknown[]): Promise<T | null> {
    isRunning.value = true;
    isError.value = false;
    error.value = null;
    performCount.value++;
    try {
      data.value = await fn(...args);
    } catch (e) {
      error.value = e;
      isError.value = true;
    } finally {
      isRunning.value = false;
    }
    return data.value;
  }

  return { data, error, isRunning, isError, performCount, perform };
}
