<script setup lang="ts">
import { onMounted } from "vue";

import { API } from "@/api";
import CachedAt from "@/components/CachedAt.vue";
import ErrorMessage from "@/components/ErrorMessage.vue";
import Loading from "@/components/Loading.vue";
import StatsComponent from "@/components/stats/Stats.vue";
import { useAsyncTask } from "@/composables/useAsyncTask";
import type { Stats } from "@/types";

const { data: stats, isRunning, isError, error, perform } = useAsyncTask<Stats>(
  () => API.getStats()
);

onMounted(() => perform());
</script>

<template>
  <Loading v-if="isRunning" />

  <div v-if="stats">
    <StatsComponent :stats="stats" />

    <div class="columns">
      <div class="column">
        <div class="field is-grouped is-grouped-centered">
          <p class="control">
            <a class="button is-light" @click="perform()">
              <span class="icon is-small"><i class="fas fa-sync"></i></span>
              <span>Update</span>
            </a>
          </p>
        </div>
        <CachedAt :cached-at="stats.cachedAt" />
      </div>
    </div>
  </div>

  <ErrorMessage v-if="isError" :error="error" />
</template>
