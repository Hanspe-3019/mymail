from urllib.parse import urlparse
from urllib.parse import unquote
from collections import defaultdict

from . consts import CON

SELECT_MSG = '''
select coalesce(a.address, base.sender)
     , coalesce(s.subject, base.subject)
     , coalesce(m.url, base.mailbox)
     , datetime(base.display_date, 'unixepoch', 'localtime')
  from messages as base
  left outer join addresses as a
     on base.sender = a.rowid
  left outer join subjects  as s
     on base.subject = s.rowid
  left outer join mailboxes as m
     on m.rowid = base.mailbox
 where base.rowid = ?
;
'''
SELECT_MBOXES = '''
select max(m.url), count(*) 
  from messages as base
  left outer join mailboxes as m
     on m.rowid = base.mailbox
 group by base.mailbox;
'''

MBOXES = { unquote(url): count for url, count in CON.execute(SELECT_MBOXES) }
ACCOUNT_TYPE = {u[1][:8] : u[0] for u in (urlparse(url) for url in MBOXES)}

class MSG:
    def __init__(self,  rowid):

        data=CON.execute(SELECT_MSG, (rowid,)).fetchone()
        (sender, subject, url_mailbox, display_date) = data
        scheme, netloc, path, *_ = urlparse(url_mailbox)
        self.mbox_path=path
        self.account=netloc[:8]
        self.rowid=rowid
        self.sender=sender
        self.subject=subject
        self.date=display_date

    def print(self):
        ''' -
        '''
        print(f'''{self.account}{self.mbox_path}
            rowid:   {self.rowid}
            Date:    {self.date}
            Sender:  {self.sender}
            Subject: {self.subject[:60]}
        '''.replace(f'''\n{' '*8}''', '\n')
            )
    def dump_rowid(self):
        ''' -
        '''
        cursor = CON.execute(
            'select * from messages where rowid=?',
            (self.rowid,)
        )
        data = cursor.fetchone()
        cols = tuple(x[0] for x in cursor.description)
        for (col, val) in zip(cols, data):
            print(f'{col} : {val}')

    @staticmethod
    def rowids():
        return set(
            rowid[0] for rowid in CON.execute(
                'select rowid from messages;'
            )
        )
    @staticmethod
    def mboxes():
        mboxes = []
        for url, cnt in MBOXES.items():
            schema, netloc, mbox_path, *_ = urlparse(url)

            mboxes.append((netloc[:8] + mbox_path, cnt))

        return { mbox : count for mbox, count in mboxes}

    @staticmethod
    def account_info():
        return ACCOUNT_TYPE

