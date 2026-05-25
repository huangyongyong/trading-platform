// public/app.js
async function searchListings() {
    const productModel = document.getElementById('productModel').value;
    const minPrice = document.getElementById('minPrice').value;
    const maxPrice = document.getElementById('maxPrice').value;
    
    // 构建查询参数
    const params = new URLSearchParams();
    if (productModel) params.append('product_model', productModel);
    if (minPrice) params.append('min_price', minPrice);
    if (maxPrice) params.append('max_price', maxPrice);
    
    // 显示加载中
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultsContainer').innerHTML = '';
    document.getElementById('errorContainer').style.display = 'none';
    
    try {
        const response = await fetch(`/listings?${params.toString()}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        // 更新结果数量
        document.getElementById('resultsCount').textContent = `${data.length} 条报价`;
        
        // 清空并显示结果
        const container = document.getElementById('resultsContainer');
        container.innerHTML = '';
        
        if (data.length === 0) {
            container.innerHTML = '<div class="loading">没有找到符合条件的报价</div>';
        } else {
            data.forEach(item => {
                const card = document.createElement('div');
                card.className = 'result-card';
                card.innerHTML = `
                    <div class="product-model">${item.product_model}</div>
                    <div class="price">¥${item.price.toLocaleString()}</div>
                    <div class="contact">${item.contact}</div>
                    <div class="time">${new Date(item.created_at).toLocaleString('zh-CN')}</div>
                `;
                container.appendChild(card);
            });
        }
    } catch (error) {
        const errorDiv = document.getElementById('errorContainer');
        errorDiv.style.display = 'block';
        errorDiv.innerHTML = `搜索失败: ${error.message}`;
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

// 页面加载完成后，可以添加一些初始数据（可选）
document.addEventListener('DOMContentLoaded', function() {
    console.log('交易平台前端已加载');
    
    // 可选：自动搜索一次显示所有数据
    // searchListings();
});