import urllib3, os
from colorama import Fore, Back
import threading
import json

from core import ascii as art
from core import lcu_info as lcu
from core import external_info as external

from core.ascii import colored

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_data():
    lcu.get_lockfile()

    print("Loading data...")

    summoner_id = lcu.get_summoner_id()
    owned_champions = lcu.get_owned_champions()
    unowned_champions, missingBE = lcu.get_unowned_champions(summoner_id, owned_champions)
    blue_essence, orange_essence, blue_essence_shards, orange_essence_shards, unowned = lcu.get_client_info()

    champion_dict, champion_dict_id = external.get_champion_list()

    return owned_champions, unowned_champions, missingBE, summoner_id, blue_essence, orange_essence, blue_essence_shards, orange_essence_shards, unowned, champion_dict, champion_dict_id

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def disenchant_shards(mastery=False, owned=False, *, masteries=None):
    player_loot = lcu.request("get", "/lol-loot/v1/player-loot").json()

    sanity_check_count = 0

    threads = []
    for loot in player_loot:
        count = loot["count"]

        if "CHAMPION_RENTAL_" not in loot["lootName"]:
            continue

        if owned and loot["itemStatus"] != "OWNED":
            count = count - 1

        if mastery:
            for champion in masteries:
                if champion["championId"] == loot["storeItemId"]:
                    save = 7 - champion["championLevel"]
                    save = min(save, 2)
                    count = count - save
                    break
            else:
                count = count - 2

        # to ensure that we don't disenchant less than 0 shards
        count = max(count, 0)

        if count == 0:
            continue

        thread = threading.Thread(target=disenchant, args=(loot["lootName"], count))
        threads.append(thread)
        sanity_check_count += count

    colored('')
    colored(f'Sanity check: {sanity_check_count} shards will be disenchanted', color='#ffffff', bg='#FF0000')
    colored("Are you sure you want to continue? (y/n)", color='#ffffff', bg='#FF0000')

    if input().lower() not in ["y", "yes"]:
        return 'Disenchanting cancelled by user'

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return f'Done, disenchanted {sanity_check_count} shards'

def disenchant(loot_name, repeat):
    lcu.request(
        "post",
        "/lol-loot/v1/recipes/CHAMPION_RENTAL_disenchant/craft",
        query=f"repeat={repeat}",
        data=f"[{json.dumps(loot_name)}]",
    )

def main_screen(message='', blue_essence=None, orange_essence=None, blue_essence_shards=None, orange_essence_shards=None, unowned=None, unowned_champions=None, missingBE=None, champion_dict_id=None):
    art.print_ascii_art()

    print("\n")
    colored(message, color='#000000', bg='#ffff00')


    colored(f'BE alone: {blue_essence}', color='#0ACAE5')
    colored(f'OE alone: {orange_essence}', color='#F29130')
    colored(f'All champion shards: {blue_essence_shards}BE', color='#5C5B57')
    colored(f'All cosmetic shards: {orange_essence_shards}OE', color='#5C5B57')
    colored(f'All champion shards + current BE: {blue_essence_shards + blue_essence}', color='#2099e9')
    colored(f'All cosmetic shards + current OE: {orange_essence_shards + orange_essence}\n', color='#e48653')
    colored(f'Missing champions: {len(unowned_champions)}', color='#c93f38')
    colored(f'BE for those {len(unowned_champions)} champions: {missingBE}\n', color='#c93f38')
    colored(f'Shards of unowned champions: {len(unowned)}', color='#FFFF00')


    unowned_champs = "".join(unowned)
    unowned_champs = unowned_champs if unowned_champs != "" else "None"
    print(f"Unowned champion shards: {unowned_champs}")

def main(message=''):

    owned_champions, unowned_champions, missingBE, summoner_id, blue_essence, orange_essence, blue_essence_shards, orange_essence_shards, unowned, champion_dict, champion_dict_id = get_data()

    cls()
    main_screen(message, blue_essence, orange_essence, blue_essence_shards, orange_essence_shards, unowned, unowned_champions, missingBE, champion_dict_id)

    print("\n")
    print("1. Disenchant all champion shards (save 1 shard for every unowned champion)")
    print("2. Disenchant all champion shards (save 1 shard for every unowned champion + 1 or 2 for every champion under mastery 6 or 7)")
    print("2. Disenchant all champion shards (not recommended)")
    print("9. Exit")


if __name__ == "__main__":

    message = ''

    while True:
        main(message)

        next_action = input()

        if next_action == "1":
            message = disenchant_shards(owned=True)
        elif next_action == "2":
            summoner_id = lcu.get_summoner_id()
            masteries = lcu.get_player_masteries(summoner_id)
            message = disenchant_shards(mastery=True, owned=True, masteries=masteries)
        elif next_action == "3":
            message = disenchant_shards()
        elif next_action == "9":
            exit(0)
