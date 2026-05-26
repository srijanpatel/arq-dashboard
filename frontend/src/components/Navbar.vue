<script setup lang="ts">
import Icon from "@/components/ui/Icon.vue";
import { useTheme } from "@/composables/useTheme";

const { isDark, toggleTheme } = useTheme();
</script>

<template>
  <nav class="navbar">
    <router-link to="/" class="navbar-brand">ARQ Dashboard</router-link>
    <div class="navbar-links">
      <router-link class="navbar-link" :to="{ name: 'stats' }">Stats</router-link>
      <router-link class="navbar-link" :to="{ name: 'jobs' }">Jobs</router-link>
      <router-link class="navbar-link" :to="{ name: 'setting' }">Settings</router-link>
      <button class="btn btn-ghost btn-icon" @click="toggleTheme" title="Toggle theme">
        <Icon :name="isDark ? 'sun' : 'moon'" :size="18" />
      </button>
    </div>
  </nav>
  <div class="navbar-spacer"></div>
</template>
