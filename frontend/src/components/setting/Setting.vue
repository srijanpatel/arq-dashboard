<template>
  <div>
    <div class="box">
      <div class="field">
        <label class="label">ARQ queue name</label>
        <div class="control">
          <div class="select">
            <select v-model="queue" @change="updateSetting">
              <option v-for="q in queueNames" :key="q.name">
                {{ q.name }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from "vue";

import { updateClient } from "@/api";
import { useGlobalState } from "@/store";
import { QueueName } from "@/types";

export default defineComponent({
  name: "SettingItem",
  props: {
    queueNames: {
      type: Array as PropType<QueueName[]>,
      required: true,
    },
  },
  setup() {
    const state = useGlobalState();

    const queue = ref(state.value.queue);

    const updateSetting = () => {
      state.value.queue = queue.value;
      updateClient();
    };

    return { queue, updateSetting };
  },
});
</script>
