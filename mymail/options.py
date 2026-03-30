import argparse
from importlib.resources import read_text

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
    )

    parser.add_argument(
        "-i",
        "--index-missing",    
        action='store_true', dest="dump_no_index",
        help="show emlx missing entry in index"
        " optionally filtered.",
    )
    parser.add_argument(
        "-e",
        "--emlx-missing",
        action='store_true', dest="dump_no_emlx",
        help="show messages missing emlx-file"
        " optionally filtered",
    )
    parser.add_argument(
        "-L",
        type=int, dest="nlargest_emlx",
        nargs='?', const=10,
        help="show top largest emlx",
        metavar="`n`",
    )
    parser.add_argument(
        "-A",
        type=int, dest="nlargest_attachments",
        nargs='?', const=10,
        help="show top largest attachments",
        metavar="`n`",
    )
    parser.add_argument(
        "-p",
        "--print",
        type=int, dest="rowids",
        nargs='+',
        help="print individual ids",
        metavar="id",
    )
    parser.add_argument(
        "--account",
        type=str, dest="filter_account",
        default=False,
        help= "filter overview and searches by account.",
        metavar="`account`",
    )
    parser.add_argument(
        "--mbox",
        type=str, dest="filter_mbox",
        default=False,
        help= "filter searches by mbox.",
        metavar="`mbox`",
    )
    parser.add_argument(
        "-v",
        action='store_true', dest="verbose",
        help="show more details",
    )

    return parser.parse_args()

