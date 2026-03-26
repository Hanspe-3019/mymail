'''
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

def print_account_info(shiftby=8) -> str:

    shift = ' '*shiftby if shiftby > 0 else ''
    print('Account Info:')
    schemas = MSG.account_info()
    for a_id, name in sorted( info_accounts().items()):
        account = a_id[:8]
        schema = schemas[account]
        print(
            f'{shift}'
            f'{account} ' 
            f'{schema:5s} '
            f'{name}' 
        )
    for account, schema in schemas.items():
        if schema != 'local':
            continue
        print(
            f'{shift}'
            f'{account} ' 
            f'{schema:5s} '
            'On my Mac' 
        )
        
