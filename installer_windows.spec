# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/florian/Programming/Github/GamepadBlockUpdater'],
             binaries=[],
             datas=[('tools/avrdude/mac/avrdude', 'tools/avrdude/mac/'),
             		('tools/avrdude/windows/avrdude.exe', 'tools/avrdude/windows/'),
             		('tools/avrdude/windows/avrdude.conf', 'tools/avrdude/windows/'),
             		('tools/avrdude/windows/cygwin1.dll', 'tools/avrdude/windows/'),
             		('tools/avrdude/windows/libusb0.dll', 'tools/avrdude/windows/')
             		],
             hiddenimports=['tkinter', 'requests'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='GamepadBlockUpdater',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
app = BUNDLE(exe,
             name='main.app',
             icon=None,
             bundle_identifier=None)
