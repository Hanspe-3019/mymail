from pathlib import Path
import sqlite3
import logging

from . options import get_options

LOGGER = logging.getLogger(__name__)
ARGS = get_options()
MAIL = Path('~/Library/Mail').expanduser()
if not MAIL.is_dir():
    raise FileNotFoundError(f'{MAIL} not a directory')

try:
    _ = next(MAIL.iterdir())
except PermissionError:
    LOGGER.error(f'😞 cannot read {MAIL}. Needing Full Disk Access 🤔')
    raise

def get_maildata():
    ''' Im Verzeichnis MailData liegt der Mail-Index als sqlite-DB
    '''
    test = list(MAIL.glob('*/MailData'))
    if len(test) == 1:
        return test[0]
    raise AssertionError(f'MailData {test}')

def make_connection():
    ''' sqlite-Connection read-only
    '''
    maildb = get_maildata() / "envelope index"
    mailuri = f'file:{maildb}?mode=ro'
    return sqlite3.connect(mailuri, uri=True)

CON = make_connection()
