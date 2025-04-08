'''
Author: liguoqiang
Date: 2025-03-03 13:40:09
LastEditors: liguoqiang
LastEditTime: 2025-03-19 14:57:09
Description: 
'''
import os
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import ui,app
from resources import strings
from pages import login_page, main_page

import matplotlib
matplotlib.use('Agg')  # 使用非图形后端
import matplotlib.pyplot as plt

# 添加以下代码以注册静态文件目录
# 获取当前文件所在目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 注册静态文件目录
# app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "../static")), name="static")
app.add_static_files('/static', os.path.join(current_dir, "static"))

# 添加自定义字体
ui.add_head_html('''
    <style>
        @font-face {
            font-family: 'Source Han Sans CN';
            src: url('/static/fonts/SourceHanSansCN-Regular.otf') format('opentype');
            font-weight: normal;
            font-style: normal;
        }
        @font-face {
            font-family: 'Source Han Sans CN';
            src: url('/static/fonts/SourceHanSansCN-Bold.otf') format('opentype');
            font-weight: bold;
            font-style: normal;
        }
        @font-face {
            font-family: 'Source Han Sans CN';
            src: url('/static/fonts/SourceHanSansCN-Light.otf') format('opentype');
            font-weight: 300;
            font-style: normal;
        }
        /* 设置全局默认字体 */
        html, body {
            font-family: 'Source Han Sans CN';
        }        
    </style>
''')

# 定义全局颜色
# ui.colors(primary='#65B6FF', onprimary='#FFFFFF', secondary='#65B6FF', accent='#111B1E', positive='#53B689')

# 预先构建字体缓存
plt.plot([0,1], [0,1])
plt.savefig('font_cache_test.png')  # 保存到有效的文件路径

unrestricted_page_routes = {'/login', '/static'}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') \
                and not request.url.path.startswith('/static') \
                and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path
                return RedirectResponse('/login')
        return await call_next(request)


app.add_middleware(AuthMiddleware)



if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title=strings.APP_NAME, port=8083, favicon='/static/images/web_logo.png', storage_secret='a719a08c-30c5-4d19-8116-05af7d6b3cec')