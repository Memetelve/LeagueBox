import urllib3, os
from colorama import Fore

from src import ascii as art, lcu_info as lcu, external_info as external



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def dis_all_shards():
    workshop_items = lcu.request('get', '/lol-loot/v1/player-loot').json()

    for item in workshop_items:
        if item['disenchantLootName'] == "CURRENCY_champion":
            count = int(item['count'])
            name = {'recipeName': item['lootName']}
            disenchant = lcu.request('post', f'/lol-loot/v1/recipes/CHAMPION_RENTAL_disenchant/craft?repeat={count}', data=name).json()
    return


def main_screen(message=None):  # sourcery skip: remove-redundant-fstring
    art.print_ascii_art()
    print('\n')
    if message:
        print(message)
    print('\n')

    BE, shards = lcu.get_client_info()
    art.color_print(f'BE alone: {BE}', Fore.BLUE)
    art.color_print(f'All champion shards: {shards}', Fore.YELLOW)
    art.color_print(f'All champion shards + current BE: {shards + BE}', Fore.GREEN)
    art.color_print(f'Missing champions: {len(unowned_champions)}', Fore.RED)
    art.color_print(f'Missing BE: {missingBE}', Fore.RED)
    print('\n')
    return



if __name__ == '__main__':
    global owned_champions, unowned_champions, summoner_id, champ_data, missingBE, champion_list

    lcu.get_lockfile()

    print('Loading data...')

    champion_list = external.get_champion_list()
    summoner_id = lcu.get_summoner_id()
    owned_champions = lcu.get_owned_champions()
    unowned_champions, missingBE = lcu.get_unowned_champions(summoner_id, owned_champions, champion_list)

    main_screen()
    os.system('pause')
    exit(0)