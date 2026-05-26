<template>
  <span class="tag is-medium" :class="className">{{ status }}</span>
</template>

<script lang="ts">
import { computed, defineComponent } from "vue";

export default defineComponent({
  name: "StatusItem",
  props: {
    status: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const statusToClassName = new Map<string, string>([
      ["deferred", "is-info"],
      ["queued", ""],
      ["in_progress", "is-link"],
      ["complete", "is-success"],
      ["not_found", "is-warning"],
    ]);

    const className = computed(() => {
      return statusToClassName.get(props.status) || "";
    });

    return { className };
  },
});
</script>
