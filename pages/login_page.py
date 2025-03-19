from typing import Optional
from nicegui import ui,app
from fastapi.responses import RedirectResponse
from components import inputs

passwords = {'admin': 'admin', 'user': 'user'}

@ui.page('/login')
def login() -> Optional[RedirectResponse]:
    def try_login() -> None:
        if passwords.get(username.value) == password.value:
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.navigate.to(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go
        else:
            ui.notify('账号或密码错误', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('w-1/3 h-1/3 absolute-center place-content-center') as card:
        with ui.column().classes('size-full item-center place-content-center'):
            username = inputs.input_user_w60('请输入登录账号', try_login)
            password = inputs.input_password_w60('请输入密码', try_login)
            ui.button('登录', on_click=try_login).classes('w-60 self-center')
    return None