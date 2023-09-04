import requests
import json
import csv
import pprint

#build champ url
league_version = '13.17.1'
champ_name = 'Yone'
champ_url = 'http://ddragon.leagueoflegends.com/cdn/' + league_version + '/data/en_US/champion/' + champ_name + '.json'

#get json data
json_data = requests.get(champ_url)

if json_data.ok:
    
    #grab champ info
    champ_info = json_data.json()['data'][champ_name]
    #included dictionaries: allytips, blurb, enemytips, id, image, info, key, lore, name, partype, passive, recommended, skins, spells, stats, tags, title
    #pprint.pprint(champ_info)
    
    #create the csv
    csv_filename = champ_name + '_data.csv'

    with open(csv_filename, 'w', newline='') as csvfile:
        
        #grab stats
        stats_data = champ_info['stats']
        headers = [key for key in stats_data.keys()]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerow({key: value for key, value in stats_data.items()})
            
        print(f'Successfully created {csv_filename}')

else:
    print (f'Error creating CSV. Make sure the league_version and champ_name are correct.\nleague_version: {league_version}\nchamp_name: {champ_name}')