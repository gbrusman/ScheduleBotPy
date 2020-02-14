# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['AcademicTime.py', 'AppliedSeriesChoicePage.py', 'Course.py', 'CourseSelectPage.py', 'InterestSelectPage.py', 'MajorSelectPage.py', 'MultiPageApp.py', 'ScheduleBlock.py', 'ScheduleDisplayPage.py', 'Schedule.py', 'Student.py'],
             pathex=['C:\\Users\\gabri\\PycharmProjects\\ScheduleBotPy'],
             binaries=[],
             datas=[('database/*', 'database')],
             hiddenimports=[],
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
          name='ScheduleBotLINUX',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
