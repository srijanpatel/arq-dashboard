<template>
  <span class="tag is-medium is-light" :class="className">{{ success }}</span>
</template>

<script lang="ts">
import { computed, defineComponent } from "vue";

export default defineComponent({
  name: "SuccessItem",
  props: {
    success: {
      type: Boolean,
      required: true,
    },
    status: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const className = computed(() => {
      if (props.status === "complete") {
        return props.success ? "is-success" : "is-danger";
      }

      return "";
    });

    return { className };
  },
});
</script>
