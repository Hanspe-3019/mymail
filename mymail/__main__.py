from . emlx import EMLX
from . msg  import MSG
from . attachments import Attachment
from . consts import ARGS
from . accounts import get_account_info

account_filter = ARGS.filter_account if ARGS.filter_account else ''
mbox_filter = ARGS.filter_mbox if ARGS.filter_mbox else '' 

rowids_in_index = MSG.rowids()

mboxes_emlx, emlx_sizes, mboxes_du = EMLX.mboxes()
rowids_in_emlx = set( emlx_sizes.keys())

w_o_emlx = len(rowids_in_index - rowids_in_emlx)
w_o_indx = len(rowids_in_emlx - rowids_in_index)

# ====================================
def overview():

    mboxes_index = MSG.mboxes()
    mboxes_no_ix = EMLX.no_index_summary(rowids_in_emlx - rowids_in_index)

    v = ' '
    monster_1 = '👹' if w_o_indx > 0 else ' '
    monster_2 = '👺' if w_o_emlx > 0 else ' '
    monster = f'{monster_1} {monster_2}'
    print(f' Overview Mailboxes{v*32}'
          f'Index{v*3}Files  KB %   {monster}')
    sum_count_emlx = 0
    sum_count_index = 0

    total = mboxes_du['total']

    prev_account = ''
    account_info = get_account_info()

    for mbox in sorted( set(mboxes_emlx.keys() ) | mboxes_index.keys()) :

        account, mbox_path = mbox.split('/', maxsplit=1)
        count_emlx  = mboxes_emlx.get(mbox, 0)
        count_index = mboxes_index.get(mbox, 0)
        count_no_ix = mboxes_no_ix.get(mbox, 0)
        sum_count_emlx += count_emlx
        sum_count_index += count_index
        if not account.startswith(account_filter):
            continue
        if prev_account != account:
            print(f'\n{account}  -  {account_info.get(account, "?")}')
            prev_account = account
        path_splitted = mbox_path.split('/')
        indention = (len(path_splitted) - 1) * 2
        path_indented = f' {" "*indention}↳ {path_splitted[-1]}'

        du_size = mboxes_du.get(mbox, 0)

        print(
            f'{path_indented:48s} {count_index:7d} {count_emlx:7d}'
            f' {du_size * 100 / total:5.1f}'
            f''' {format(count_no_ix, '4d') if count_no_ix > 0 else v*4 }'''
        )

    print(
        f'''\nAll Accounts{'𝚺':>36s} {sum_count_index:7d} {sum_count_emlx:7d}'''
        f'''{mboxes_du['total']:6d}'''
        f'{w_o_indx:5d}'
    )

def report_emlx_missing():
    print(f'\n👺  In Index w/o emlx : {w_o_emlx}')
    if ARGS.dump_no_emlx:
        for rowid in rowids_in_index - rowids_in_emlx:
            msg = MSG(rowid)
            if (
                msg.mbox_path.startswith(mbox_filter) and
                msg.account.startswith(account_filter)
            ):
            
                msg.print()

def report_index_missing():
    print(f'\n👹 emlx-Files w/o Index : {w_o_indx}')
    if ARGS.dump_no_index:
        for rowid in  rowids_in_emlx - rowids_in_index:
            elmx = EMLX(rowid)
            if (
                elmx.mbox_path.startswith(mbox_filter) and
                elmx.account.startswith(account_filter)
            ):
                elmx.print()

def report_attachments():
    attachments_sizes = Attachment.sizes()
    rowids_with_attachments = set( attachments_sizes.keys())
    sum_sizes = (512 + sum( attachments_sizes.values())) // 1024
    orphaned = len( set( rowids_with_attachments - rowids_in_emlx))
    print(f'\n🗂️ Attachments: {len(rowids_with_attachments)}, '
          f'{sum_sizes} KB, orphaned  : { orphaned} ')

    Attachment.attachments(attachments_sizes)
# ====================================

overview()

if w_o_emlx > 0:
    report_emlx_missing()

if w_o_indx  > 0:
    report_index_missing()

report_attachments()
if ARGS.nlargest_emlx is not None:
    EMLX.print_nlargest(emlx_sizes)

if ARGS.rowids is not None:
    for rowid in ARGS.rowids:
        if rowid in rowids_in_index:
            msg = MSG(rowid).print()
        if rowid in rowids_in_emlx:
            emlx = EMLX(rowid).print()


