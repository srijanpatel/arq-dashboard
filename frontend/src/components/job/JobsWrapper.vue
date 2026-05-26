<template>
  <div class="box mb-6">
    <JobForm ref="form" :page="page"></JobForm>

    <hr />

    <div class="columns">
      <div class="column">
        <div class="field is-grouped is-grouped-centered">
          <p class="control">
            <a class="button is-light" @click="search">
              <span class="icon is-small">
                <i class="fas fa-search"></i>
              </span>
              <span>Search</span>
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>

  <div v-if="getJobsTask.performCount > 0">
    <hr />

    <Loading v-if="getJobsTask.isRunning"></Loading>

    <ErrorMessage
      v-if="getJobsTask.isError"
      :error="getJobsTask.last?.error"
    ></ErrorMessage>

    <Jobs
      :jobs="getJobsTask.last.value"
      v-if="getJobsTask.last?.value"
      @refresh-page="refreshPage"
      @update-page="updatePage"
    ></Jobs>
  </div>
</template>

<script lang="ts">
import { defineComponent, nextTick, onMounted, ref, watch } from "vue";
import { useAsyncTask } from "vue-concurrency";

import { API } from "@/api";
import ErrorMessage from "@/components/ErrorMessage.vue";
import JobForm from "@/components/job/FormWrapper.vue";
import Jobs from "@/components/job/Jobs.vue";
import Loading from "@/components/Loading.vue";
import { JobsWithPagination, SearchParams } from "@/types";

export default defineComponent({
  name: "JobsWrapper",
  components: {
    Loading,
    ErrorMessage,
    JobForm,
    Jobs,
  },
  setup() {
    const page = ref(1);
    const form = ref<InstanceType<typeof JobForm>>();

    const getJobsTask = useAsyncTask<JobsWithPagination, [SearchParams]>(
      async (_signal, params) => {
        return await API.getJobs(params);
      }
    );

    const getJobs = async () => {
      const params = form.value?.getSearchParams() as SearchParams;
      return await getJobsTask.perform(params);
    };

    const updatePage = (newPage: number) => {
      page.value = newPage;
    };

    const resetPage = () => {
      page.value = 1;
    };

    const refreshPage = async () => {
      resetPage();
      await getJobs();
    };

    const search = async () => {
      resetPage();
      nextTick(async () => await getJobs());
    };

    onMounted(async () => {
      await getJobs();
    });

    watch(page, async () => {
      nextTick(async () => await getJobs());
    });

    return {
      getJobsTask,
      page,
      form,
      search,
      refreshPage,
      updatePage,
    };
  },
});
</script>
