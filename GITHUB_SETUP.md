# 🌐 如何连接到 GitHub

## 📝 前置准备

1. **注册 GitHub 账号**
   - 访问 https://github.com
   - 点击 "Sign up" 注册账号

2. **配置 Git 用户信息**（首次使用需要配置）
   ```bash
   git config --global user.name "你的名字"
   git config --global user.email "你的邮箱@example.com"
   ```

## 🚀 连接到 GitHub 的步骤

### 方法一：通过 GitHub 网站创建仓库（推荐）

#### 步骤 1：在 GitHub 上创建新仓库

1. 登录 GitHub
2. 点击右上角 "+" → "New repository"
3. 填写信息：
   - Repository name: `5481`
   - Description: `我的测试项目`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"（因为我们本地已经有了）
4. 点击 "Create repository"

#### 步骤 2：连接本地仓库到 GitHub

GitHub 会显示指令，复制并在终端执行：

```bash
# 进入项目目录
cd /Users/zhuricardo/Desktop/5481

# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/5481.git

# 推送代码到 GitHub
git branch -M main
git push -u origin main
```

### 方法二：通过 Cursor IDE 直接推送

1. 在 Cursor 中打开源代码管理（Source Control）侧边栏
   - 快捷键：`Cmd + Shift + G`（macOS）

2. 点击 "Publish to GitHub" 按钮

3. 选择仓库名称和可见性（Public/Private）

4. Cursor 会自动创建 GitHub 仓库并推送代码

## 🔑 GitHub 认证

### 使用 Personal Access Token（推荐）

1. 访问 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 直接链接：https://github.com/settings/tokens

2. 点击 "Generate new token (classic)"

3. 设置权限（至少需要）：
   - ✅ `repo` - 完整的仓库访问权限

4. 生成并**保存** Token（只显示一次！）

5. 推送时使用 Token 作为密码：
   ```bash
   Username: 你的GitHub用户名
   Password: ghp_xxxxxxxxxxxxxxxxxxxx（你的Token）
   ```

### 使用 SSH Key（更安全）

1. 生成 SSH 密钥：
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # 一路回车，使用默认设置
   ```

2. 复制公钥：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

3. 添加到 GitHub：
   - GitHub Settings → SSH and GPG keys → New SSH key
   - 粘贴公钥内容

4. 使用 SSH URL：
   ```bash
   git remote add origin git@github.com:YOUR_USERNAME/5481.git
   ```

## 📤 日常使用流程

```bash
# 1. 修改文件后，查看状态
git status

# 2. 添加修改的文件
git add .
# 或者添加特定文件
git add README.md

# 3. 提交到本地仓库
git commit -m "描述你做了什么修改"

# 4. 推送到 GitHub
git push

# 5. 从 GitHub 拉取最新代码
git pull
```

## 🎯 在 Cursor 中使用 Git

### 侧边栏操作

1. **Source Control 面板**（`Cmd + Shift + G`）
   - 查看修改的文件
   - 暂存/取消暂存文件（点击 + 或 -）
   - 输入提交信息并提交
   - 同步/推送/拉取

2. **文件修改标记**
   - 🟢 新文件
   - 🟡 修改的文件
   - 🔴 删除的文件

### 快捷键

- `Cmd + Shift + G` - 打开源代码管理
- `Cmd + Enter` - 提交（在提交消息框中）

## 🔍 查看 Git 历史

```bash
# 查看提交历史
git log

# 简洁显示
git log --oneline

# 图形化显示分支
git log --graph --oneline --all

# 查看某个文件的历史
git log README.md
```

## 🌿 分支操作

```bash
# 查看所有分支
git branch -a

# 创建新分支
git branch feature-new

# 切换分支
git checkout feature-new
# 或者使用新命令
git switch feature-new

# 创建并切换到新分支
git checkout -b feature-new

# 合并分支
git checkout main
git merge feature-new

# 删除分支
git branch -d feature-new
```

## 💡 常见问题

### 如果推送失败

```bash
# 先拉取远程更改
git pull origin main

# 解决冲突后再推送
git push origin main
```

### 撤销修改

```bash
# 撤销工作区的修改
git checkout -- filename

# 撤销已暂存的文件
git reset HEAD filename

# 撤销最后一次提交（保留修改）
git reset --soft HEAD^

# 撤销最后一次提交（丢弃修改）
git reset --hard HEAD^
```

## 📚 学习资源

- [GitHub 官方文档](https://docs.github.com)
- [Git 可视化学习](https://learngitbranching.js.org/)
- [Pro Git 书籍（免费）](https://git-scm.com/book/zh/v2)

---

**祝学习愉快！🎉**
