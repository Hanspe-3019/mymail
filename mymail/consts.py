from pathlib import Path
import sqlite3
import argparse
from importlib.resources import read_text


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

def get_options():
    ''' add_arguments('-x', nargs='?', const='*') bedeutet
         ein optionales Argument: Wenn es fehlt definiert const den Wert.
         Also, wenn die action -x nicht vorhanden ist, gibt es Null
         wenn Action -x vorhanden ohne Argument, gibt es '*'.
    '''
    parser = argparse.ArgumentParser(
        prog='mymail',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=read_text(__package__, 'description.txt'),
        epilog=read_text(__package__, 'epilog.txt'),
        # {help_helper(shiftby=8)}
    )

    parser.add_argument(
        "-a",    
        "--account",
        type=str,
        dest="filter_account",
        default=False,
        help= "filter by account.",
        metavar="`account`",
    )
    parser.add_argument(
        "-m",
        "--mbox",
        type=str,
        dest="filter_mbox",
        default=False,
        help= "filter by mbox.",
        metavar="`mbox`",
    )
    parser.add_argument(
        "--mi",    
        dest="dump_no_index",
        action='store_true',
        help="show emlx missing entry in index"
        " optionally filtered by mbox and account.",
    )
    parser.add_argument(
        "--me",
        dest="dump_no_emlx",
        action='store_true',
        help="show messages missing emlx-file"
        " optionally filtered by mbox and account",
    )
    parser.add_argument(
        "--le",
        type=int,
        dest="nlargest_emlx",
        help="show top largest emlx",
        nargs='?', const=10,
        metavar="`n`",
    )
    parser.add_argument(
        "--la",
        type=int,
        dest="nlargest_attachments",
        help="show top largest attachments",
        nargs='?', const=10,
        metavar="`n`",
    )
    parser.add_argument(
        "-p",
        "--print",
        type=int,
        dest="rowids",
        nargs='+',
        help="print individual ids",
        metavar="id",
    )
    parser.add_argument(
        "-v",
        action='store_true',
        dest="verbose",
        help="show more detail",
    )

    return parser.parse_args()

ARGS = get_options()
CON = make_connection()
