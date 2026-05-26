<template>
  <Jobs></Jobs>
</template>

<script lang="ts">
import { useTitle } from "@vueuse/core";
import { defineComponent, onMounted } from "vue";

import Jobs from "@/components/job/JobsWrapper.vue";

export default defineComponent({
  name: "JobsView",
  components: {
    Jobs,
  },
  setup() {
    onMounted(() => {
      useTitle("Jobs - ARQ Dashboard");
    });
  },
});
</script>
