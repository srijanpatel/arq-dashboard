<template>
  <div v-if="dt === undefined">
    <p>-</p>
  </div>
  <div v-else>
    <p>{{ getLocalDatetime(dt) }}</p>
    <p>({{ getHumanizedRelativeTime(dt) }})</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import { getHumanizedRelativeTime, getLocalDatetime } from "@/utils";

export default defineComponent({
  name: "ReadableDatetimeItem",
  props: {
    dt: {
      type: String,
      required: false,
    },
  },
  setup() {
    return { getHumanizedRelativeTime, getLocalDatetime };
  },
});
</script>
