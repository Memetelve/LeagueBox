import urllib, json


with urllib.request.urlopen('http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json') as url:
        champions_json = json.loads(url.read().decode())

#print(champions_json)

def get_version():
    with urllib.request.urlopen("https://ddragon.leagueoflegends.com/api/versions.json") as url:
        data = json.loads(url.read().decode())

        return data[0]

def get_champion_list():
    version = get_version()

    with urllib.request.urlopen(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json") as url:
        data = json.loads(url.read().decode())
    return {champ: data['data'][champ]['key'] for champ in data['data']}, {data['data'][champ]['key']: champ for champ in data['data']}

def get_champion_price(id):

    for champ in champions_json:

        if champions_json[champ]['id'] == id:
            return champions_json[champ]['price']['blueEssence']