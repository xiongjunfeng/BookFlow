<template>
  <div class="books-container">
    <div class="books-header">
      <h2>图书列表</h2>
      <el-input
        v-model="searchQuery"
        placeholder="搜索图书"
        prefix-icon="Search"
        style="width: 300px;"
      />
    </div>
    
    <el-table :data="filteredBooks" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="书名" />
      <el-table-column prop="author" label="作者" />
      <el-table-column prop="stock" label="库存" width="80" />
      <el-table-column label="操作" width="180" v-if="isLoggedIn && !isAdmin">
        <template #default="scope">
          <el-button 
            type="primary" 
            size="small" 
            @click="handleBorrow(scope.row)"
            :disabled="scope.row.stock <= 0 || hasBorrowed(scope.row.id)"
          >
            借阅
          </el-button>
          <el-button 
            type="success" 
            size="small" 
            @click="handleReturn(scope.row)"
            :disabled="!hasBorrowed(scope.row.id)"
          >
            归还
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 图书借阅记录弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      title="我的借阅记录"
      width="50%"
      v-if="!isAdmin"
    >
      <el-table :data="userBorrowRecords" style="width: 100%">
        <el-table-column prop="book_id" label="图书ID" width="80" />
        <el-table-column label="书名" width="200">
          <template #default="scope">{{ getBookTitle(scope.row.book_id) }}</template>
        </el-table-column>
        <el-table-column prop="borrow_date" label="借阅日期" width="180" />
        <el-table-column prop="return_date" label="归还日期" width="180" />
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.return_date ? 'success' : 'warning'">
              {{ scope.row.return_date ? '已归还' : '借阅中' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';

const books = ref([]);
const searchQuery = ref('');
const dialogVisible = ref(false);
const userBorrowRecords = ref([]);

// 检查用户是否登录
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

// 过滤图书列表
const filteredBooks = computed(() => {
  if (!searchQuery.value) return books.value;
  return books.value.filter(book => 
    book.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    book.author.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// 获取图书列表
const fetchBooks = async () => {
  try {
    const token = localStorage.getItem('token');
    const config: any = {};
    if (token) {
      config.headers = { Authorization: `Bearer ${token}` };
    }
    console.log('Fetching books with config:', config);
    const response = await axios.get('http://localhost:5000/api/books/', config);
    console.log('Books response:', response.data);
    books.value = response.data.books || [];
    console.log('Books value after assignment:', books.value);
  } catch (error: any) {
    console.error('Error fetching books:', error);
    console.error('Error response:', error.response);
    ElMessage.error('获取图书列表失败: ' + (error.message || '未知错误'));
    books.value = [];
  }
};

// 获取用户借阅记录
const fetchUserBorrowRecords = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://localhost:5000/api/borrow/records/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    userBorrowRecords.value = response.data.records;
  } catch (error: any) {
    ElMessage.error('获取借阅记录失败');
  }
};

// 借阅图书
const handleBorrow = async (book) => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.post('http://localhost:5000/api/borrow', 
      { book_id: book.id },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    ElMessage.success('借阅成功');
    fetchBooks();
    fetchUserBorrowRecords();
  } catch (error: any) {
    ElMessage.error(error.response?.data?.message || '借阅失败');
  }
};

// 归还图书
const handleReturn = async (book) => {
  try {
    // 找到对应的借阅记录ID
    const borrowRecord = userBorrowRecords.value.find(record => 
      record.book_id === book.id && !record.return_date
    );
    
    if (!borrowRecord) {
      ElMessage.error('未找到待归还的借阅记录');
      return;
    }
    
    const token = localStorage.getItem('token');
    await axios.put(`http://localhost:5000/api/borrow/return/${borrowRecord.id}`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    ElMessage.success('归还成功');
    fetchBooks();
    fetchUserBorrowRecords();
  } catch (error: any) {
    ElMessage.error(error.response?.data?.message || '归还失败');
  }
};

// 检查用户是否借阅了该书
const hasBorrowed = (bookId) => {
  return userBorrowRecords.value.some(record => 
    record.book_id === bookId && !record.return_date
  );
};

// 根据图书ID获取书名
const getBookTitle = (bookId) => {
  const book = books.value.find(book => book.id === bookId);
  return book ? book.title : '';
};

// 初始化数据
onMounted(() => {
  fetchBooks();
  fetchUserBorrowRecords();
});
</script>

<style scoped>
.books-container {
  padding: 20px;
}

.books-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.books-header h2 {
  margin: 0;
}
</style>