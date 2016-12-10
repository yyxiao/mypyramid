#!"D:\Program Files\python35\python3.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'mypyramid','console_scripts','initialize_mypyramid_db'
__requires__ = 'mypyramid'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('mypyramid', 'console_scripts', 'initialize_mypyramid_db')()
    )
