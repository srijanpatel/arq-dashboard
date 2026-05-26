<template>
  <JobForm
    ref="form"
    :page="page"
    :functionNames="getFunctionNamesTask.last?.value || []"
    :queueNames="getQueueNamesTask.last?.value || []"
  ></JobForm>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "vue";
import { useAsyncTask } from "vue-concurrency";

import { API } from "@/api";
import JobForm from "@/components/job/Form.vue";
import { FunctionName, QueueName, SearchParams } from "@/types";

export default defineComponent({
  name: "FormWrapper",
  components: {
    JobForm,
  },
  props: {
    page: {
      type: Number,
      required: true,
    },
  },
  setup() {
    const form = ref<InstanceType<typeof JobForm>>();

    const getSearchParams = () => {
      return form.value?.getSearchParams() as SearchParams;
    };

    const getFunctionNamesTask = useAsyncTask<FunctionName[], []>(async () => {
      return await API.getFunctionNames();
    });

    const getQueueNamesTask = useAsyncTask<QueueName[], []>(async () => {
      return await API.getQueueNames();
    });

    onMounted(async () => {
      await getFunctionNamesTask.perform();
      await getQueueNamesTask.perform();
    });

    return {
      getFunctionNamesTask,
      getQueueNamesTask,
      getSearchParams,
      form,
    };
  },
});
</script>
