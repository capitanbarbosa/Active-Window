from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('active_window.pyw', base=base)
]

setup(name='Active Window',
      version = '0.99',
      description = 'Log of tasks connected via Notion API.',
      options = {'build_exe': build_options},
      executables = executables)
