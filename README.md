# 剪贴板工具 Windows 版

## 方法一：一键打包（推荐）

双击运行 `build.bat`，自动安装依赖并生成 `剪贴板工具.exe`

## 方法二：手动命令行

```cmd
pip install pyinstaller
pyinstaller --onefile --noconsole --name 剪贴板工具 copy-tool.py
```

## 方法三：直接运行源码

```cmd
python copy-tool.py
```

## 打包后的 exe 使用说明

1. 双击运行 `剪贴板工具.exe`
2. 自动打开浏览器显示工具界面
3. 关闭浏览器窗口即可退出程序
4. 数据保存在 `%APPDATA%\copytool_data.json`

## 界面功能

- 点击复制按钮 → 直接复制文本
- 双击文本框 → 同样可以复制
- + 添加文本项 → 追加新内容
- 删除 → 移除该条目
- 数据自动保存在本地，永久有效
