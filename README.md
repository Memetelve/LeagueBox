# LeagueBox
![](https://img.shields.io/github/v/tag/Memetelve/LeagueBox?label=release&style=for-the-badge)
![](https://img.shields.io/github/downloads/Memetelve/LeagueBox/total?style=for-the-badge)
<img src="https://raw.githubusercontent.com/Memetelve/LeagueBox/master/img/main_screen.png" width="900" />

League of Legends currency helper

## Features
- Get contents of your loot
	- detect champion shards and calculate their disenchant value
	- add your BE to shard value to show how much BE you can have
- Detect owned/unowned  champions 
	- show how many are missing
	- calculate how much BE you need to buy them all (not counting what you have)

## Upcoming
- show stats for Orange Essence
- get value (OE) of skin shards/wards/emotes
- caching 

## FAQ
- Why it is taking so long?
	It is because Riot says you cant retrieve store data from lcu api, so I need to get champion prices from [cdn.merakianalytics.com](https://merakianalytics.com), it takes a moment
