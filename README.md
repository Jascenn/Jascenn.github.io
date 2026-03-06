# YuChen 个人博客

一个简洁优雅的个人博客网站，参考 lingyi.bio 设计风格。

## 特性

- 🎨 极简设计，专注内容
- 🌓 深色模式支持
- 📱 响应式布局
- ⚡ 纯静态，加载快速
- 🚀 可直接部署到 GitHub Pages

## 技术栈

- HTML5
- CSS3 (CSS Variables)
- Vanilla JavaScript
- 无需构建工具

## 本地预览

直接用浏览器打开 `index.html` 即可预览。

或者使用简单的 HTTP 服务器：

```bash
# Python 3
python -m http.server 8000

# Node.js (需要先安装 http-server)
npx http-server
```

然后访问 `http://localhost:8000`

## 部署到 GitHub Pages

### 方法一：通过 GitHub 网页操作

1. 在 GitHub 创建新仓库（例如：`yourusername.github.io`）
2. 将所有文件上传到仓库
3. 进入仓库 Settings → Pages
4. Source 选择 `main` 分支，目录选择 `/ (root)`
5. 点击 Save，等待几分钟即可访问

### 方法二：通过命令行

```bash
# 初始化 Git 仓库
git init
git add .
git commit -m "Initial commit"

# 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/yourusername/yourusername.github.io.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

然后在 GitHub 仓库设置中启用 Pages。

## 自定义内容

### 修改个人信息

编辑 `about.html`：
- 修改名字、简介
- 更新项目列表
- 添加联系方式

### 添加新文章

1. 在 `posts/` 目录创建新的 HTML 文件
2. 复制 `posts/first-post.html` 作为模板
3. 修改标题、日期、内容
4. 在 `index.html` 添加文章卡片

### 修改配色

编辑 `styles.css` 中的 CSS 变量：

```css
:root {
    --bg-primary: #ffffff;
    --text-primary: #1a1a1a;
    --accent-color: #2563eb;
    /* ... */
}
```

## 文件结构

```
lingyi-blog-b/
├── index.html          # 首页
├── about.html          # 关于页面
├── styles.css          # 样式文件
├── script.js           # JavaScript 功能
├── posts/              # 文章目录
│   └── first-post.html
└── README.md           # 说明文档
```

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge

## License

MIT

## 致谢

设计灵感来自 [lingyi.bio](https://lingyi.bio)
