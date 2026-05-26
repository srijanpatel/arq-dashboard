<template>
  <h2 class="is-size-2 mb-4">{{ state.queue }}</h2>

  <div class="columns">
    <div class="column">
      <article class="message">
        <div class="message-header">
          <p>Queued jobs</p>
        </div>
        <div class="message-body has-text-centered">
          <router-link :to="{ name: 'jobs', query: { status: 'queued' } }">{{
            stats.queuedJobs
          }}</router-link>
        </div>
      </article>
    </div>
    <div class="column">
      <article class="message is-info">
        <div class="message-header">
          <p>Deferred jobs</p>
        </div>
        <div class="message-body has-text-centered">
          <router-link :to="{ name: 'jobs', query: { status: 'deferred' } }">{{
            stats.deferredJobs
          }}</router-link>
        </div>
      </article>
    </div>
    <div class="column">
      <article class="message is-link">
        <div class="message-header">
          <p>In progress jobs</p>
        </div>
        <div class="message-body has-text-centered">
          <router-link
            :to="{ name: 'jobs', query: { status: 'in_progress' } }"
            >{{ stats.inProgressJobs }}</router-link
          >
        </div>
      </article>
    </div>

    <div class="column">
      <article class="message is-success">
        <div class="message-header">
          <p>Complete jobs</p>
        </div>
        <div class="message-body has-text-centered">
          <router-link :to="{ name: 'jobs', query: { status: 'complete' } }">{{
            stats.completeJobs
          }}</router-link>
        </div>
      </article>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

import { useGlobalState } from "@/store";
import { Stats } from "@/types";

export default defineComponent({
  name: "StatsItem",
  props: {
    stats: {
      type: Object as PropType<Stats>,
      required: true,
    },
  },
  setup() {
    const state = useGlobalState();

    return { state };
  },
});
</script>
