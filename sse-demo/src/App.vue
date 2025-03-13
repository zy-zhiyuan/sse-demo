<template>
  <div id="app">
    <h1>DeepSeek 对话示例</h1>
    <div class="chat-box">
      <div v-for="(message, index) in messages" :key="index" class="message" :class="message.type">
        <deepseekIcon />
        <div class="bubble">
          <div class="text">{{ message.text }}</div>
        </div>
      </div>
    </div>
    <div class="input-box">
      <input v-model="userInput" placeholder="输入消息..." @keyup.enter="sendMessage" />
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import deepseekIcon from './components/icons/deepseekIcon.vue'

export default {
  name: 'App',
  setup() {
    // 使用 ref 创建响应式数据
    const messages = ref([]); // 存储消息
    const userInput = ref(''); // 用户输入
    let displayedMessage = ''; // 当前逐字显示的消息

    // 初始化 SSE 连接
    const initSSE = () => {
      const eventSource = new EventSource('http://localhost:5000/stream');

      // 监听消息事件
      eventSource.onmessage = (event) => {
        const char = event.data; // 逐字接收
        displayedMessage += char; // 追加到当前消息
        updateMessage(displayedMessage); // 更新显示
      };

      // 监听错误事件
      eventSource.onerror = (error) => {
        console.error('SSE 错误:', error);
        eventSource.close(); // 关闭连接
      };
    };

    // 更新消息
    const updateMessage = (text) => {
      if (messages.value.length === 0 || messages.value[messages.value.length - 1].type === 'user') {
        // 如果是新消息，添加到列表
        messages.value.push({
          text: text,
          type: 'system',
          avatar: 'https://via.placeholder.com/40/0078D7/FFFFFF?text=DS',
        });
      } else {
        // 如果是已有消息，更新内容
        messages.value[messages.value.length - 1].text = text;
      }
      scrollToBottom(); // 滚动到底部
    };

    // 发送用户输入
    const sendMessage = async () => {
      if (userInput.value.trim()) {
        // 添加用户消息
        messages.value.push({
          text: userInput.value,
          type: 'user',
          avatar: 'https://via.placeholder.com/40/4CAF50/FFFFFF?text=ME',
        });
        scrollToBottom(); // 滚动到底部

        // 发送到后端
        const response = await fetch('http://localhost:5000/send', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: userInput.value }),
        });

        if (response.ok) {
          console.log('消息发送成功');
        } else {
          console.error('消息发送失败');
        }

        userInput.value = ''; // 清空输入框
        displayedMessage = ''; // 重置逐字显示的消息
      }
    };

    // 滚动到底部
    const scrollToBottom = () => {
      const chatBox = document.querySelector('.chat-box');
      if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    };

    // 在组件挂载时初始化 SSE
    onMounted(() => {
      initSSE();
    });

    // 返回模板中需要使用的数据和方法
    return {
      messages,
      userInput,
      sendMessage,
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}

.chat-box {
  border: 1px solid #ccc;
  padding: 20px;
  width: 400px;
  height: 500px;
  margin: 0 auto;
  overflow-y: auto;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.message.system {
  justify-content: flex-start;
}

.message.user {
  justify-content: flex-end;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.bubble {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 10px;
  position: relative;
}

.message.system .bubble {
  background-color: #0078d7;
  color: white;
}

.message.user .bubble {
  background-color: #e1e1e1;
  color: black;
}

.message.system .bubble::after {
  content: '';
  position: absolute;
  left: -10px;
  top: 10px;
  width: 0;
  height: 0;
  border: 10px solid transparent;
  border-right-color: #0078d7;
}

.message.user .bubble::after {
  content: '';
  position: absolute;
  right: -10px;
  top: 10px;
  width: 0;
  height: 0;
  border: 10px solid transparent;
  border-left-color: #e1e1e1;
}

.text {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.input-box {
  margin-top: 20px;
}

input {
  width: 300px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 20px;
  margin-left: 10px;
  background-color: #0078d7;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #005bb5;
}
</style>