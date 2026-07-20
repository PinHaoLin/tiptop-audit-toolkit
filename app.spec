# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

project_root = Path.cwd()
app_icon = str(project_root / 'backend' / 'edimax_audit.ico')


a = Analysis(
    ['backend\\app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/dist', 'web'),
        ('aud', 'aud_seed'),
        ('程式修改週覆核記錄(暫存)', 'review_seed'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    exclude_binaries=False,
    name='TIPTOP_Audit_Toolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=app_icon,
)
