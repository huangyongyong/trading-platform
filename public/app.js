// API 基础地址
const API_BASE = '';

/**
 * 搜索报价
 */
async function searchListings() {
    // 获取搜索条件
    const productModel = document.getElementById('productModel').value.trim();
    const minPrice = document.getElementById('minPrice').value;
    const maxPrice = document.getElementById('maxPrice').value;

    // 构建查询参数
    const params = new URLSearchParams();
    if (productModel) params.append('product_model', productModel);
    if (minPrice) params.append('min_price', minPrice);
    if (maxPrice) params.append('max_price', maxPrice);

    // 显示加载中
    showLoading(true);
    clearError();

    try {
        const response = await fetch(`${API_BASE}/listings?${params}`);
        
        if (!response.ok) {
            throw new Error(`请求失败: ${response.status}`);
        }

        const listings = await response.json();
        displayResults(listings);
    } catch (error) {
        showError(`搜索失败: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

/**
 * 显示搜索结果
 */
function displayResults(listings) {
    const container = document.getElementById('resultsContainer');
    const countElement = document.getElementById('resultsCount');
    
    // 更新数量
    countElement.textContent = `${listings.length} 条报价`;
    
    if (listings.length === 0) {
        container.innerHTML = `
            <div class="loading">
                没有找到符合条件的报价
            </div>
        `;
        return;
    }

    // 生成结果卡片
    container.innerHTML = listings.map(listing => `
        <div class="result-card">
            <div class="product-model">${escapeHtml(listing.product_model)}</div>
            <div class="price">¥${listing.price.toLocaleString()}</div>
            <div class="contact">${escapeHtml(listing.contact)}</div>
            <div class="time">发布于 ${formatTime(listing.created_at)}</div>
        </div>
    `).join('');
}

/**
 * 格式化时间
 */
function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * 防止 XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * 显示/隐藏加载状态
 */
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

/**
 * 显示错误信息
 */
function showError(message) {
    const container = document.getElementById('errorContainer');
    container.innerHTML = `
        <div class="error">
            ❌ ${escapeHtml(message)}
        </div>
    `;
    container.style.display = 'block';
}

/**
 * 清空错误信息
 */
function clearError() {
    const container = document.getElementById('errorContainer');
    container.innerHTML = '';
    container.style.display = 'none';
}

/**
 * 页面加载时自动搜索一次
 */
window.onload = function() {
    // 可以在这里添加初始搜索
    // searchListings();
    
    // 支持回车搜索
    document.getElementById('productModel').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchListings();
    });
    document.getElementById('minPrice').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchListings();
    });
    document.getElementById('maxPrice').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchListings();
    });
};