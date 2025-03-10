<template>
  <div class="container">
    <el-card class="header-card">
      <div class="header-content">
        <el-icon class="header-icon"><Money /></el-icon>
        <h1>甲骨文老号价格查询系统</h1>
        <!-- 添加界面切换按钮 -->
        <el-button 
          type="text" 
          @click="toggleLayout" 
          class="layout-toggle"
        >
          <el-icon><Operation /></el-icon>
          {{ isNewLayout ? '切换到经典布局' : '切换到新布局' }}
        </el-button>
      </div>
    </el-card>

    <!-- 使用动态组件切换布局 -->
    <component :is="currentLayout"></component>
  </div>
</template>

<script>
import { Money, Operation } from '@element-plus/icons-vue'
import OldLayout from './AppOld.vue'
import NewLayout from './AppNew.vue'

export default {
  components: {
    Money,
    Operation,
    OldLayout,
    NewLayout
  },
  data() {
    return {
      isNewLayout: true,
    }
  },
  computed: {
    currentLayout() {
      return this.isNewLayout ? 'NewLayout' : 'OldLayout'
    }
  },
  methods: {
    toggleLayout() {
      this.isNewLayout = !this.isNewLayout
    }
  }
}
</script>

<style>
body {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
  margin: 0;
  padding: 20px;
  background-color: #f5f7fa;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.header-card {
  margin-bottom: 20px;
  text-align: center;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  position: relative;
}

.header-icon {
  font-size: 28px;
  color: #409EFF;
}

.header-card h1 {
  margin: 0;
  color: #303133;
  font-size: 24px;
}

.layout-toggle {
  position: absolute;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 5px;
}
</style>