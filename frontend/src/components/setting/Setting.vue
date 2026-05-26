<script setup lang="ts">
import { ref } from "vue";

import { updateClient } from "@/api";
import { useGlobalState } from "@/store";
import type { QueueName } from "@/types";

defineProps<{ queueNames: QueueName[] }>();

const state = useGlobalState();
const queue = ref(state.value.queue);

function updateSetting() {
  state.value.queue = queue.value;
  updateClient();
}
</script>

<template>
  <div class="card" style="max-width: 480px;">
    <h3 class="mb-md">Queue Settings</h3>
    <div class="form-group">
      <label class="form-label">ARQ queue name</label>
      <select v-model="queue" class="form-select" @change="updateSetting">
        <option v-for="q in queueNames" :key="q.name">{{ q.name }}</option>
      </select>
    </div>
  </div>
</template>
