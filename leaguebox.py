import urllib3, os
from colorama import Fore

from core import ascii as art, lcu_info as lcu, external_info as external



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main_screen(message=None):
    art.print_ascii_art()
    print('\n')
    if message:
        print(message)
    print('\n')

    BE, shards, unowned = lcu.get_client_info()
    art.color_print(f'BE alone: {BE}', Fore.BLUE)
    art.color_print(f'All champion shards: {shards}', Fore.YELLOW)
    art.color_print(f'All champion shards + current BE: {shards + BE}', Fore.GREEN)
    art.color_print(f'Missing champions: {len(unowned_champions)}', Fore.RED)
    art.color_print(f'BE for those {len(unowned_champions)} champions: {missingBE}', Fore.RED)
    print('\n')
    art.color_print(f'Shards of unowned champions: {len(unowned)}', Fore.YELLOW)


    unowned_champs = ''.join(f'{champion_dict_id[str(champ_id)]}, ' for champ_id in unowned_champions)
    print(f'\nUnowned champions: {unowned_champs}')
    return



if __name__ == '__main__':
    global champion_dict_id, champion_dict_name, owned_champions, unowned_champions, summoner_id, champ_data, missingBE

    lcu.get_lockfile()

    print('Loading data...')

    champion_dict_id, champion_dict_name = external.get_champion_list()
    summoner_id = lcu.get_summoner_id()
    owned_champions = lcu.get_owned_champions()
    unowned_champions, missingBE = lcu.get_unowned_champions(summoner_id, owned_champions, champion_dict_id)

    main_screen()

    x = input()
    exit(0)