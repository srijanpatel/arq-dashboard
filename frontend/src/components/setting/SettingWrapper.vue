<template>
  <Setting :queueNames="getQueueNamesTask.last?.value || []"></Setting>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { useAsyncTask } from "vue-concurrency";

import { API } from "@/api";
import Setting from "@/components/setting/Setting.vue";
import { QueueName } from "@/types";

export default defineComponent({
  name: "SettingWrapper",
  components: {
    Setting,
  },
  setup() {
    const getQueueNamesTask = useAsyncTask<QueueName[], []>(async () => {
      return await API.getQueueNames();
    });

    onMounted(async () => {
      await getQueueNamesTask.perform();
    });

    return {
      getQueueNamesTask,
    };
  },
});
</script>
