<template>
  <div class="borrow-container">
    <div class="borrow-header">
      <h2>我的借阅列表</h2>
    </div>
    
    <el-table :data="borrowRecords" style="width: 100%" v-loading="loading">
      <el-table-column prop="book_id" label="图书ID" width="80" />
      <el-table-column label="书名" width="200">
        <template #default="scope">{{ getBookTitle(scope.row.book_id) }}</template>
      </el-table-column>
      <el-table-column label="作者" width="150">
        <template #default="scope">{{ getBookAuthor(scope.row.book_id) }}</template>
      </el-table-column>
      <el-table-column prop="borrow_date" label="借阅日期" width="180" />
      <el-table-column prop="return_date" label="归还日期" width="180" />
      <el-table-column label="状态" width="120">
        <template #default="scope">
          <el-tag :type="scope.row.status === 'returned' ? 'success' : 'warning'">
            {{ scope.row.status === 'returned' ? '已归还' : '借阅中' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120" v-if="isLoggedIn">
        <template #default="scope">
          <el-button 
            type="success" 
            size="small" 
            @click="handleReturn(scope.row)"
            :disabled="scope.row.status === 'returned'"
          >
            归还
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页组件 -->
    <div class="pagination-container" v-if="total > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';

const borrowRecords = ref([]);
const books = ref([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 检查用户是否登录
const isLoggedIn = computed(() => {
  return !!localStorage.getItem('token');
});

// 获取借阅记录
const fetchBorrowRecords = async () => {
  if (!isLoggedIn.value) return;
  
  loading.value = true;
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://localhost:5000/api/borrow/records/', {
      headers: { Authorization: `Bearer ${token}` },
      params: {
        page: currentPage.value,
        per_page: pageSize.value
      }
    });
    
    borrowRecords.value = response.data.records;
    total.value = response.data.total;
  } catch (error: any) {
    ElMessage.error(error.response?.data?.message || '获取借阅记录失败');
  } finally {
    loading.value = false;
  }
};

// 获取所有图书信息（用于显示书名）
const fetchBooks = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/books/');
    books.value = response.data.books || [];
  } catch (error: any) {
    console.error('获取图书信息失败:', error);
  }
};

// 根据图书ID获取书名
const getBookTitle = (bookId) => {
  const book = books.value.find(book => book.id === bookId);
  return book ? book.title : '';
};

// 根据图书ID获取作者
const getBookAuthor = (bookId) => {
  const book = books.value.find(book => book.id === bookId);
  return book ? book.author : '';
};

// 归还图书
const handleReturn = async (record) => {
  try {
    const token = localStorage.getItem('token');
    await axios.put(`http://localhost:5000/api/borrow/return/${record.id}`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    ElMessage.success('归还成功');
    fetchBorrowRecords();
    fetchBooks(); // 更新图书库存
  } catch (error: any) {
    ElMessage.error(error.response?.data?.message || '归还失败');
  }
};

// 分页大小变化
const handleSizeChange = (val) => {
  pageSize.value = val;
  fetchBorrowRecords();
};

// 当前页变化
const handleCurrentChange = (val) => {
  currentPage.value = val;
  fetchBorrowRecords();
};

// 初始化数据
onMounted(() => {
  if (isLoggedIn.value) {
    fetchBooks();
    fetchBorrowRecords();
  }
});
</script>

<style scoped>
.borrow-container {
  padding: 20px;
}

.borrow-header {
  margin-bottom: 20px;
}

.borrow-header h2 {
  margin: 0;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>