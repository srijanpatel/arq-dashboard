<script setup lang="ts">
import { useRouteQuery } from "@vueuse/router";
import { computed, onMounted, type Ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const props = defineProps<{
  currentPage: number;
  pageSize: number;
  total: number;
}>();

const emit = defineEmits<{ "update-page": [page: number] }>();

const route = useRoute();
const router = useRouter();
const options = { route, router };

const totalPageCount = computed(() => Math.ceil(props.total / props.pageSize));
const hasOnlyOnePage = computed(() => totalPageCount.value <= 1);
const hasPreviousPage = computed(() => props.currentPage > 1);
const isPreviousPageNotFirst = computed(() => props.currentPage - 1 !== 1);
const hasNextPage = computed(() => props.currentPage < totalPageCount.value);
const isNextPageNotLast = computed(() => props.currentPage + 1 !== totalPageCount.value);

function updatePage(page: number) {
  const pageQuery = useRouteQuery("page", page.toString(), options);
  pageQuery.value = page.toString();
  emit("update-page", page);
}

onMounted(() => {
  const pageQuery = useRouteQuery("page", null, options) as Ref<string | null>;
  if (pageQuery.value && parseInt(pageQuery.value) !== props.currentPage) {
    updatePage(parseInt(pageQuery.value));
  }
});
</script>

<template>
  <nav v-if="!hasOnlyOnePage" class="pagination" aria-label="pagination">
    <a
      v-if="hasPreviousPage && isPreviousPageNotFirst"
      class="pagination-link"
      @click="updatePage(1)"
    >1</a>
    <span v-if="hasPreviousPage && isPreviousPageNotFirst" class="pagination-ellipsis">&hellip;</span>
    <a
      v-if="hasPreviousPage"
      class="pagination-link"
      @click="updatePage(currentPage - 1)"
    >{{ currentPage - 1 }}</a>
    <a
      class="pagination-link pagination-link-active"
      @click="updatePage(currentPage)"
    >{{ currentPage }}</a>
    <a
      v-if="hasNextPage"
      class="pagination-link"
      @click="updatePage(currentPage + 1)"
    >{{ currentPage + 1 }}</a>
    <span v-if="hasNextPage && isNextPageNotLast" class="pagination-ellipsis">&hellip;</span>
    <a
      v-if="hasNextPage && isNextPageNotLast"
      class="pagination-link"
      @click="updatePage(totalPageCount)"
    >{{ totalPageCount }}</a>
  </nav>
</template>
