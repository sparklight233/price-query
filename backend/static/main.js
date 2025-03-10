let currentPage = 1;
const itemsPerPage = 20;
let filteredData = [];
let allData = [];  // 存储所有数据
let currentSort = {
    column: '出售日期',
    ascending: false
};

// 初始化
window.onload = async function() {
    try {
        const response = await fetch('/api/data');
        allData = await response.json();
        filteredData = [...allData];  // 复制一份数据
        initializeDateInputs();
        sortData();
        displayResults();
        updatePagination();
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('searchStats').textContent = '数据加载失败';
    }
};

function initializeDateInputs() {
    const dates = filteredData.map(item => new Date(item.出售日期));
    const minDate = new Date(Math.min(...dates));
    const maxDate = new Date();
    
    document.getElementById('startDate').value = minDate.toISOString().split('T')[0];
    document.getElementById('endDate').value = maxDate.toISOString().split('T')[0];
}

function searchLocation() {
    const keyword = document.getElementById('searchInput').value.toLowerCase();
    const minPrice = Number(document.getElementById('minPrice').value) || 0;
    const maxPrice = Number(document.getElementById('maxPrice').value) || Infinity;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    // 从所有数据中筛选
    filteredData = allData.filter(item => {
        const matchesKeyword = item.地区.toLowerCase().includes(keyword);
        const price = Number(item.价格);
        const matchesPrice = price >= minPrice && price <= maxPrice;
        
        const itemDate = new Date(item.出售日期);
        const start = startDate ? new Date(startDate) : new Date(0);
        const end = endDate ? new Date(endDate) : new Date();
        
        start.setHours(0, 0, 0, 0);
        end.setHours(23, 59, 59, 999);
        
        const matchesDate = itemDate >= start && itemDate <= end;

        return matchesKeyword && matchesPrice && matchesDate;
    });

    document.getElementById('searchStats').textContent = 
        `找到 ${filteredData.length} 条相关记录`;

    currentPage = 1;
    sortData();
    displayResults();
    updatePagination();
}

function sortData() {
    filteredData.sort((a, b) => {
        let compareResult;
        if (currentSort.column === '出售日期') {
            compareResult = new Date(a[currentSort.column]) - new Date(b[currentSort.column]);
        } else if (currentSort.column === '价格' || currentSort.column === '账号时间') {
            compareResult = Number(a[currentSort.column]) - Number(b[currentSort.column]);
        } else {
            compareResult = String(a[currentSort.column]).localeCompare(String(b[currentSort.column]));
        }
        return currentSort.ascending ? compareResult : -compareResult;
    });
}

function displayResults() {
    const resultBody = document.getElementById('resultBody');
    resultBody.innerHTML = '';

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageData = filteredData.slice(start, end);

    if (pageData.length === 0) {
        resultBody.innerHTML = '<tr><td colspan="5" style="text-align: center;">没有找到匹配的记录</td></tr>';
        return;
    }

    pageData.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.地区}</td>
            <td>${item.价格}</td>
            <td>${item.账号时间}</td>
            <td>${item.出售日期}</td>
            <td>${item.备注 || ''}</td>
        `;
        resultBody.appendChild(row);
    });
}

function updatePagination() {
    const paginationDiv = document.getElementById('pagination');
    paginationDiv.innerHTML = '';

    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    
    if (totalPages <= 1) return;

    const prevButton = document.createElement('button');
    prevButton.textContent = '上一页';
    prevButton.onclick = () => {
        if (currentPage > 1) {
            currentPage--;
            displayResults();
            updatePagination();
        }
    };
    paginationDiv.appendChild(prevButton);

    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.textContent = i;
        pageButton.className = i === currentPage ? 'active' : '';
        pageButton.onclick = () => {
            currentPage = i;
            displayResults();
            updatePagination();
        };
        paginationDiv.appendChild(pageButton);
    }

    const nextButton = document.createElement('button');
    nextButton.textContent = '下一页';
    nextButton.onclick = () => {
        if (currentPage < totalPages) {
            currentPage++;
            displayResults();
            updatePagination();
        }
    };
    paginationDiv.appendChild(nextButton);
}

function sortTable(column) {
    if (currentSort.column === column) {
        currentSort.ascending = !currentSort.ascending;
    } else {
        currentSort.column = column;
        currentSort.ascending = true;
    }
    sortData();
    displayResults();
}

function resetFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('minPrice').value = '';
    document.getElementById('maxPrice').value = '';
    initializeDateInputs();
    
    filteredData = [...allData];  // 重置为所有数据
    currentPage = 1;
    sortData();
    displayResults();
    updatePagination();
}
