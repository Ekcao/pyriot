import os.path
import json
import argparse
import riotlol


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('champ', help='display a champion\'s info')
    parser.add_argument(
        'spell',
        help='spell (pqwer by default)',
        nargs='*',
        default=['p', 'q', 'w', 'e', 'r']
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
    champs = riot.champion_list(True, champ_data='all')
    args = parse()

    champ_name = args.champ.capitalize()
    if champ_name in champs['data'].keys():
        ch = champs['data'][champ_name]
        for i in args.spell:
            if i.lower() == 'p':
                print(ch['passive']['sanitizedDescription'])
            elif i.lower() == 'q':
                print("Q ability")
            elif i.lower() == 'w':
                print("W ability")
            elif i.lower() == 'e':
                print("E ability")
            elif i.lower() == 'r':
                print("R ability")
            else:
                print("Not found")
if __name__ == '__main__':
    main()
