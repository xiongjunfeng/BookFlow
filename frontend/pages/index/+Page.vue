<template>
  <div class="home-container">
    <el-card class="home-card">
      <template #header>
        <div class="card-header">
          <h1>图书管理系统</h1>
        </div>
      </template>
      <div class="card-content">
        <p>欢迎使用图书管理系统，这是一个基于Vue 3和Flask的前后端分离项目。</p>
        <div class="home-actions">
          <el-button type="primary" @click="navigateToBooks">查看图书列表</el-button>
          <el-button @click="navigateToLogin" v-if="!isLoggedIn">登录</el-button>
          <el-button @click="navigateToRegister" v-if="!isLoggedIn">注册</el-button>
          <el-button type="warning" @click="handleLogout" v-if="isLoggedIn">登出</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { ElMessage } from 'element-plus';

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('token');
});

const navigateToBooks = () => {
  window.location.href = '/books';
};

const navigateToLogin = () => {
  window.location.href = '/login';
};

const navigateToRegister = () => {
  window.location.href = '/register';
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  ElMessage.success('登出成功');
  window.location.href = '/';
};
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.home-card {
  max-width: 600px;
  margin: 0 auto;
}

.card-header {
  text-align: center;
}

.card-content {
  text-align: center;
  padding: 20px 0;
}

.home-actions {
  margin-top: 30px;
}

.home-actions .el-button {
  margin: 0 10px;
}
</style>
