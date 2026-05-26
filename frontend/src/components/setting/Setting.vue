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
  <div class="box">
    <div class="field">
      <label class="label">ARQ queue name</label>
      <div class="control">
        <div class="select">
          <select v-model="queue" @change="updateSetting">
            <option v-for="q in queueNames" :key="q.name">{{ q.name }}</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>
