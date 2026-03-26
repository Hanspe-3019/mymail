import subprocess
from pathlib import Path

from . consts import MAIL  
def get_diskusage(mboxes) -> dict:
    ''' run du -k -d 0 -c ./**/*.mbox
    -> dict(mbox: size)
    '''

    glob = f'{MAIL}/**/*.mbox'

    du = run_du(glob)

    level = {mbox: mbox.count('/') for mbox in du}

    for mbox in sorted(level, key=lambda mbox: level[mbox], reverse=True):
        child_lvl = 1 + level[mbox]
        du[mbox] -= sum(
            size for child, size in du.items()
                if child.startswith(mbox) and level[child] == child_lvl
        )

    return du

def run_du(glob) -> dict:
    du = f'du -k -d 0 -c {glob}' 

    args = ['zsh', '-c', du]
    proc = subprocess.run(args, capture_output=True, check=True)

    result = []
    for line in proc.stdout.decode().split('\n'):
        try:
            size, path = line.split('\t')
        except ValueError:
            continue
        size = int(size)
        mbox = extract_mbox(path)
        result.append((mbox, size))

    return dict(result)

def extract_mbox(path) -> str:
    '''
    /Users/mb/Library/Mail/V10/
    6879A484-20CB-4C3B-8C49-2F3A1ECFE048/
    Archive.mbox/Tiefenriede.mbox/Tiefenriede H-Gas.mbox/
    /D5FEFD72-E421-4AFA-BF95-F74D5CDA4E45/
    Data/Messages/65.emlx
       ->
    6879A484/Archive/Tiefenriede/Tiefenriede H-Gas

    '''
    if path == 'total':
        return path
    path = Path(path)
    mbox_dirs = []
    account = None
    for i, part in enumerate(path.parts):
        if not part.endswith('.mbox'):
            continue
        if account is None:
            account = path.parts[i-1][:8]
        mbox_dirs.append(part[:-5])

    if len(mbox_dirs) == 0:
        raise AssertionError(f'No mbox_dirs: {path}')
    return f'{account}/{"/".join(mbox_dirs)}'
