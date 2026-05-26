<template>
  <Stats></Stats>
</template>

<script lang="ts">
import { useTitle } from "@vueuse/core";
import { defineComponent, onMounted } from "vue";

import Stats from "@/components/stats/StatsWrapper.vue";

export default defineComponent({
  name: "StatsView",
  components: {
    Stats,
  },
  setup() {
    onMounted(() => {
      useTitle("Stats - ARQ Dashboard");
    });
  },
});
</script>
