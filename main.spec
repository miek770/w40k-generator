# -*- mode: python ; coding: utf-8 -*-

version = "0.1.0"

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\michel\\gits\\w40k-generator\\src'],
             binaries=[],
             datas=[
                 ("C:\\Users\\michel\\gits\\w40k-generator\\src\\codices\\necron.cfg", "codices"),
                 ("C:\\Users\\michel\\gits\\w40k-generator\\src\\configs\\sample_necron.cfg", "configs"),
             ],
             hiddenimports=[
                 "pkg_resources.py2_warn",
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=f"w40k-generator-{version}",
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
