<script setup lang="ts">
import { onMounted, ref } from "vue";

import { API } from "@/api";
import JobForm from "@/components/job/Form.vue";
import { useAsyncTask } from "@/composables/useAsyncTask";
import type { FunctionName, QueueName, SearchParams } from "@/types";

defineProps<{ page: number }>();

const form = ref<InstanceType<typeof JobForm>>();

const { data: functionNames, perform: fetchFunctions } = useAsyncTask<FunctionName[]>(
  () => API.getFunctionNames()
);
const { data: queueNames, perform: fetchQueues } = useAsyncTask<QueueName[]>(
  () => API.getQueueNames()
);

function getSearchParams(): SearchParams {
  return form.value!.getSearchParams();
}

onMounted(async () => {
  await Promise.all([fetchFunctions(), fetchQueues()]);
});

defineExpose({ getSearchParams });
</script>

<template>
  <JobForm
    ref="form"
    :page="page"
    :function-names="functionNames || []"
    :queue-names="queueNames || []"
  />
</template>
