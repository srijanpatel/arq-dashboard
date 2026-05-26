import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";

import JobsView from "@/views/JobsView.vue";
import JobView from "@/views/JobView.vue";
import SettingView from "@/views/SettingView.vue";
import StatsView from "@/views/StatsView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "stats",
    component: StatsView,
  },
  {
    path: "/jobs/:id",
    name: "job",
    component: JobView,
    props: true,
  },
  {
    path: "/jobs/",
    name: "jobs",
    component: JobsView,
  },
  {
    path: "/setting/",
    name: "setting",
    component: SettingView,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
