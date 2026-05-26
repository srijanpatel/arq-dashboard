<template>
  <h2 class="is-size-2 mb-4">{{ job.jobId }}</h2>

  <div class="wrapper">
    <VueJsonPretty :data="job"></VueJsonPretty>
  </div>
  <CachedAt :cachedAt="job.cachedAt"></CachedAt>
</template>

<script lang="ts">
import "vue-json-pretty/lib/styles.css";

import { defineComponent, PropType } from "vue";
import VueJsonPretty from "vue-json-pretty";

import CachedAt from "@/components/CachedAt.vue";
import { CachedJob } from "@/types";

export default defineComponent({
  name: "JobItem",
  components: {
    VueJsonPretty,
    CachedAt,
  },
  props: {
    job: {
      type: Object as PropType<CachedJob>,
      required: true,
    },
  },
});
</script>
<style scoped>
.wrapper {
  background-color: rgb(246, 248, 250);
  padding: 10px;
}
</style>
