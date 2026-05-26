<script setup lang="ts">
import "vue-json-pretty/lib/styles.css";

import VueJsonPretty from "vue-json-pretty";

import CachedAt from "@/components/CachedAt.vue";
import Status from "@/components/job/Status.vue";
import JobTimeline from "@/components/job/JobTimeline.vue";
import Success from "@/components/job/Success.vue";
import type { CachedJob } from "@/types";

defineProps<{ job: CachedJob }>();
</script>

<template>
  <div class="animate-fade-up">
    <!-- Header -->
    <div class="flex items-center gap-md mb-lg flex-wrap">
      <h2 class="text-mono" style="font-family: var(--font-ui); font-size: 1.1rem;">{{ job.jobId }}</h2>
      <Status :status="job.status" />
      <Success :success="job.success" :status="job.status" />
      <span v-if="job.jobTry && job.jobTry > 0" class="tag tag-warning">
        try #{{ job.jobTry }}
      </span>
    </div>

    <!-- Timeline -->
    <div class="card mb-lg">
      <h4 class="mb-sm text-muted text-sm" style="font-family: var(--font-ui);">TIMELINE</h4>
      <JobTimeline
        :enqueue-time="job.enqueueTime"
        :start-time="job.startTime"
        :finish-time="job.finishTime"
      />
    </div>

    <!-- Details grid -->
    <div class="grid grid-cols-2 mb-lg">
      <div class="card">
        <h4 class="text-muted text-sm mb-sm" style="font-family: var(--font-ui);">FUNCTION</h4>
        <p class="text-mono">{{ job.function }}</p>
      </div>
      <div class="card">
        <h4 class="text-muted text-sm mb-sm" style="font-family: var(--font-ui);">QUEUE</h4>
        <p>{{ job.queueName || '—' }}</p>
      </div>
    </div>

    <!-- Args -->
    <div v-if="job.args && job.args.length > 0" class="card mb-lg">
      <h4 class="text-muted text-sm mb-sm" style="font-family: var(--font-ui);">ARGS</h4>
      <div class="code-block">
        <VueJsonPretty :data="job.args" :deep="2" />
      </div>
    </div>

    <!-- Kwargs -->
    <div v-if="job.kwargs && Object.keys(job.kwargs as any).length > 0" class="card mb-lg">
      <h4 class="text-muted text-sm mb-sm" style="font-family: var(--font-ui);">KWARGS</h4>
      <div class="code-block">
        <VueJsonPretty :data="(job.kwargs as any)" :deep="2" />
      </div>
    </div>

    <!-- Result -->
    <div v-if="job.result !== null && job.result !== undefined" class="card mb-lg">
      <h4 class="text-muted text-sm mb-sm" style="font-family: var(--font-ui);">RESULT</h4>
      <div class="code-block">
        <VueJsonPretty :data="(job.result as any)" :deep="3" />
      </div>
    </div>

    <CachedAt :cached-at="job.cachedAt" />
  </div>
</template>
