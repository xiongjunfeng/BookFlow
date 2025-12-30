<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <div class="register-header">
          <h2>用户注册</h2>
        </div>
      </template>
      <el-form :model="registerForm" :rules="rules" ref="registerFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请再次输入密码" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" :loading="loading">注册</el-button>
          <el-button @click="handleLoginRedirect">已有账号？去登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import { useData } from "vike-vue/useData";
import type { Data } from "./+data";

const registerFormRef = ref();
const loading = ref(false);
const { data } = useData<Data>();
const registerForm = ref(data?.initialFormData || {
  username: '',
  password: '',
  confirmPassword: ''
});

const validateConfirmPassword = (rule: any, value: string, callback: any) => {
  if (value !== registerForm.value.password) {
    callback(new Error('两次输入的密码不一致'));
  } else {
    callback();
  }
};

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
};

const handleRegister = async () => {
  if (!registerFormRef.value) return;
  
  await registerFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      loading.value = true;
      try {
        const { confirmPassword, ...userData } = registerForm.value;
        await axios.post('http://localhost:5000/api/auth/register', userData);
        ElMessage.success('注册成功');
        window.location.href = '/login';
      } catch (error: any) {
        console.error('注册错误详情:', error);
        const errorMessage = error.response?.data?.message 
          || error.response?.statusText 
          || error.message 
          || '注册失败';
        ElMessage.error(`注册失败: ${errorMessage}`);
      } finally {
        loading.value = false;
      }
    }
  });
};

const handleLoginRedirect = () => {
  window.location.href = '/login';
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.register-card {
  width: 400px;
}

.register-header {
  text-align: center;
}
</style>