import psutil, time, requests, threading, json
from base64 import b64encode

from . import external_info

def request(method, path, query='', data=''):
        if query:
                url = f'{protocol}://127.0.0.1:{port}{path}?{query}'
        else:
                url = f'{protocol}://127.0.0.1:{port}{path}'
        fn = getattr(s, method)
        if data:
            return fn(url, verify=False, headers=headers, data=data)
        try:
            return fn(url, verify=False, headers=headers)
        except Exception:
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
        userpass = b64encode(bytes(f'riot:{password}', 'utf-8')).decode('ascii')
        headers = {'Authorization': f'Basic {userpass}', 'Content-Type': "application/json"}
        # Create Request session
        s = requests.session()

def get_owned_champions():
        champs_json = request('get', '/lol-champions/v1/owned-champions-minimal').json()

        return [
            champion['id'] for champion in champs_json
            if champion['ownership']['owned'] == True
        ]

def get_unowned_champions(summoner_id, owned_champions):

    all_champs = request('get', f'/lol-champions/v1/inventories/{summoner_id}/champions-minimal').json()
    unowned_champions = [champ['id'] for champ in all_champs if champ['id'] not in owned_champions]
    del unowned_champions[0]


    price = 0
    for id in unowned_champions:
        price += external_info.get_champion_price(id)


    return unowned_champions, price

def get_client_info():

    # Get wallet info
    wallet_be = request('get', '/lol-inventory/v1/wallet/ORANGE_ESSENCE').json()

    BE = int(wallet_be['lol_blue_essence'])
    OE = int(wallet_be['lol_orange_essence'])

    # Get shard info
    workshop_items = request('get', '/lol-loot/v1/player-loot').json()
    shards = 0
    unowned = []


    # Check if any champions from shards are unowned
    for item in workshop_items:
        if item['disenchantLootName'] == 'CURRENCY_champion':
            if item['itemStatus'] == 'NONE':
                unowned.append(item['itemDesc'])
            amount = item['count']
            be = item['disenchantValue']
            shards += be*amount

    return BE, OE, shards, unowned

def get_summoner_id():
    # Get summoner id
    summoner = request('get', '/lol-summoner/v1/current-summoner').json()
    return summoner['summonerId']

def get_player_masteries(summonerId):
    # Get mastery info
    masteries = request('get', f'/lol-collections/v1/inventories/{summonerId}/champion-mastery').json()

    for dictionary in masteries:
        keys_to_remove = [key for key in dictionary.keys() if key not in ['championId', 'championLevel']]
        for key in keys_to_remove:
            dictionary.pop(key)

    return masteries