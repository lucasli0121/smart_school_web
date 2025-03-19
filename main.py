'''
Author: liguoqiang
Date: 2025-03-03 13:40:09
LastEditors: liguoqiang
LastEditTime: 2025-03-18 18:42:04
Description: 
'''
'''
Author: liguoqiang
Date: 2025-03-03 13:40:09
LastEditors: liguoqiang
LastEditTime: 2025-03-13 11:33:33
Description: 
'''
'''
Author: liguoqiang
Date: 2025-03-03 13:40:09
LastEditors: liguoqiang
LastEditTime: 2025-03-13 11:29:49
Description: 
'''

import matplotlib
matplotlib.use('Agg')  # 使用非图形后端
import matplotlib.pyplot as plt

# 预先构建字体缓存
plt.plot([0,1], [0,1])
plt.savefig('font_cache_test.png')  # 保存到有效的文件路径

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import ui,app
from resources import strings
from pages import login_page, main_page


unrestricted_page_routes = {'/login'}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path
                return RedirectResponse('/login')
        return await call_next(request)


app.add_middleware(AuthMiddleware)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title=strings.APP_NAME, port=8083, storage_secret='a719a08c-30c5-4d19-8116-05af7d6b3cec')