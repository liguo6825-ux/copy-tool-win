@echo off
echo ============================================
echo   剪贴板工具 - Windows 一键打包脚本
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/2] 正在安装打包工具...
pip install pyinstaller -q

echo [2/2] 正在打包，请稍候...
pyinstaller --onefile --noconsole --name "剪贴板工具" --distpath . copy-tool.py

echo.
echo ============================================
echo   打包完成！生成的 exe 文件在当前目录
echo ============================================
pause
