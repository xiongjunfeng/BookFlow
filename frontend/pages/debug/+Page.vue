<template>
  <div class="debug-container">
    <h2>前端调试工具</h2>
    
    <div class="debug-section">
      <h3>localStorage 检查</h3>
      <button @click="checkLocalStorage">检查 localStorage</button>
      <pre>{{ localStorageInfo }}</pre>
    </div>
    
    <div class="debug-section">
      <h3>图书数据检查</h3>
      <button @click="checkBooksData">检查图书数据</button>
      <div v-if="booksInfo">
        <p>图书数量: {{ booksInfo.count }}</p>
        <p>前3本图书:</p>
        <ul>
          <li v-for="book in booksInfo.sample" :key="book.id">
            {{ book.title }} - 库存: {{ book.stock }}
          </li>
        </ul>
      </div>
    </div>
    
    <div class="debug-section">
      <h3>借阅记录检查</h3>
      <button @click="checkBorrowRecords">检查借阅记录</button>
      <div v-if="borrowInfo">
        <p>借阅记录数量: {{ borrowInfo.count }}</p>
        <p>当前借阅的图书:</p>
        <ul>
          <li v-for="record in borrowInfo.current" :key="record.id">
            图书ID: {{ record.book_id }}, 状态: {{ record.status }}
          </li>
        </ul>
      </div>
    </div>
    
    <div class="debug-section">
      <h3>测试借阅功能</h3>
      <button @click="testBorrow" :disabled="testing">测试借阅</button>
      <p v-if="testResult">{{ testResult }}</p>
    </div>
    
    <div class="debug-section">
      <h3>网络请求测试</h3>
      <button @click="testNetwork">测试网络请求</button>
      <pre>{{ networkResult }}</pre>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';

const localStorageInfo = ref('');
const booksInfo = ref<any>(null);
const borrowInfo = ref<any>(null);
const testResult = ref('');
const networkResult = ref('');
const testing = ref(false);

// 检查localStorage
const checkLocalStorage = () => {
  const token = localStorage.getItem('token');
  const user = localStorage.getItem('user');
  
  let info = `Token: ${token ? token.substring(0, 20) + '...' : 'null'}\n`;
  info += `User: ${user || 'null'}\n`;
  
  if (user) {
    try {
      const userObj = JSON.parse(user);
      info += `User Role: ${userObj.role}\n`;
      info += `User ID: ${userObj.id}\n`;
    } catch (e) {
      info += '解析用户信息失败\n';
    }
  }
  
  localStorageInfo.value = info;
};

// 检查图书数据
const checkBooksData = async () => {
  try {
    const token = localStorage.getItem('token');
    const config: any = {};
    if (token) {
      config.headers = { Authorization: `Bearer ${token}` };
    }
    
    const response = await axios.get('http://localhost:5000/api/books/', config);
    const books = response.data.books || [];
    
    booksInfo.value = {
      count: books.length,
      sample: books.slice(0, 3)
    };
  } catch (error: any) {
    console.error('获取图书数据失败:', error);
    ElMessage.error('获取图书数据失败');
  }
};

// 检查借阅记录
const checkBorrowRecords = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      ElMessage.error('未登录');
      return;
    }
    
    const response = await axios.get('http://localhost:5000/api/borrow/records/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    const records = response.data.records || [];
    const current = records.filter((record: any) => record.status === 'borrowed');
    
    borrowInfo.value = {
      count: records.length,
      current: current
    };
  } catch (error: any) {
    console.error('获取借阅记录失败:', error);
    ElMessage.error('获取借阅记录失败');
  }
};

// 测试借阅功能
const testBorrow = async () => {
  testing.value = true;
  testResult.value = '测试中...';
  
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      testResult.value = '未登录';
      return;
    }
    
    // 获取图书列表
    const booksResponse = await axios.get('http://localhost:5000/api/books/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    const books = booksResponse.data.books || [];
    
    // 找一本有库存且未借阅的书
    const borrowResponse = await axios.get('http://localhost:5000/api/borrow/records/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    const records = borrowResponse.data.records || [];
    const borrowedBookIds = records.filter((r: any) => r.status === 'borrowed').map((r: any) => r.book_id);
    
    const availableBook = books.find((book: any) => 
      book.stock > 0 && !borrowedBookIds.includes(book.id)
    );
    
    if (!availableBook) {
      testResult.value = '没有可借阅的图书';
      return;
    }
    
    testResult.value = `尝试借阅: ${availableBook.title}`;
    
    // 尝试借阅
    const response = await axios.post('http://localhost:5000/api/borrow', 
      { book_id: availableBook.id },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    
    if (response.status === 201) {
      testResult.value = `✅ 借阅成功! 状态码: ${response.status}`;
    } else {
      testResult.value = `❌ 借阅失败. 状态码: ${response.status}, 响应: ${response.data}`;
    }
    
  } catch (error: any) {
    testResult.value = `❌ 借阅测试失败: ${error.response?.data?.message || error.message}`;
  } finally {
    testing.value = false;
  }
};

// 测试网络请求
const testNetwork = async () => {
  networkResult.value = '测试中...';
  
  try {
    const token = localStorage.getItem('token');
    
    // 测试基本的API连接
    const response = await axios.get('http://localhost:5000/api/books/', {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    });
    
    networkResult.value = `✅ API连接正常\n状态码: ${response.status}\n图书数量: ${response.data.books?.length || 0}`;
  } catch (error: any) {
    networkResult.value = `❌ 网络请求失败\n错误: ${error.message}\n状态码: ${error.response?.status}`;
  }
};
</script>

<style scoped>
.debug-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.debug-section {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.debug-section h3 {
  margin-top: 0;
  color: #333;
}

button {
  background-color: #409eff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 10px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

pre {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}
</style>