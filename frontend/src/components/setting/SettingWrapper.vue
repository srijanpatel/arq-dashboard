<script setup lang="ts">
import { onMounted } from "vue";

import { API } from "@/api";
import Setting from "@/components/setting/Setting.vue";
import { useAsyncTask } from "@/composables/useAsyncTask";
import type { QueueName } from "@/types";

const { data: queueNames, perform } = useAsyncTask<QueueName[]>(
  () => API.getQueueNames()
);

onMounted(() => perform());
</script>

<template>
  <Setting :queue-names="queueNames || []" />
</template>
