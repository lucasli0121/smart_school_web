# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import matplotlib

a = Analysis(
    ['main.py',
    'navigation.py',
    './components/cards.py',
    './components/dialogs.py',
    './components/inputs.py',
    './components/labels.py',
    './components/progress.py',
    './components/tables.py',
    './menu/top_menu.py',
    './pages/course_page.py',
    './pages/device_page.py',
    './pages/login_page.py',
    './pages/main_page.py',
    './resources/strings.py',
    ],
    pathex=['~/hjy_school_proj/code/smart_school_web'],
    binaries=[],
    datas=[
        (matplotlib.get_data_path(), 'matplotlib/mpl-data'),
        ('./nicegui/static/*','./nicegui/static'),
    ],
    hiddenimports=['matplotlib', 'matplotlib.pyplot', 'nicegui', 'tables._comp_lzo', 'tables._comp_bzip2', '"pysqlite2', 'psycopg2'],
    zipfiles=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='smart_school_web',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='smart_school_web',
)
