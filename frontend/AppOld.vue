<template>
  <div class="container">
    <el-card class="search-container">
      <div class="search-panel">
        <div class="search-row">
          <!-- 地区搜索 -->
          <div class="search-item keyword-search">
            <span class="label">地区</span>
            <el-input 
              v-model="searchInput" 
              placeholder="输入关键词" 
              clearable
              class="keyword-input"
            ></el-input>
          </div>
          
          <div class="search-item price-search">
            <span class="label">出售价格(￥)</span>
            <div class="price-filter">
              <el-input-number v-model="minPrice" placeholder="最低" :min="0" controls-position="right" size="default" :controls="false"></el-input-number>
              <span class="price-separator">至</span>
              <el-input-number v-model="maxPrice" placeholder="最高" :min="0" controls-position="right" size="default" :controls="false"></el-input-number>
            </div>
          </div>
          
          <!-- 账号时间 -->
          <div class="search-item time-search">
            <span class="label">账号时间(天)</span>
            <div class="time-filter">
              <el-input-number v-model="minTime" placeholder="最短时间" :min="0" controls-position="right" size="default" :controls="false"></el-input-number>
              <span class="time-separator">至</span>
              <el-input-number v-model="maxTime" placeholder="最长时间" :min="0" controls-position="right" size="default" :controls="false"></el-input-number>
            </div>
          </div>
          
          <!-- 出售日期 -->
          <div class="search-item date-search">
            <span class="label">出售日期</span>
            <div class="date-range-container">
              <el-date-picker
                v-model="startDateValue"
                type="date"
                placeholder="开始日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                class="single-date-picker"
                @change="updateDateRange"
              ></el-date-picker>
              <span class="date-separator">至</span>
              <el-date-picker
                v-model="endDateValue"
                type="date"
                placeholder="结束日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                class="single-date-picker"
                @change="updateDateRange"
              ></el-date-picker>
            </div>
          </div>
          
          <!-- 搜索和重置按钮 -->
          <div class="search-item button-search">
            <span class="label">&nbsp;</span>
            <div class="button-group">
              <el-button type="primary" @click="searchLocation" class="action-button-small">
                <el-icon><Search /></el-icon>
              </el-button>
              <el-button @click="resetFilters" class="action-button-small">
                <el-icon><RefreshRight /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 表格部分保持不变 -->
    <el-card class="table-container">
      <el-table
        :data="pageData"
        style="width: 100%"
        border
        stripe
        highlight-current-row
        empty-text="没有找到匹配的记录"
        @sort-change="onSortChange"
      >
        <el-table-column prop="地区" label="地区" sortable></el-table-column>
        <el-table-column prop="价格" label="价格(￥)" sortable></el-table-column>
        <el-table-column prop="账号时间" label="账号时间(天)" sortable></el-table-column>
        <el-table-column prop="出售日期" label="出售日期" sortable></el-table-column>
        <el-table-column prop="备注" label="备注"></el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          background
          layout="sizes, prev, pager, next, total"
          :total="filteredData.length"
          :page-size="itemsPerPage"
          :page-sizes="[10, 20, 50, 100]"
          :current-page="currentPage"
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
        >
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import { Money, Search, RefreshRight } from '@element-plus/icons-vue'

export default {
  components: {
    Money,
    Search,
    RefreshRight,
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
      itemsPerPage: 20,
      currentSort: {
        column: '出售日期',
        ascending: false
      },
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
    onSortChange({ prop, order }) {
      if (prop) {
        this.currentSort.column = prop;
        this.currentSort.ascending = order === 'ascending';
        this.sortData();
      }
    },
    sortData() {
      const getCompareValue = (item, column) => {
        if (column === '出售日期') {
          return new Date(item[column]);
        } else if (column === '价格' || column === '账号时间') {
          return Number(item[column]);
        } else {
          return String(item[column]).toLowerCase();
        }
      };
      
      this.filteredData.sort((a, b) => {
        const aValue = getCompareValue(a, this.currentSort.column);
        const bValue = getCompareValue(b, this.currentSort.column);
        
        let compareResult;
        if (this.currentSort.column === '出售日期') {
          compareResult = aValue - bValue;
        } else if (this.currentSort.column === '价格' || this.currentSort.column === '账号时间') {
          compareResult = aValue - bValue;
        } else {
          compareResult = aValue.localeCompare(bValue);
        }
        return this.currentSort.ascending ? compareResult : -compareResult;
      });
      this.currentPage = 1;
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

        return matchesKeyword && matchesPrice && matchesTime && matchesDate;  // 添加账号时间条件
      });

      this.currentPage = 1;
      this.sortData();
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    handleSizeChange(val) {
      this.itemsPerPage = val;
      this.currentPage = 1;
    }
  },
  mounted() {
    this.fetchData();
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
  max-width: 1200px;
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
  gap: 10px;
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

.search-container {
  margin-bottom: 20px;
}

.search-panel {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.search-row {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.search-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.keyword-search {
  flex: 0.6;
  min-width: 100px;
  max-width: 130px;
}

.price-search {
  flex: 1.2;
  min-width: 160px;
  max-width: 175px;
}

.time-filter {
  display: flex;
  align-items: center;
}

.time-separator {
  margin: 0 10px;
  color: #909399;
}

.date-search {
  flex: 1.8;
  min-width: 260px;
}

.keyword-input {
  width: 100%;
  max-width: 150px;
}

.small-input-number {
  width: 90px !important;
}

.single-date-picker {
  width: 120px !important;
}

.price-filter, .date-range-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
}

.price-filter {
  display: flex;
  align-items: center;
}

.price-separator {
  margin: 0 10px;
  color: #909399;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: auto;
}

.table-container {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.el-table th {
  background-color: #f5f7fa !important;
  font-size: 16px !important;
  font-weight: bold !important;
}

.el-table td {
  font-size: 14px !important;
}

.el-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05) !important;
}

.date-range-container {
  display: flex;
  align-items: center;
  gap: 5px;
}

.single-date-picker {
  width: 150px !important;
}

.date-separator {
  color: #909399;
}

.date-picker {
  width: 320px !important;
}
</style>

.search-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  flex: 1;
  min-width: 220px;
}

.search-item .label {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
  display: block;
}

.price-search {
  flex: 1.2;
  min-width: 200px;
  max-width: 300px;
}

.time-search {
  flex: 1.2;
  min-width: 300px;
  max-width: 350px;
}

.date-search {
  flex: 1.8;
  min-width: 400px;
}

.el-input-number {
  width: 120px !important;
}

.search-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  flex: 1;
  min-width: 220px;
}

.search-item .label {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
  display: block;
}

.price-search {

