// 主题切换功能
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// 页面加载时恢复主题设置
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    // 初始化搜索功能
    initSearch();

    // 初始化标签筛选
    initTagFilter();
});

// ===== 搜索功能 =====
function initSearch() {
    const searchInput = document.getElementById('search-input');
    const searchClear = document.getElementById('search-clear');
    const searchInfo = document.getElementById('search-results-info');
    
    if (!searchInput) return;

    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim().toLowerCase();
        
        // 显示/隐藏清除按钮
        if (searchClear) {
            searchClear.classList.toggle('visible', query.length > 0);
        }

        filterPosts(query);
    });

    if (searchClear) {
        searchClear.addEventListener('click', () => {
            searchInput.value = '';
            searchClear.classList.remove('visible');
            filterPosts('');
            searchInput.focus();
        });
    }
}

function filterPosts(query) {
    const posts = document.querySelectorAll('.post-card');
    const noResults = document.getElementById('no-results');
    const searchInfo = document.getElementById('search-results-info');
    let visibleCount = 0;

    // 获取当前激活的标签
    const activeTag = document.querySelector('.filter-tag.active');
    const activeTagText = activeTag ? activeTag.dataset.tag : null;

    posts.forEach(post => {
        const title = (post.dataset.title || '').toLowerCase();
        const excerpt = (post.dataset.excerpt || '').toLowerCase();
        const tags = (post.dataset.tags || '').toLowerCase();

        const matchesSearch = !query || 
            title.includes(query) || 
            excerpt.includes(query) || 
            tags.includes(query);

        const matchesTag = !activeTagText || tags.includes(activeTagText.toLowerCase());

        if (matchesSearch && matchesTag) {
            post.classList.remove('hidden');
            visibleCount++;
        } else {
            post.classList.add('hidden');
        }
    });

    // 更新无结果提示
    if (noResults) {
        noResults.classList.toggle('visible', visibleCount === 0);
    }

    // 更新搜索结果信息
    if (searchInfo) {
        if (query) {
            searchInfo.textContent = `找到 ${visibleCount} 篇相关文章`;
            searchInfo.classList.add('visible');
        } else {
            searchInfo.classList.remove('visible');
        }
    }
}

// ===== 标签筛选 =====
function initTagFilter() {
    const filterTags = document.querySelectorAll('.filter-tag');
    
    filterTags.forEach(tag => {
        tag.addEventListener('click', () => {
            // 切换激活状态
            if (tag.classList.contains('active')) {
                tag.classList.remove('active');
            } else {
                filterTags.forEach(t => t.classList.remove('active'));
                tag.classList.add('active');
            }

            // 重新筛选
            const searchInput = document.getElementById('search-input');
            const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
            filterPosts(query);
        });
    });
}
