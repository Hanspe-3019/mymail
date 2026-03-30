''' Über osascript entlocken wir Mail die Namen der Accounts.
Dies wird gemischt mit dem  Schema der Mailbox-URLs aus dem Index.

In dem info-Dictionary sind nur die Mailboxen enthalten, die im Index
vorkommen.
'''
import subprocess
import json

from . msg import MSG

script = '''
const entries = Application("Mail")
    .accounts().map(
        acc => [acc.id(), acc.name()]
    );
JSON.stringify(Object.fromEntries(entries));
'''.replace('\n', '')

def info_accounts() -> dict:
    runscript = 'osascript -l JavaScript -'
    cmd = f"echo '{script}' | {runscript}"

    args = ['zsh', '-c', cmd]
    proc = subprocess.run(args, capture_output=True, check=True)

    return json.loads(proc.stdout)

def get_account_info() -> dict:

    info = {}
    schemas = MSG.account_info()
    for a_id, name in sorted( info_accounts().items()):
        account = a_id[:8]
        schema = schemas[account]
        info[account] = f'{schema:5s}  {name}'
    for account, schema in schemas.items():
        if schema != 'local':
            continue
        info[account] = f'{schema:5s}  On my Mac'
    return info
