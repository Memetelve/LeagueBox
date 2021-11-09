import urllib.request, json

#Get data from the link 'https://ddragon.leagueoflegends.com/api/versions.json'
#Convert to python dictionary
# Print the first element of the dictionary
def get_version():
    with urllib.request.urlopen("https://ddragon.leagueoflegends.com/api/versions.json") as url:
        data = json.loads(url.read().decode())
        return data[0]



#Get json from link 'https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json'
#Convert to python dictionary with champion_name and champion_id
def get_champion_list(version):
    with urllib.request.urlopen("https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json".format(version)) as url:
        data = json.loads(url.read().decode())
    return {data['data'][champ]['key']: champ for champ in data['data']}

print(get_champion_list(get_version()))

exit(1)

site = urllib.request.urlopen("https://ddragon.leagueoflegends.com/cdn/latest/data/en_US/champion.json")
data = json.loads(site.read())

print(data)

