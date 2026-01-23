#!/usr/bin/env python3
"""
测试文件 - Python 版本
用于测试 Git 版本控制
"""

def hello_world():
    """打印问候信息"""
    print("你好，这是我的第一个 Git 项目！")
    print("🚀 让我们开始学习版本控制吧！")

def show_git_commands():
    """显示常用 Git 命令"""
    commands = {
        "初始化": "git init",
        "查看状态": "git status",
        "添加文件": "git add .",
        "提交": "git commit -m '提交信息'",
        "查看历史": "git log",
        "推送到远程": "git push origin main",
    }
    
    print("\n📚 常用 Git 命令：")
    print("=" * 40)
    for name, cmd in commands.items():
        print(f"{name:10} → {cmd}")
    print("=" * 40)

if __name__ == "__main__":
    hello_world()
    show_git_commands()
