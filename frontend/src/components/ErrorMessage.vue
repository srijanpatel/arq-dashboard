<template>
  <div class="notification is-danger is-light">
    <p>Something went wrong...</p>
  </div>
  <div class="wrapper" v-if="error.response.data">
    <VueJsonPretty :data="error.response.data"></VueJsonPretty>
  </div>
  <p v-else>{{ error }}</p>
</template>

<script lang="ts">
import "vue-json-pretty/lib/styles.css";

import { defineComponent } from "vue";
import VueJsonPretty from "vue-json-pretty";

export default defineComponent({
  name: "ErrorMessageItem",
  components: {
    VueJsonPretty,
  },
  props: {
    error: {
      type: Object,
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
