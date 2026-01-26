# 🎨 Cursor 中使用 GitHub 完全指南

## ✅ 是的！您可以完全在 Cursor 中使用 GitHub！

Cursor 内置了完整的 Git 和 GitHub 集成功能，无需切换到终端。

---

## 🚀 快速开始：3 种方式推送到 GitHub

### 方法 1：一键发布到 GitHub（最简单）✨

1. **打开源代码管理**
   ```
   快捷键：Cmd + Shift + G（macOS）
   或点击左侧栏的源代码管理图标
   ```

2. **点击 "Publish to GitHub" 按钮**
   - Cursor 会自动登录 GitHub
   - 选择仓库名称
   - 选择公开（Public）或私有（Private）
   - 点击确认

3. **完成！**
   - Cursor 自动创建 GitHub 仓库
   - 自动推送所有代码
   - 自动设置远程连接

### 方法 2：连接已有的 GitHub 仓库

如果您已经在 GitHub 上创建了仓库：

1. **复制仓库 URL**
   ```
   https://github.com/YOUR_USERNAME/5481.git
   ```

2. **在 Cursor 终端中**（`` Ctrl + ` ``）：
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/5481.git
   git branch -M main
   git push -u origin main
   ```

3. **之后就可以用 Cursor 界面操作了**

### 方法 3：使用 Cursor 的命令面板

1. **打开命令面板**
   ```
   Cmd + Shift + P（macOS）
   ```

2. **输入并选择**：
   ```
   Git: Add Remote
   ```

3. **按提示输入**：
   - Remote name: `origin`
   - Remote URL: `https://github.com/YOUR_USERNAME/5481.git`

---

## 📱 Cursor 源代码管理界面详解

### 打开方式：
- **快捷键**：`Cmd + Shift + G`（macOS）
- **或点击**：左侧边栏的分支图标 🌿

### 界面布局：

```
┌──────────────────────────────────────┐
│  SOURCE CONTROL                      │
├──────────────────────────────────────┤
│                                      │
│  Message (Cmd+Enter to commit)       │  ← 输入提交信息
│  ┌────────────────────────────────┐  │
│  │ 添加新功能                      │  │
│  └────────────────────────────────┘  │
│                                      │
│  ✓ Commit  ↻ Sync  ... More         │  ← 操作按钮
│                                      │
├──────────────────────────────────────┤
│  CHANGES (3)                         │  ← 未暂存的更改
│  ├─ M  test.py                      │
│  ├─ +  new_file.py                  │
│  └─ D  old_file.py                  │
│                                      │
│  STAGED CHANGES (1)                  │  ← 已暂存的更改
│  └─ M  README.md                    │
│                                      │
└──────────────────────────────────────┘
```

---

## 🎯 日常工作流程（在 Cursor 中）

### 步骤 1：修改代码
- 在 Cursor 中编辑文件
- 文件名旁会显示修改标记（M、+、D）

### 步骤 2：查看更改
1. 打开源代码管理（`Cmd + Shift + G`）
2. 点击文件名查看具体修改：
   - 🟢 绿色：新增的行
   - 🔴 红色：删除的行
   - 并排对比显示

### 步骤 3：暂存更改
- **暂存所有文件**：点击 "Changes" 旁的 `+` 按钮
- **暂存单个文件**：点击文件名旁的 `+` 按钮
- **取消暂存**：点击 `-` 按钮

### 步骤 4：提交更改
1. 在顶部消息框输入提交信息
2. 点击 `✓ Commit` 按钮
3. 或使用快捷键：`Cmd + Enter`

### 步骤 5：推送到 GitHub
- **点击 "Sync" 按钮**
- 或点击 "..." → "Push"
- Cursor 会自动推送到 GitHub

---

## 🌿 分支管理（在 Cursor 中）

### 查看当前分支
- 看左下角状态栏，显示当前分支名（如 `main`）

### 创建新分支
1. **方法 1**：点击左下角的分支名
2. 选择 "Create new branch"
3. 输入分支名（如 `feature-new`）

或

1. **方法 2**：命令面板（`Cmd + Shift + P`）
2. 输入 "Git: Create Branch"

### 切换分支
1. 点击左下角的分支名
2. 选择要切换的分支

### 合并分支
1. 切换到目标分支（如 `main`）
2. 命令面板 → "Git: Merge Branch"
3. 选择要合并的分支

---

## 🔄 同步代码（Pull & Push）

### Sync 按钮的作用：
```
点击 Sync = git pull + git push
```

### 手动操作：
- **Pull（拉取）**："..." → "Pull"
- **Push（推送）**："..." → "Push"
- **Fetch（获取）**："..." → "Fetch"

---

## 📝 实际操作示例

### 示例：修改 README.md 并推送到 GitHub

1. **修改文件**
   ```markdown
   # 我的项目
   
   添加了新的内容！
   ```

2. **打开源代码管理**
   - 按 `Cmd + Shift + G`
   - 看到 `README.md` 在 "Changes" 中

3. **查看差异**
   - 点击 `README.md`
   - 看到绿色的新增行

4. **暂存文件**
   - 点击 `README.md` 旁的 `+` 号
   - 文件移到 "Staged Changes"

5. **提交**
   - 输入：`更新 README 文档`
   - 点击 `✓ Commit` 或按 `Cmd + Enter`

6. **推送到 GitHub**
   - 点击 `↻ Sync` 按钮
   - 完成！GitHub 上已更新

---

## 🎨 Cursor 的 GitHub 高级功能

### 1. **查看提交历史**
- 在文件上右键 → "View File History"
- 或使用扩展：GitLens

### 2. **对比版本**
- 右键文件 → "Compare with..."
- 选择要对比的版本

### 3. **撤销更改**
- 右键文件 → "Discard Changes"（丢弃未提交的更改）

### 4. **Stash（暂存工作）**
- "..." → "Stash" → "Stash Changes"
- 临时保存未提交的更改

### 5. **Pull Request**
- 安装 GitHub Pull Requests 扩展
- 在 Cursor 中直接创建和审查 PR

---

## 🔑 GitHub 认证设置

### 首次使用时：

1. **Cursor 会提示登录 GitHub**
   - 点击 "Sign in with GitHub"
   - 浏览器打开授权页面
   - 点击 "Authorize"

2. **或使用 Personal Access Token**
   - GitHub → Settings → Developer settings → Tokens
   - 生成 Token（勾选 `repo` 权限）
   - Cursor 中输入 Token

3. **或使用 SSH**
   - 配置 SSH 密钥（参考 GITHUB_SETUP.md）
   - Cursor 自动使用

---

## 💡 常用快捷键

| 操作 | 快捷键 (macOS) |
|------|----------------|
| 打开源代码管理 | `Cmd + Shift + G` |
| 提交 | `Cmd + Enter` |
| 打开命令面板 | `Cmd + Shift + P` |
| 打开终端 | `` Ctrl + ` `` |
| 查看文件历史 | 右键 → View History |

---

## ⚙️ 推荐的 Cursor 扩展

### 1. **GitLens**（强烈推荐）
- 显示每行代码的提交信息
- 可视化分支历史
- 强大的 Git 功能

安装：
```
Cmd + Shift + X → 搜索 "GitLens" → Install
```

### 2. **GitHub Pull Requests**
- 在 Cursor 中管理 PR
- 代码审查

### 3. **Git Graph**
- 图形化显示 Git 历史
- 分支可视化

---

## 🎯 最佳实践

### ✅ DO：

1. **频繁提交**
   - 小改动，频繁提交
   - 提交信息清晰

2. **使用分支**
   - 新功能用新分支
   - 保持 `main` 分支稳定

3. **定期同步**
   - 经常 Pull 最新代码
   - 避免冲突

4. **利用 Cursor 的可视化**
   - 查看差异
   - 代码审查

### ❌ DON'T：

1. **不要直接在 main 分支开发**
2. **不要提交敏感信息**（密码、Token）
3. **不要忽略冲突**

---

## 🔍 排查问题

### 问题 1：推送失败

**症状**：点击 Sync 报错

**解决**：
```bash
# 在 Cursor 终端中
git pull origin main
# 解决冲突后
git push origin main
```

### 问题 2：未连接远程仓库

**症状**：没有 Sync 按钮

**解决**：
1. 命令面板 → "Git: Add Remote"
2. 或使用 "Publish to GitHub"

### 问题 3：认证失败

**症状**：推送时要求密码

**解决**：
- 重新登录 GitHub
- 或使用 Personal Access Token

---

## 📊 总结对比

| 操作 | 终端命令 | Cursor 界面操作 |
|------|---------|----------------|
| 查看状态 | `git status` | 源代码管理面板自动显示 |
| 暂存文件 | `git add file` | 点击 `+` 按钮 |
| 提交 | `git commit -m "msg"` | 输入消息 + 点击 Commit |
| 推送 | `git push` | 点击 Sync 按钮 |
| 拉取 | `git pull` | 点击 Sync 按钮 |
| 切换分支 | `git checkout branch` | 点击左下角分支名 |
| 查看差异 | `git diff` | 点击文件名查看 |

---

## 🎉 立即尝试！

现在试试在 Cursor 中：

1. **按 `Cmd + Shift + G`** 打开源代码管理
2. **查看刚才创建的新文件**
3. **暂存所有文件**（点击 Changes 旁的 `+`）
4. **输入提交信息**：`添加 CI/CD 文档`
5. **提交**（点击 ✓ 或按 `Cmd + Enter`）
6. **准备推送到 GitHub**

---

**您完全可以在 Cursor 中完成所有 Git 和 GitHub 操作！** 🚀

再也不需要切换到终端了（除非您喜欢命令行）😊
