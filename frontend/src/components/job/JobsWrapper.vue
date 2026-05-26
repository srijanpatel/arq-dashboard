<script setup lang="ts">
import { nextTick, onMounted, ref, watch } from "vue";

import { API } from "@/api";
import ErrorMessage from "@/components/ErrorMessage.vue";
import JobForm from "@/components/job/FormWrapper.vue";
import Jobs from "@/components/job/Jobs.vue";
import Loading from "@/components/Loading.vue";
import Icon from "@/components/ui/Icon.vue";
import { useAsyncTask } from "@/composables/useAsyncTask";
import type { JobsWithPagination, SearchParams } from "@/types";

const page = ref(1);
const form = ref<InstanceType<typeof JobForm>>();

const {
  data: jobsData,
  isRunning,
  isError,
  error,
  performCount,
  perform: fetchJobs,
} = useAsyncTask<JobsWithPagination>(() => {
  const params = form.value?.getSearchParams() as SearchParams;
  return API.getJobs(params);
});

function updatePage(newPage: number) {
  page.value = newPage;
}

async function refreshPage() {
  page.value = 1;
  await fetchJobs();
}

async function search() {
  page.value = 1;
  nextTick(() => fetchJobs());
}

onMounted(() => fetchJobs());

watch(page, () => {
  nextTick(() => fetchJobs());
});
</script>

<template>
  <div class="card mb-lg">
    <JobForm ref="form" :page="page" />
    <hr />
    <div class="flex justify-center">
      <button class="btn" @click="search">
        <Icon name="search" :size="14" />
        Search
      </button>
    </div>
  </div>

  <div v-if="performCount > 0">
    <Loading v-if="isRunning" />
    <ErrorMessage v-if="isError" :error="error" />
    <Jobs
      v-if="jobsData"
      :jobs="jobsData"
      @refresh-page="refreshPage"
      @update-page="updatePage"
    />
  </div>
</template>
