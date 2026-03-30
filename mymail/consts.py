from pathlib import Path
import sqlite3
from . options import get_options

ARGS = get_options()
MAIL = Path('~/Library/Mail').expanduser()

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
