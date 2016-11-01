#!"D:\Program Files\python35\python3.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'hyjj','console_scripts','initialize_hyjj_db'
__requires__ = 'hyjj'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('hyjj', 'console_scripts', 'initialize_hyjj_db')()
    )
