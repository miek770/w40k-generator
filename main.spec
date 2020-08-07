# -*- mode: python ; coding: utf-8 -*-

from main import __version__

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\michel\\gits\\w40k-generator\\src'],
             binaries=[],
             datas=[],
             hiddenimports=[
                 "pkg_resources.py2_warn",
                 "PyQt5.sip",
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=f"w40k-generator-{__version__}",
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
