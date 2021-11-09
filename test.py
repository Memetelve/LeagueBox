import os, requests, urllib3, logging, time, psutil, json
from colorama import Fore, Back, Style
from base64 import b64encode
from src import ascii as art

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def request(method, path, query='', data=''):
        if query:
            url = '%s://%s:%s%s?%s' % (protocol, '127.0.0.1', port, path, query)
        else:
            url = '%s://%s:%s%s' % (protocol, '127.0.0.1', port, path)
        fn = getattr(s, method)
        if data:
            return fn(url, verify=False, headers=headers, json=data)
        try:
            return fn(url, verify=False, headers=headers)
        except:
            return 0

# Get path of running process with specified name
def exe_path(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return str(proc.exe())[:-len(process_name)]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None




def get_lockfile():
        lockfile = None
        print('Waiting for League of Legends to start ..')
        while not lockfile:
                while True:
                        lockpath = exe_path('LeagueClient.exe')
                        if lockpath is None:
                            time.sleep(2)
                            continue
                        print(f'Found running League of Legends, {lockpath}')
                        break

                lockfile = open(r'%s\lockfile' % lockpath, 'r')

        # Read the lock file data
        lockdata = lockfile.read()
        lockfile.close()
        # Parse the lock data

        global procname, pid, protocol, port

        lock = lockdata.split(':')
        procname = lock[0]
        pid = lock[1]
        protocol = lock[4]
        port = lock[2]
        password = lock[3]

        global userpass, headers, s
        userpass = b64encode(bytes('%s:%s' % ('riot', password), 'utf-8')).decode('ascii')
        headers = { 'Authorization': 'Basic %s' % userpass }
        # Create Request session
        s = requests.session()


get_lockfile()
#abc = '/lol-champions/v1/inventories/61663941/champions-minimal'
#abc = '/lol-champions/v1/inventories/61663941/champions/8'


abc = [['/lol-loot/v1/player-loot', 'get']]
for i in abc:
    file_name = (i[0].replace('/', '-'))[1:]

    print(request(i[1], i[0]).json())

    with open(f'json/{file_name}.json', 'w') as f:
        f.write(request(i[1], i[0]).text)
        f.close()
