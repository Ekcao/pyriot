import os.path
import json
import argparse
import riotlol


def save_champs_to_file(riot, file):
    champs = riot.champion_list(champ_data='all')
    json.dump(champs, file, sort_keys=True,
              indent=4, separators=(',', ': ')
              )

    return champs


def get_champions(riot):
    '''Checks directory for 'champs.json',
    a json file containing the list of champion data.

    If the file exists, the version is checked and updated if needed.
    Otherwise the file is created.
    '''
    champs_json = 'champs.json'
    current_patch = riot.latest_version()

    if os.path.isfile(champs_json):
        with open(champs_json, 'r+') as f:
            champs = json.load(f)
            if champs['version'] != current_patch:
                f.seek(0)
                champs = save_champs_to_file(riot, f)
    else:
        with open(champs_json, 'w') as f:
            champs = save_champs_to_file(riot, f)

    return champs['data']


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('champ', help='display a champion\'s info')
    parser.add_argument(
        'spell',
        help='spell (pqwer by default)',
        nargs='*',
        default='pqwer'
    )
    return parser.parse_args()

def main():
    info_json = 'info.json'
    if os.path.isfile(info_json):
        with open(info_json, 'r') as f:
            info = json.load(f)
    else:
        with open(info_json, 'w') as f:
            api_key = input("Enter Riot Games API key: ")
            info = {'api_key': api_key}
            json.dump(info, f, indent=4)

    riot = riotlol.RiotLOL(info['api_key'])
    champs = get_champions(riot)
    args = parse()

    champ_name = args.champ.capitalize()
    if champ_name in champs.keys():
        ch = champs[champ_name]
        for i in args.spell:
            if i.lower() == 'p':
                print(ch['passive']['sanitizedDescription'])
            else:
                print('Not found')


if __name__ == '__main__':
    main()
