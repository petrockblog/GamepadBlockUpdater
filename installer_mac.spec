# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/florian/Programming/Github/GamepadBlockUpdater'],
             binaries=[],
             datas=[('/Users/florian/Programming/Github/GamepadBlockUpdater/tools/avrdude/mac/avrdude', 'tools/avrdude/mac/'),
             		('/Users/florian/Programming/Github/GamepadBlockUpdater/tools/avrdude/mac/avrdude.conf', 'tools/avrdude/mac/'),
             		('/Users/florian/Programming/Github/GamepadBlockUpdater/tools/avrdude/mac/libavrdude.1.dylib', 'tools/avrdude/mac/'),
             		('/Users/florian/Programming/Github/GamepadBlockUpdater/tools/avrdude/mac/libavrdude.a', 'tools/avrdude/mac/'),
             		('/Users/florian/Programming/Github/GamepadBlockUpdater/tools/avrdude/mac/libavrdude.la', 'tools/avrdude/mac/'),
             		('/Users/florian/Programming/Github/GamepadBlockUpdater/tools/avrdude/mac/libusb-1.0.a', 'tools/avrdude/mac/'),
             		('/Users/florian/Programming/Github/GamepadBlockUpdater/tools/avrdude/mac/libusb-1.0.la', 'tools/avrdude/mac/'),
             		('/Users/florian/Programming/Github/GamepadBlockUpdater/tools/avrdude/mac/libusb.a', 'tools/avrdude/mac/'),
             		('/Users/florian/Programming/Github/GamepadBlockUpdater/tools/avrdude/mac/libusb.la', 'tools/avrdude/mac/')
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
          console=False )
app = BUNDLE(exe,
             name='main.app',
             icon=None,
             bundle_identifier=None)
