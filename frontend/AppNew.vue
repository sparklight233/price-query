<template>
  <div class="container">
    <div class="main-content">
      <!-- 左侧筛选面板 -->
      <el-card class="filter-panel">
        <template #header>
          <div class="filter-header">
            <el-icon><Filter /></el-icon>
            <span>筛选条件</span>
          </div>
        </template>
        
        <div class="filter-section">
          <div class="filter-row">
            <div class="filter-item keyword-filter">
              <span class="label">地区</span>
              <div class="search-row">
                <el-input 
                  v-model="searchInput" 
                  placeholder="输入关键词" 
                  clearable
                  class="keyword-input"
                ></el-input>
                <el-button type="primary" @click="searchLocation" class="action-button-small">
                  <el-icon><Search /></el-icon>
                </el-button>
                <el-button @click="resetFilters" class="action-button-small">
                  <el-icon><RefreshRight /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
          
          <div class="filter-row">
            <div class="filter-item">
              <span class="label">出售价格(￥)</span>
              <div class="price-filter">
                <el-input-number v-model="minPrice" placeholder="低" :min="0" controls-position="right" size="default" :controls="false" class="small-input-number"></el-input-number>
                <span class="price-separator">至</span>
                <el-input-number v-model="maxPrice" placeholder="高" :min="0" controls-position="right" size="default" :controls="false" class="small-input-number"></el-input-number>
              </div>
            </div>
          </div>
          
          <div class="filter-row">
            <div class="filter-item">
              <span class="label">账号时间(天)</span>
              <div class="price-filter">
                <el-input-number v-model="minTime" placeholder="低" :min="0" controls-position="right" size="default" :controls="false" class="small-input-number"></el-input-number>
                <span class="price-separator">至</span>
                <el-input-number v-model="maxTime" placeholder="高" :min="0" controls-position="right" size="default" :controls="false" class="small-input-number"></el-input-number>
              </div>
            </div>
          </div>
          
          <div class="filter-row">
            <div class="filter-item">
              <span class="label">出售日期</span>
              <div class="date-range-container">
                <el-date-picker
                  v-model="startDateValue"
                  type="date"
                  placeholder="开始日期"
                  format="YYYY-MM-DD"
                  value-format="YYYY-MM-DD"
                  class="date-picker"
                  @change="updateDateRange"
                ></el-date-picker>
                <span class="date-separator">至</span>
                <el-date-picker
                  v-model="endDateValue"
                  type="date"
                  placeholder="结束日期"
                  format="YYYY-MM-DD"
                  value-format="YYYY-MM-DD"
                  class="date-picker"
                  @change="updateDateRange"
                ></el-date-picker>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 关于区域 -->
        <div class="about-section">
          <el-divider></el-divider>
          <div class="social-links">
            <a href="https://github.com/sparklight233" target="_blank" class="social-link" title="GitHub">
              <el-button circle>
                <el-icon><Link /></el-icon>
              </el-button>
            </a>
            <a href="https://zeaurx.com" target="_blank" class="social-link" title="博客">
              <el-button circle>
                <el-icon><Document /></el-icon>
              </el-button>
            </a>
            <a href="https://linux.do/u/ggsmida/summary" target="_blank" class="social-link" title="Linux.do">
              <el-button circle>
                <el-icon><Monitor /></el-icon>
              </el-button>
            </a>
            <el-popover
              placement="top"
              :width="200"
              trigger="click"
            >
              <template #reference>
                <el-button circle class="social-link" title="邮箱">
                  <el-icon><Message /></el-icon>
                </el-button>
              </template>
              <div style="text-align: center;">admin@zeaurx.com</div>
            </el-popover>
          </div>
        </div>

      </el-card>

      <!-- 右侧结果显示 -->
      <el-card class="results-panel">
        <template #header>
          <div class="results-header">
            <el-icon><List /></el-icon>
            <span>查询结果</span>
          </div>
        </template>
        
        <el-table
          :data="pageData"
          style="width: 100%"
          border
          stripe
          highlight-current-row
          empty-text="没有找到匹配的记录"
          :max-height="tableHeight"
        >
          <el-table-column prop="地区" label="地区" sortable @sort-change="onSortChange" show-overflow-tooltip min-width="200"></el-table-column>
          <el-table-column prop="价格" label="价格(￥)" sortable @sort-change="onSortChange" min-width="120"></el-table-column>
          <el-table-column prop="账号时间" label="账号时间(天)" sortable @sort-change="onSortChange" min-width="150"></el-table-column>
          <el-table-column prop="出售日期" label="出售日期" sortable @sort-change="onSortChange" min-width="150"></el-table-column>
          <el-table-column prop="备注" label="备注" show-overflow-tooltip min-width="250"></el-table-column>
        </el-table>
        
        <div class="pagination-container">
          <el-pagination
            background
            layout="total, prev, pager, next"
            :total="filteredData.length"
            :page-size="itemsPerPage"
            :current-page="currentPage"
            @current-change="handleCurrentChange"
          >
          </el-pagination>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { Money, Search, RefreshRight, Filter, List, Link, Document, Monitor, Message } from '@element-plus/icons-vue'

export default {
  components: {
    Money,
    Search,
    RefreshRight,
    Filter,
    List,
    Link,
    Document,
    Monitor,
    Message
  },
  data() {
    return {
      searchInput: '',
      minPrice: '',
      maxPrice: '',
      minTime: '',
      maxTime: '',
      dateRange: [],
      startDateValue: '',
      endDateValue: '',
      allData: [],
      filteredData: [],
      currentPage: 1,
      itemsPerPage: 10,
      currentSort: {
        column: '出售日期',
        ascending: false
      },
      tableHeight: 600
    }
  },
  computed: {
    pageData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredData.slice(start, end);
    },
    startDate() {
      return this.dateRange && this.dateRange.length > 0 ? this.dateRange[0] : '';
    },
    endDate() {
      return this.dateRange && this.dateRange.length > 0 ? this.dateRange[1] : '';
    }
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch('/api/data');
        this.allData = await response.json();
        this.filteredData = [...this.allData];
        this.initializeDateInputs();
        this.sortData();
      } catch (error) {
        console.error('Error loading data:', error);
      }
    },
    updateDateRange() {
      if (this.startDateValue && this.endDateValue) {
        this.dateRange = [this.startDateValue, this.endDateValue];
      } else if (this.startDateValue) {
        this.dateRange = [this.startDateValue, new Date().toISOString().split('T')[0]];
      } else if (this.endDateValue) {
        this.dateRange = ['1970-01-01', this.endDateValue];
      } else {
        this.dateRange = [];
      }
    },
    initializeDateInputs() {
      const dates = this.filteredData.map(item => new Date(item.出售日期));
      const minDate = new Date(Math.min(...dates));
      const maxDate = new Date();
      
      this.startDateValue = minDate.toISOString().split('T')[0];
      this.endDateValue = maxDate.toISOString().split('T')[0];
      this.dateRange = [this.startDateValue, this.endDateValue];
    },
    resetFilters() {
      this.searchInput = '';
      this.minPrice = '';
      this.maxPrice = '';
      this.minTime = '';
      this.maxTime = '';
      this.initializeDateInputs();
      
      this.filteredData = [...this.allData];
      this.currentPage = 1;
      this.sortData();
    },
    searchLocation() {
      const keyword = this.searchInput.toLowerCase();
      const minPrice = Number(this.minPrice) || 0;
      const maxPrice = Number(this.maxPrice) || Infinity;
      const minTime = Number(this.minTime) || 0;
      const maxTime = Number(this.maxTime) || Infinity;
      
      this.filteredData = this.allData.filter(item => {
        const matchesKeyword = item.地区.toLowerCase().includes(keyword);
        const price = Number(item.价格);
        const matchesPrice = price >= minPrice && price <= maxPrice;
        
        const time = Number(item.账号时间);
        const matchesTime = time >= minTime && time <= maxTime;
        
        const itemDate = new Date(item.出售日期);
        const start = this.startDate ? new Date(this.startDate) : new Date(0);
        const end = this.endDate ? new Date(this.endDate) : new Date();
        
        start.setHours(0, 0, 0, 0);
        end.setHours(23, 59, 59, 999);
        
        const matchesDate = itemDate >= start && itemDate <= end;

        return matchesKeyword && matchesPrice && matchesTime && matchesDate;
      });

      this.currentPage = 1;
      this.sortData();
    },
    sortData() {
      this.filteredData.sort((a, b) => {
        let compareResult;
        if (this.currentSort.column === '出售日期') {
          compareResult = new Date(a[this.currentSort.column]) - new Date(b[this.currentSort.column]);
        } else if (this.currentSort.column === '价格' || this.currentSort.column === '账号时间') {
          compareResult = Number(a[this.currentSort.column]) - Number(b[this.currentSort.column]);
        } else {
          compareResult = String(a[this.currentSort.column]).localeCompare(String(b[this.currentSort.column]));
        }
        return this.currentSort.ascending ? compareResult : -compareResult;
      });
    },
    onSortChange({ prop, order }) {
      if (prop) {
        this.currentSort.column = prop;
        this.currentSort.ascending = order === 'ascending';
        this.sortData();
      }
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    handleSizeChange(val) {
      this.itemsPerPage = val;
      this.currentPage = 1;
    },
    calculateTableHeight() {
      const windowHeight = window.innerHeight;
      this.tableHeight = windowHeight - 200;
    }
  },
  mounted() {
    this.fetchData();
    this.calculateTableHeight();
    window.addEventListener('resize', this.calculateTableHeight);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.calculateTableHeight);
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

.main-content {
  display: flex;
  gap: 20px;
  min-height: calc(100vh - 150px);
}

.filter-panel {
  width: 320px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.results-panel {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.filter-header, .results-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.filter-item {
  margin-bottom: 5px;
  width: 100%;
}

.keyword-filter {
  width: 100%;
}

.label {
  display: block;
  font-size: 16px;
  font-weight: bold;
  color: #606266;
  margin-bottom: 20px;
}

.keyword-input {
  width: 120px; /* 使用固定宽度 */
}

.search-row {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.price-filter {
  display: flex;
  align-items: center;
  width: 100%;
}

.small-input-number {
  width: 140px !important;
}

.price-separator {
  margin: 0 10px;
  color: #909399;
}

.date-range-container {
  display: flex;
  align-items: center;
  gap: 4px;
  width: 100%;
}

.date-picker {
  width: 140px !important;
}

.date-separator {
  color: #909399;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.el-table th {
  background-color: #f5f7fa !important;
}

.el-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05) !important;
}

.date-range-container {
  width: 100%;
}

.about-section {
  margin-top: auto;
  padding-top: 20px;
}

.about-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
}

.about-card {
  border-radius: 8px;
  transition: all 0.3s;
}

.about-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
}

.about-content {
  text-align: center;
  color: #606266;
  font-size: 14px;
  padding: 10px;
}

.about-content p {
  margin: 8px 0;
}

.search-row {
  display: flex;
  align-items: center;
  gap: 20px;
  width: 100%;
}

.action-button-small {
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.action-button-small:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.button-row-search {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
  margin-top: 8px;
}

.action-button-search {
  flex: 1;
  padding: 8px 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  transition: all 0.3s;
}

.action-button-search:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin: 15px 0;
}

.social-link {
  text-decoration: none;
  transition: all 0.3s;
}

.social-link:hover {
  transform: translateY(-2px);
}

.blog-logo {
  margin: 15px auto;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.blog-logo:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.blog-icon {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.copyright {
  font-size: 12px;
  color: #909399;
  margin-top: 15px;
}

.el-table {
  --el-table-header-bg-color: #f5f7fa;
  --el-table-row-hover-bg-color: #ecf5ff;
}

.el-table .el-table__cell {
  padding: 8px 0; 
}

.results-panel {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  padding: 15px 0;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .filter-panel {
    width: 100%;
    margin-bottom: 20px;
  }
  
  .filter-row {
    flex-direction: column;
  }
  
  .button-group {
    margin-top: 5px;
  }
  
  .about-section {
    margin-top: 20px;
  }
}

.button-row {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
}

.action-button {
  min-width: 100px;
  padding: 10px 20px;
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.el-input, .el-input-number, .el-date-picker {
  transition: all 0.3s;
}

.el-input:hover, .el-input-number:hover, .el-date-picker:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.el-table {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.el-card {
  transition: all 0.3s;
}

.el-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
}
</style>
