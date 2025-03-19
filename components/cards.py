from nicegui import ui

def seat_card(seat):
    with ui.card().classes('size-[120px]').props('flat bordered') as card:
        with ui.column().classes('size-full items-center place-content-start'):
            with ui.row().classes('w-full h-1/2 items-center place-content-start'):
                ui.label(f'座位 {seat["seat_number"]}').classes('w-full h-fit text-sm font-bold')
            with ui.column().classes('w-full h-1/2 gap-0 items-center'):
                if seat['status'] == 0:
                    ui.label('未安装设备').classes('w-full text-xs text-red-500')
                elif seat['status'] == 1:
                    ui.label('已安装设备').classes('w-full text-xs text-green-500')
                    ui.label('MAC').classes('w-full text-xs text-gray-500')
                    ui.label(seat["mac"]).classes('w-full text-xs text-gray-500')