// 测试localStorage中的token和用户状态
// 请在浏览器控制台中运行此脚本

console.log('=== localStorage 检查 ===');

// 检查token
const token = localStorage.getItem('token');
console.log('Token:', token ? `${token.substring(0, 20)}...` : 'null');

// 检查用户信息
const userStr = localStorage.getItem('user');
console.log('User string:', userStr);

if (userStr) {
  try {
    const user = JSON.parse(userStr);
    console.log('Parsed user:', user);
    console.log('User role:', user.role);
    console.log('User ID:', user.id);
  } catch (e) {
    console.log('解析用户信息失败:', e);
  }
}

// 列出所有localStorage键
console.log('\n=== 所有 localStorage 键 ===');
for (let i = 0; i < localStorage.length; i++) {
  const key = localStorage.key(i);
  const value = localStorage.getItem(key);
  console.log(`${key}: ${value?.substring(0, 50)}...`);
}

console.log('\n=== 建议的操作 ===');
console.log('1. 如果没有token，请先登录');
console.log('2. 检查用户角色是否为"user"');
console.log('3. 如果是admin，切换到普通用户账号');