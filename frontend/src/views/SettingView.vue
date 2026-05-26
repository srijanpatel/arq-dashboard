<script setup lang="ts">
import { useTitle } from "@vueuse/core";
import { onMounted } from "vue";

import Setting from "@/components/setting/SettingWrapper.vue";

onMounted(() => useTitle("Setting - ARQ Dashboard"));
</script>

<template>
  <Setting />
</template>
