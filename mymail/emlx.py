from collections import defaultdict
import heapq
from email.parser import BytesParser
from email.policy import default

try:
    from dateutil.parser import parse
    dateutil = True
except ModuleNotFoundError:
    dateutil = False

from . consts import MAIL, ARGS
from . du import get_diskusage
from . du import extract_mbox

MAILGLOB = '**/*.emlx'
ROWID_TO_PATH = {int(path.name.split('.')[0]) : path for path in MAIL.glob(MAILGLOB)}


class EMLX:

    def __init__(self, rowid):
        ''' Parse der emlx-Datei
        '''

        self.rowid = rowid
        emlx = ROWID_TO_PATH[rowid]

        # emlx enthält in der ersten Zeile die Größe,
        # dies ist eine Erweiterung zum eml-Standard
        # Der BytesParser kann nur eml und nicht emlx.

        with emlx.open('rb') as fp:
            emlx_size = int(fp.readline())
            headers = BytesParser(policy=default).parse(fp, headersonly=True)

        date = ( # dates laut RFC 2822:
                 #     'Tue, 08 Apr 2025 06:10:35 +0000'
            parse(headers['Date'])
                .astimezone()
                .isoformat(sep=' ', timespec='minutes')
        ) if dateutil else headers['Date']
        
        to = headers['To']
        subject = headers.get('Subject','no subject')[:40]

        self.path = emlx
        self.size = emlx_size
        self.mbox = extract_mbox(emlx)
        self.account = self.mbox[:8]
        self.mbox_path = self.mbox[9:]
        self.name = emlx.name
        self.date = date
        self.to = to
        self.subject = subject

    def print(self):
        if ARGS.verbose:
            print(f'''{self.name}
            Mbox:    {self.mbox}
            Size:    {self.size}
            Date:    {self.date}
            To:      {self.to}
            Subject: {self.subject}
            '''.replace(f'''\n{' '*8}''','\n')
            )
        else:
            print(
                f'{self.mbox:40s}{self.name:20s}'
                f':{self.size:8d}'
            )

    @staticmethod
    def print_nlargest(sizes):
        print(f'\nTop{ARGS.nlargest_emlx} of largest emlx files')
        for rowid, size in heapq.nlargest(
            ARGS.nlargest_emlx,
            sizes.items(),
            key=lambda item: item[1]
        ):
            EMLX(rowid).print()

    @staticmethod
    def mboxes() -> (dict, dict):
        '''
        '''
        counts = defaultdict(int)   # mbox -> count of emlx-files
        sizes  = defaultdict(int)   # rowid -> size of emlx-file

        for emlx in ROWID_TO_PATH.values():

            mbox = extract_mbox(emlx)
            counts[mbox] += 1

            rowid = int(emlx.name.split('.')[0])
            sizes[rowid] += emlx.stat().st_size

        du = get_diskusage(counts.keys())
        return (counts, sizes, du)

    @staticmethod
    def no_index_summary(rowids) -> dict:
        ''' -> dict( mbox : count)
        '''
        mbox_cnt = defaultdict(int)  # Anzahl

        for rowid in rowids:
            emlx = EMLX(rowid)
            mbox_key = emlx.mbox
            mbox_cnt[mbox_key] += 1

        return { mbox: count for mbox, count in mbox_cnt.items() }

    @staticmethod
    def get_rowid2path():
        return ROWID_TO_PATH
