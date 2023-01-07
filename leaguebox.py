import urllib3, os
from colorama import Fore, Back
import threading
import json

from core import ascii as art
from core import lcu_info as lcu
from core import external_info as external

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_data():
    lcu.get_lockfile()

    print("Loading data...")

    summoner_id = lcu.get_summoner_id()
    owned_champions = lcu.get_owned_champions()
    unowned_champions, missingBE = lcu.get_unowned_champions(summoner_id, owned_champions)
    blue_essence, shards, unowned = lcu.get_client_info()

    champion_dict, champion_dict_id = external.get_champion_list()

    return owned_champions, unowned_champions, missingBE, summoner_id, blue_essence, shards, unowned, champion_dict, champion_dict_id

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

    art.color_print("\n", Back.RED)
    art.color_print(f"Sanity check: {sanity_check_count} shards will be disenchanted", Back.RED)
    art.color_print("Are you sure you want to continue? (y/n)", Back.RED)

    if input().lower() not in ["y", "yes"]:
        return

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

def main_screen(message='', blue_essence=None, shards=None, unowned=None, unowned_champions=None, missingBE=None, champion_dict_id=None):
    art.print_ascii_art()

    print("\n")
    art.color_print(message, Back.YELLOW)
    print("\n")


    art.color_print(f"BE alone: {blue_essence}", Fore.BLUE)
    art.color_print(f"All champion shards: {shards}", Fore.YELLOW)
    art.color_print(f"All champion shards + current BE: {shards + blue_essence}", Fore.GREEN)
    art.color_print(f"Missing champions: {len(unowned_champions)}", Fore.RED)
    art.color_print(f"BE for those {len(unowned_champions)} champions: {missingBE}", Fore.RED)
    art.color_print("\n", Fore.RED)
    art.color_print(f"Shards of unowned champions: {len(unowned)}", Fore.YELLOW)

    unowned_champs = "".join(
        f"{champion_dict_id[str(champ_id)]}, " for champ_id in unowned_champions
    )

    print(f"\nUnowned champions: {unowned_champs}")

def main(message=''):

    owned_champions, unowned_champions, missingBE, summoner_id, blue_essence, shards, unowned, champion_dict, champion_dict_id = get_data()

    cls()
    main_screen(message, blue_essence, shards, unowned, unowned_champions, missingBE, champion_dict_id)

    print("1. Disenchant all shards (save 1 shard for every unowned champion)")
    print("2. Disenchant all shards (save 1 shard for every unowned champion + 1 or 2 for every champion you have mastery 6 or 7)")
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
        elif next_action == "9":
            exit(0)
