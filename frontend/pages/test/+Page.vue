<template>
  <div class="test-container">
    <h2>借阅功能测试页面</h2>
    
    <div class="user-info">
      <h3>用户信息</h3>
      <p><strong>登录状态:</strong> {{ isLoggedIn ? '已登录' : '未登录' }}</p>
      <p v-if="user"><strong>用户名:</strong> {{ user.username }}</p>
      <p v-if="user"><strong>角色:</strong> {{ user.role }}</p>
    </div>
    
    <div class="books-section">
      <h3>图书列表</h3>
      <button @click="fetchBooks" :disabled="loading">刷新图书列表</button>
      <div v-if="loading">加载中...</div>
      <div v-else-if="books.length === 0">暂无图书数据</div>
      <div v-else>
        <table border="1" style="width: 100%; margin-top: 10px;">
          <thead>
            <tr>
              <th>ID</th>
              <th>书名</th>
              <th>库存</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in books.slice(0, 5)" :key="book.id">
              <td>{{ book.id }}</td>
              <td>{{ book.title }}</td>
              <td>{{ book.stock }}</td>
              <td>
                <button 
                  @click="borrowBook(book)" 
                  :disabled="!isLoggedIn || book.stock <= 0 || isBorrowed(book.id)"
                >
                  {{ isBorrowed(book.id) ? '已借阅' : '借阅' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <p>显示前5本图书，共{{ books.length }}本</p>
      </div>
    </div>
    
    <div class="borrows-section">
      <h3>我的借阅记录</h3>
      <button @click="fetchBorrowRecords" :disabled="loading || !isLoggedIn">刷新借阅记录</button>
      <div v-if="!isLoggedIn">请先登录</div>
      <div v-else-if="loading">加载中...</div>
      <div v-else-if="borrowRecords.length === 0">暂无借阅记录</div>
      <div v-else>
        <table border="1" style="width: 100%; margin-top: 10px;">
          <thead>
            <tr>
              <th>图书ID</th>
              <th>状态</th>
              <th>借阅日期</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in borrowRecords" :key="record.id">
              <td>{{ record.book_id }}</td>
              <td>{{ record.status }}</td>
              <td>{{ formatDate(record.borrow_date) }}</td>
              <td>
                <button 
                  @click="returnBook(record)" 
                  :disabled="record.status === 'returned'"
                >
                  {{ record.status === 'returned' ? '已归还' : '归还' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div class="logs-section">
      <h3>操作日志</h3>
      <div class="logs" style="background: #f5f5f5; padding: 10px; height: 200px; overflow-y: auto;">
        <div v-for="(log, index) in logs" :key="index">{{ log }}</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const books = ref([]);
const borrowRecords = ref([]);
const loading = ref(false);
const logs = ref([]);

// 计算属性
const isLoggedIn = computed(() => {
  return !!localStorage.getItem('token');
});

const user = computed(() => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
});

// 日志记录
const addLog = (message: string) => {
  const timestamp = new Date().toLocaleTimeString();
  logs.value.unshift(`[${timestamp}] ${message}`);
  console.log(message);
};

// 检查是否已借阅
const isBorrowed = (bookId: number) => {
  return borrowRecords.value.some(record => 
    record.book_id === bookId && record.status === 'borrowed'
  );
};

// 格式化日期
const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString();
};

// 获取图书列表
const fetchBooks = async () => {
  loading.value = true;
  addLog('开始获取图书列表...');
  
  try {
    const token = localStorage.getItem('token');
    const config: any = {};
    if (token) {
      config.headers = { Authorization: `Bearer ${token}` };
    }
    
    const response = await axios.get('http://localhost:5000/api/books/', config);
    books.value = response.data.books || [];
    addLog(`✅ 获取图书列表成功，共${books.value.length}本`);
  } catch (error: any) {
    addLog(`❌ 获取图书列表失败: ${error.message}`);
    console.error('获取图书列表失败:', error);
  } finally {
    loading.value = false;
  }
};

// 获取借阅记录
const fetchBorrowRecords = async () => {
  if (!isLoggedIn.value) {
    addLog('⚠️ 未登录，跳过获取借阅记录');
    return;
  }
  
  loading.value = true;
  addLog('开始获取借阅记录...');
  
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://localhost:5000/api/borrow/records/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    borrowRecords.value = response.data.records || [];
    addLog(`✅ 获取借阅记录成功，共${borrowRecords.value.length}条`);
  } catch (error: any) {
    addLog(`❌ 获取借阅记录失败: ${error.message}`);
    console.error('获取借阅记录失败:', error);
  } finally {
    loading.value = false;
  }
};

// 借阅图书
const borrowBook = async (book: any) => {
  addLog(`开始借阅图书: ${book.title} (ID: ${book.id})`);
  
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      addLog('❌ 未登录，无法借阅');
      return;
    }
    
    const response = await axios.post('http://localhost:5000/api/borrow', 
      { book_id: book.id },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    
    if (response.status === 201) {
      addLog(`✅ 借阅成功! 状态码: ${response.status}`);
      // 刷新数据
      await fetchBooks();
      await fetchBorrowRecords();
    } else {
      addLog(`❌ 借阅失败，状态码: ${response.status}`);
    }
  } catch (error: any) {
    addLog(`❌ 借阅失败: ${error.response?.data?.message || error.message}`);
    console.error('借阅失败:', error);
  }
};

// 归还图书
const returnBook = async (record: any) => {
  addLog(`开始归还图书 ID: ${record.book_id}`);
  
  try {
    const token = localStorage.getItem('token');
    const response = await axios.put(`http://localhost:5000/api/borrow/return/${record.id}`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    
    if (response.status === 200) {
      addLog(`✅ 归还成功! 状态码: ${response.status}`);
      // 刷新数据
      await fetchBooks();
      await fetchBorrowRecords();
    } else {
      addLog(`❌ 归还失败，状态码: ${response.status}`);
    }
  } catch (error: any) {
    addLog(`❌ 归还失败: ${error.response?.data?.message || error.message}`);
    console.error('归还失败:', error);
  }
};

// 初始化
onMounted(async () => {
  addLog('🚀 页面初始化开始');
  
  if (isLoggedIn.value) {
    addLog(`👤 已登录用户: ${user.value?.username}`);
    await fetchBorrowRecords();
  } else {
    addLog('⚠️ 用户未登录');
  }
  
  await fetchBooks();
  addLog('✅ 页面初始化完成');
});
</script>

<style scoped>
.test-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.user-info, .books-section, .borrows-section, .logs-section {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  background-color: #409eff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

table {
  border-collapse: collapse;
}

th, td {
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f5f5f5;
}
</style>