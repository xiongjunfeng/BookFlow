<template>
  <a :href="href" :class="['sidebar-link', { active: isActive }]">
    <slot />
  </a>
</template>

<script lang="ts" setup>
import { usePageContext } from "vike-vue/usePageContext";
import { computed, useAttrs } from "vue";

const pageContext = usePageContext();
const attrs = useAttrs();
const href = computed(() => attrs.href as string);
const isActive = computed(() => {
  const { urlPathname } = pageContext;
  return href.value === "/" ? urlPathname === href.value : urlPathname.startsWith(href.value);
});
</script>

<style scoped>
.sidebar-link {
  padding: 8px 16px;
  margin: 4px 0;
  border-radius: 4px;
  color: #303133;
  transition: all 0.3s;
  display: block;
  text-decoration: none;
}

.sidebar-link:hover {
  background-color: #ecf5ff;
  color: #409eff;
}

.sidebar-link.active {
  background-color: #ecf5ff;
  color: #409eff;
  border-right: 3px solid #409eff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar-link {
    display: inline-block;
    margin: 5px;
  }
  
  .sidebar-link.active {
    border-right: none;
    border-bottom: 2px solid #409eff;
  }
}
</style>
