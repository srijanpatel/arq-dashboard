import { computed, onMounted, ref, watch } from "vue";

type Theme = "light" | "dark";

const STORAGE_KEY = "arq-dash-theme";
const theme = ref<Theme>("light");

function getSystemTheme(): Theme {
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function applyTheme(t: Theme) {
  document.documentElement.setAttribute("data-theme", t);
}

export function useTheme() {
  const isDark = computed(() => theme.value === "dark");

  function toggleTheme() {
    theme.value = theme.value === "dark" ? "light" : "dark";
    localStorage.setItem(STORAGE_KEY, theme.value);
    applyTheme(theme.value);
  }

  onMounted(() => {
    const stored = localStorage.getItem(STORAGE_KEY) as Theme | null;
    theme.value = stored || getSystemTheme();
    applyTheme(theme.value);

    window
      .matchMedia("(prefers-color-scheme: dark)")
      .addEventListener("change", (e) => {
        if (!localStorage.getItem(STORAGE_KEY)) {
          theme.value = e.matches ? "dark" : "light";
          applyTheme(theme.value);
        }
      });
  });

  return { theme, isDark, toggleTheme };
}
