<!-- https://vike.dev/Layout -->

<template>
  <div class="layout">
    <Sidebar v-if="isDesktop">
      <Logo />
      <Link href="/"> 首页 </Link>
      <Link href="/books"> 图书列表 </Link>
      <Link href="/borrow" v-if="isLoggedIn && !isAdmin"> 我的借阅 </Link>
      <Link href="/login" v-if="!isLoggedIn"> 登录 </Link>
      <Link href="/register" v-if="!isLoggedIn"> 注册 </Link>
      <div class="user-info" v-if="isLoggedIn">欢迎，{{ currentUsername }}</div>
      <Link href="/" @click="handleLogout" v-if="isLoggedIn"> 登出 </Link>
    </Sidebar>
    <Content><slot /></Content>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, onMounted, onUnmounted } from 'vue';
import Content from "../components/Content.vue";
import Link from "../components/Link.vue";
import Logo from "../components/Logo.vue";
import Sidebar from "../components/Sidebar.vue";

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('token');
});

// 检查用户是否为管理员
const isAdmin = computed(() => {
  const userStr = localStorage.getItem('user');
  if (userStr) {
    try {
      const user = JSON.parse(userStr);
      return user.role === 'admin';
    } catch (e) {
      return false;
    }
  }
  return false;
});

// 获取当前用户信息
const currentUser = computed(() => {
  const userStr = localStorage.getItem('user');
  if (userStr) {
    try {
      return JSON.parse(userStr);
    } catch (e) {
      return null;
    }
  }
  return null;
});

// 获取当前用户名
const currentUsername = computed(() => {
  return currentUser.value?.username || '用户';
});

// 使用ref存储窗口宽度以实现响应式
const windowWidth = ref(window.innerWidth);

const isDesktop = computed(() => {
  return windowWidth.value >= 768;
});

const handleResize = () => {
  windowWidth.value = window.innerWidth;
};

const handleLogout = (event: MouseEvent) => {
  event.preventDefault();
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  window.location.href = '/';
};

onMounted(() => {
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});
</script>

<style>
body {
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}
* {
  box-sizing: border-box;
}
a {
  text-decoration: none;
}
</style>

<style scoped>
.layout {
  display: flex;
  max-width: 1200px;
  margin: auto;
}

.content {
  padding: 20px;
  padding-bottom: 50px;
  min-height: 100vh;
  flex-grow: 1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .layout {
    flex-direction: column;
  }
}

.user-info {
  padding: 10px 20px;
  color: #606266;
  font-size: 14px;
  font-weight: 500;
  border-top: 1px solid #ebeef5;
  border-bottom: 1px solid #ebeef5;
  margin: 10px 0;
}

/* Page Transition Animation */
#page-content {
  opacity: 1;
  transition: opacity 0.3s ease-in-out;
}
body.page-transition #page-content {
  opacity: 0;
}
</style>
