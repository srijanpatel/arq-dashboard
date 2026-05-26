<script setup lang="ts">
import { nextTick, onMounted, ref, watch } from "vue";

import { API } from "@/api";
import ErrorMessage from "@/components/ErrorMessage.vue";
import JobForm from "@/components/job/FormWrapper.vue";
import Jobs from "@/components/job/Jobs.vue";
import Loading from "@/components/Loading.vue";
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

function resetPage() {
  page.value = 1;
}

async function refreshPage() {
  resetPage();
  await fetchJobs();
}

async function search() {
  resetPage();
  nextTick(() => fetchJobs());
}

onMounted(() => fetchJobs());

watch(page, () => {
  nextTick(() => fetchJobs());
});
</script>

<template>
  <div class="box mb-6">
    <JobForm ref="form" :page="page" />

    <hr />

    <div class="columns">
      <div class="column">
        <div class="field is-grouped is-grouped-centered">
          <p class="control">
            <a class="button is-light" @click="search">
              <span class="icon is-small"><i class="fas fa-search"></i></span>
              <span>Search</span>
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>

  <div v-if="performCount > 0">
    <hr />
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
