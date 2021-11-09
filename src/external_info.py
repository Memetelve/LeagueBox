import urllib, json



def get_version():
    with urllib.request.urlopen("https://ddragon.leagueoflegends.com/api/versions.json") as url:
        data = json.loads(url.read().decode())
        return data[0]

def get_champion_list():
    version = get_version()

    with urllib.request.urlopen("https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json".format(version)) as url:
        data = json.loads(url.read().decode())
    return {data['data'][champ]['key']: champ for champ in data['data']}

def get_champion_price(id, champ_list):
    name = champ_list[str(id)]

    with urllib.request.urlopen(f'http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions/{name}.json') as url:
        data = json.loads(url.read().decode())

    return data['price']['blueEssence']