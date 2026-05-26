<script setup lang="ts">
import "@vuepic/vue-datepicker/dist/main.css";

import Datepicker from "@vuepic/vue-datepicker";
import { useRouteQuery } from "@vueuse/router";
import { onMounted, ref } from "vue";

import type { FunctionName, QueueName, SearchParams } from "@/types";

const props = defineProps<{
  page: number;
  functionNames: FunctionName[];
  queueNames: QueueName[];
}>();

const success = ref<boolean | undefined>(undefined);
const startTime = ref<string | undefined>(undefined);
const finishTime = ref<string | undefined>(undefined);
const functionName = ref<string | undefined>(undefined);
const status = ref<string | undefined>(undefined);

const functionQuery = useRouteQuery("function");
const statusQuery = useRouteQuery("status");

const statuses = ["deferred", "queued", "in_progress", "complete", "not_found"];

function normalizeQueryValue(value: string | undefined): string | undefined {
  if (value === undefined || value === "") return undefined;
  return value;
}

function getSearchParams(): SearchParams {
  return {
    page: props.page,
    success: success.value,
    status: normalizeQueryValue(status.value),
    startTime: normalizeQueryValue(startTime.value),
    finishTime: normalizeQueryValue(finishTime.value),
    functionName: normalizeQueryValue(functionName.value),
  };
}

onMounted(() => {
  if (functionQuery.value) functionName.value = functionQuery.value.toString();
  if (statusQuery.value) status.value = statusQuery.value.toString();
});

defineExpose({ getSearchParams });
</script>

<template>
  <div class="columns">
    <div class="column">
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Function</label>
        </div>
        <div class="field-body">
          <div class="field">
            <div class="control">
              <div class="select">
                <select v-model="functionName">
                  <option value=""></option>
                  <option v-for="f in functionNames" :key="f.name">{{ f.name }}</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="column">
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Status</label>
        </div>
        <div class="field-body">
          <div class="field">
            <div class="control">
              <div class="select">
                <select v-model="status">
                  <option value=""></option>
                  <option v-for="s in statuses" :key="s">{{ s }}</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="columns">
    <div class="column">
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Start time</label>
        </div>
        <div class="field-body">
          <div class="field">
            <p class="control">
              <Datepicker v-model="startTime" />
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="column">
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Finish time</label>
        </div>
        <div class="field-body">
          <div class="field">
            <p class="control">
              <Datepicker v-model="finishTime" />
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="columns">
    <div class="column">
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Success</label>
        </div>
        <div class="field-body">
          <div class="field">
            <div class="control">
              <label class="radio">
                <input type="radio" v-model="success" :value="true" /> True
              </label>
              <label class="radio">
                <input type="radio" v-model="success" :value="false" /> False
              </label>
              <label class="radio">
                <input type="radio" v-model="success" :value="undefined" /> Both
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="column"></div>
  </div>
</template>
