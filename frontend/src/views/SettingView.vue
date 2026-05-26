<template>
  <Setting></Setting>
</template>

<script lang="ts">
import { useTitle } from "@vueuse/core";
import { defineComponent, onMounted } from "vue";

import Setting from "@/components/setting/SettingWrapper.vue";

export default defineComponent({
  name: "SettingView",
  components: {
    Setting,
  },
  setup() {
    onMounted(() => {
      useTitle("Setting - ARQ Dashboard");
    });
  },
});
</script>
