<template>
  <Loading v-if="getStatsTask.isRunning"></Loading>

  <div v-if="getStatsTask.last?.value">
    <StatsComponent :stats="getStatsTask.last.value"></StatsComponent>

    <div class="columns">
      <div class="column">
        <div class="field is-grouped is-grouped-centered">
          <p class="control">
            <a class="button is-light" @click="update">
              <span class="icon is-small">
                <i class="fas fa-sync"></i>
              </span>
              <span>Update</span>
            </a>
          </p>
        </div>
        <CachedAt :cachedAt="getStatsTask.last.value.cachedAt"></CachedAt>
      </div>
    </div>
  </div>

  <ErrorMessage
    v-if="getStatsTask.isError"
    :error="getStatsTask.last?.error"
  ></ErrorMessage>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { useAsyncTask } from "vue-concurrency";

import { API } from "@/api";
import CachedAt from "@/components/CachedAt.vue";
import ErrorMessage from "@/components/ErrorMessage.vue";
import Loading from "@/components/Loading.vue";
import StatsComponent from "@/components/stats/Stats.vue";
import { Stats } from "@/types";
import { getHumanizedRelativeTime, getLocalDatetime } from "@/utils";

export default defineComponent({
  name: "StatsWrapper",
  components: {
    Loading,
    ErrorMessage,
    StatsComponent,
    CachedAt,
  },
  setup() {
    const getStatsTask = useAsyncTask<Stats, []>(async () => {
      return await API.getStats();
    });

    const update = async () => {
      await getStatsTask.perform();
    };

    onMounted(async () => {
      await update();
    });

    return {
      getStatsTask,
      update,
      getHumanizedRelativeTime,
      getLocalDatetime,
    };
  },
});
</script>
