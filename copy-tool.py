# -*- coding: utf-8 -*-
"""
copy-tool.py  离线剪贴板工具 for Windows
依赖: Python 3.8+ (Windows自带或官网下载)
作者: QClaw Agent
"""
import os, sys, json, tempfile, webbrowser, subprocess, ctypes

STORAGE_FILE = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'copytool_data.json')

DEFAULT_ITEMS = [
    {"title": "微信号", "text": "your-wechat-id", "badge": "常用"},
    {"title": "店铺介绍文案", "text": "欢迎来到我的小店！专注电脑维修、系统重装、网络调试，抖音直播6年，服务过上万用户，靠谱不踩坑！", "badge": "引流"},
    {"title": "远程协助链接", "text": "https://your-remote-support-link.com", "badge": "服务"},
]

HTML = r"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>剪贴板工具</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Microsoft YaHei",PingFang SC,sans-serif;background:#0f0f1a;color:#e0e0e0;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:40px 20px}
h1{font-size:22px;font-weight:600;color:#7dd3fc;margin-bottom:8px;letter-spacing:2px}
.subtitle{color:#64748b;font-size:13px;margin-bottom:36px}
.card{width:100%;max-width:680px;background:#1a1a2e;border:1px solid #2a2a4a;border-radius:14px;padding:20px 24px;margin-bottom:16px;transition:border-color .2s}
.card:hover{border-color:#3a3a6a}
.card-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.card-title{font-size:13px;color:#94a3b8;font-weight:500}
.badge{font-size:11px;background:#1e3a5f;color:#7dd3fc;padding:2px 10px;border-radius:20px;border:1px solid #0f4060}
.badge-orange{background:#3d2000;color:#fb923c;border-color:#5c3000}
.badge-green{background:#0f4060;color:#4ade80;border-color:#1a5a1a}
textarea{width:100%;height:90px;background:#111827;border:1px solid #2a2a4a;border-radius:10px;color:#e2e8f0;font-family:"Consolas","Cascadia Code",monospace;font-size:13px;line-height:1.6;padding:12px 14px;resize:vertical;outline:none;transition:border-color .2s}
textarea:focus{border-color:#4a9eff}
textarea.dbl-flash{border-color:#4ade80!important;background:#0a1f0a!important}
.btn-row{display:flex;gap:10px;margin-top:12px}
button{flex:1;padding:9px 0;border:none;border-radius:8px;font-size:13px;font-weight:500;cursor:pointer;transition:all .15s}
.btn-copy{background:#1d4ed8;color:#fff}
.btn-copy:hover{background:#2563eb;transform:translateY(-1px)}
.btn-del{background:#1f1f3a;color:#94a3b8;border:1px solid #2a2a4a}
.btn-del:hover{background:#2a2a4a;color:#e0e0e0}
#toast{position:fixed;bottom:40px;left:50%;transform:translateX(-50%) translateY(20px);background:#1d4ed8;color:#fff;padding:10px 24px;border-radius:8px;font-size:13px;font-weight:500;opacity:0;transition:all .25s ease;pointer-events:none;z-index:999;box-shadow:0 4px 20px rgba(29,78,216,.4)}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.hint{color:#475569;font-size:12px;text-align:center;margin-top:30px}
.add-section{width:100%;max-width:680px;margin-top:10px}
.add-card{background:#1a1a2e;border:1px dashed #2a2a4a;border-radius:14px;padding:20px 24px;display:flex;flex-direction:column;gap:10px}
.add-card input{background:#111827;border:1px solid #2a2a4a;border-radius:8px;color:#e2e8f0;font-size:13px;padding:9px 14px;outline:none}
.add-card input:focus{border-color:#4a9eff}
.add-card input::placeholder{color:#475569}
.btn-add{background:#0f4060;color:#7dd3fc;border:1px solid #1e4a7a;border-radius:8px;padding:9px;font-size:13px;cursor:pointer;transition:all .15s}
.btn-add:hover{background:#1e4a7a}
</style>
</head>
<body>
<h1>📋 剪贴板工具</h1>
<p class="subtitle">双击文本框 或 点复制按钮，即可复制</p>
<div id="cards"></div>
<div class="add-section">
  <div class="add-card">
    <input id="new-title" placeholder="标题（选填）" />
    <input id="new-text" placeholder="输入要复制的文本内容" />
    <button class="btn-add" onclick="addCard()">+ 添加文本项</button>
  </div>
</div>
<p class="hint">💡 关闭浏览器窗口即可退出程序</p>
<div id="toast"></div>
<script>
const STORAGE_KEY='__ct_local';
const defaults=__DEFAULT_JSON__;
function getItems(){try{const s=localStorage.getItem(STORAGE_KEY);if(s)return JSON.parse(s)}catch(e){}saveItems(defaults);return defaults}
function saveItems(items){localStorage.setItem(STORAGE_KEY,JSON.stringify(items))}
function showToast(msg){const t=document.getElementById('toast');t.textContent='✅ '+msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),1800)}
function copyText(text,title){if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).then(()=>showToast('"'+title+'" 已复制'))}else{const ta=document.createElement('textarea');ta.value=text;ta.style.cssText='position:fixed;opacity:0';document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);showToast('"'+title+'" 已复制')}}
function buildCard(item,i){const s=(t)=>t.replace(/'/g,"\\'");return`<div class="card"><div class="card-header"><span class="card-title">${item.title||('文本'+(i+1))}</span><span class="badge">${item.badge||''}</span></div><textarea id="ta-${i}" onclick="this.select()" ondblclick="copyText(this.value,'${s(item.title||'')}');this.classList.add('dbl-flash');setTimeout(()=>this.classList.remove('dbl-flash'),400)">${item.text}</textarea><div class="btn-row"><button class="btn-copy" onclick="copyText(document.getElementById('ta-${i}').value,'${s(item.title||'')}')">📋 复制</button><button class="btn-del" onclick="if(confirm('确定删除？'))deleteCard(${i})">🗑 删除</button></div></div>`}
function renderAll(){document.getElementById('cards').innerHTML=getItems().map((it,i)=>buildCard(it,i)).join('')}
function addCard(){const t=document.getElementById('new-title').value.trim(),n=document.getElementById('new-text').value.trim();if(!n){showToast('请输入内容');return}const items=getItems();items.push({title:t||('文本'+(items.length+1)),text:n,badge:''});saveItems(items);document.getElementById('new-title').value='';document.getElementById('new-text').value='';renderAll();showToast('已添加')}
function deleteCard(i){const items=getItems();items.splice(i,1);saveItems(items);renderAll()}
renderAll();
</script>
</body>
</html>
"""

def get_html():
    return HTML.replace('__DEFAULT_JSON__', json.dumps(DEFAULT_ITEMS, ensure_ascii=False))

def main():
    # 隐藏控制台窗口（Windows GUI 模式）
    if sys.platform == 'win32':
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except: pass

    html = get_html()
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.html', encoding='utf-8', delete=False, prefix='剪贴板工具_')
    tmp.write(html)
    tmp_path = tmp.name
    tmp.close()

    print(f"正在打开浏览器...")
    webbrowser.open('file:///' + tmp_path.replace('\\', '/'))
    print("剪贴板工具已打开！关闭浏览器窗口即可退出。")
    print("")
    try:
        input("按回车键退出...\n")
    except (EOFError, SyntaxError):
        pass

if __name__ == '__main__':
    main()
