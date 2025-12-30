import type { Config } from "vike/types";
import vikeVue from "vike-vue/config";

// Default config (can be overridden by pages)
// https://vike.dev/config

export default {
  // https://vike.dev/head-tags
  title: "My Vike App",
  description: "Demo showcasing Vike",
  // 禁用SSR以解决CSS加载问题
  ssr: false,
  extends: [vikeVue],
} as Config;
