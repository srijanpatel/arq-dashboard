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
const hasOnlyOnePage = computed(() => totalPageCount.value === 1);
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
  <nav class="pagination" role="navigation" aria-label="pagination">
    <ul v-if="hasOnlyOnePage" class="pagination-list">
      <li>
        <a class="pagination-link mt-2 is-current" @click="updatePage(1)">1</a>
      </li>
    </ul>
    <ul v-else class="pagination-list">
      <li v-if="hasPreviousPage && isPreviousPageNotFirst">
        <a class="pagination-link mt-2" @click="updatePage(1)">1</a>
      </li>
      <li v-if="hasPreviousPage && isPreviousPageNotFirst">
        <span class="pagination-ellipsis">&hellip;</span>
      </li>
      <li v-if="hasPreviousPage">
        <a class="pagination-link mt-2" @click="updatePage(currentPage - 1)">
          {{ currentPage - 1 }}
        </a>
      </li>
      <li>
        <a class="pagination-link mt-2 is-current" @click="updatePage(currentPage)">
          {{ currentPage }}
        </a>
      </li>
      <li v-if="hasNextPage">
        <a class="pagination-link mt-2" @click="updatePage(currentPage + 1)">
          {{ currentPage + 1 }}
        </a>
      </li>
      <li v-if="hasNextPage && isNextPageNotLast">
        <span class="pagination-ellipsis">&hellip;</span>
      </li>
      <li v-if="hasNextPage && isNextPageNotLast">
        <a class="pagination-link mt-2" @click="updatePage(totalPageCount)">
          {{ totalPageCount }}
        </a>
      </li>
    </ul>
  </nav>
</template>
