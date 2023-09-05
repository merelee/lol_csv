import requests
import json
import csv

#get data dragon version, and build base champ url
versions_file = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
version_check = versions_file.json()[0]
base_url = 'http://ddragon.leagueoflegends.com/cdn/' + version_check + '/data/en_US/champion/'

#get list of champions
with open('champions.json', 'r') as file:
    data = json.load(file)
    
champ_list = data['champions']

#create the csv
csv_filename = 'champion_data_' + version_check + '.csv'
print(f'Creating {csv_filename}...')

with open(csv_filename, 'w', newline='') as csvfile:
    writer = None
    error = False

    #loop through list of champions to grab json data
    for champ in champ_list:
        champ_id = champ['id']
        champ_name = champ['name']
        champ_url = base_url + champ_id + '.json'
        json_data = requests.get(champ_url)
        
        #check if url gives status code 2xx, then grab champ info
        if json_data.ok:
            champ_info = json_data.json()['data'][champ_id]
            #included dictionaries: allytips, blurb, enemytips, id, image, info, key, lore, name, partype, passive, recommended, skins, spells, stats, tags, title

            #first champ
            if writer is None:
                stats_data = champ_info['stats']
                headers = ['name'] + [key for key in stats_data.keys()] #writes headers (name, then stats)
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()

            #subsequent champs
            row_data = {'name': champ_name}
            row_data.update({key: value for key, value in champ_info['stats'].items()})
            writer.writerow(row_data)
            
        else:
            error = True
            
    if error:
        print ('There was an error adding champion data.')

print(f'Successfully created {csv_filename}')