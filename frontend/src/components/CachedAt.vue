<template>
  <p class="has-text-grey">
    Cached at:
    {{ getLocalDatetime(cachedAt) }} ({{ getHumanizedRelativeTime(cachedAt) }})
  </p>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import { getHumanizedRelativeTime, getLocalDatetime } from "@/utils";

export default defineComponent({
  name: "CachedAtItem",
  props: {
    cachedAt: {
      type: String,
      required: true,
    },
  },
  setup() {
    return { getHumanizedRelativeTime, getLocalDatetime };
  },
});
</script>
