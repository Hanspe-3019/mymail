from collections import defaultdict
import heapq
from . emlx import EMLX
from . consts import MAIL, ARGS

ATMTGLOB = '**/Attachments/'

class Attachment():

    @staticmethod
    def sizes() -> defaultdict:

        sizes = defaultdict(int)
        for atmt in MAIL.glob(ATMTGLOB + '/*'):
            if not atmt.is_dir():
                continue
            rowid = int(atmt.name)
            sizes[rowid] += sum(
                child.stat().st_size
                for child in atmt.rglob('*') if child.is_file()
            )
        return sizes

    @staticmethod
    def get(rowid):
        return [f'{atmt.stat().st_size:16d}  {atmt.name}'
            for atmt in MAIL.rglob(ATMTGLOB + f'/{str(rowid)}/**/*')
                if atmt.is_file()
        ]

    @staticmethod
    def attachments(sizes):
        if ARGS.nlargest_attachments is None:
            return
        if len(sizes) == 0:
            return

        nlargest = ARGS.nlargest_attachments
        n = len(sizes) if nlargest <=  0 else nlargest
        print(f'🗂️ Top-{n} of emlx-Files with downladed attachments:') 
        for rowid, size in heapq.nlargest(
            n, sizes.items(), key=lambda item: item[1]
        ):
            EMLX(rowid).print()
            print('\n'.join(Attachment.get(rowid)))
