import os.path
import json
import argparse
import riotlol
import spell


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('champ', help='display a champion\'s info')
    parser.add_argument('spell',
                        help='spell (pqwer by default)',
                        nargs='*',
                        default=['p', 'q', 'w', 'e', 'r'])
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
    champs = riot.champion_list_from_file(champ_data='all')
    args = parse()

    name = args.champ.capitalize()
    if name in champs['data'].keys():
        ch = champs['data'][name]

        ability = {
            'p': ch['passive'],
            'q': spell.Spell(ch['spells'][0]),
            'w': spell.Spell(ch['spells'][1]),
            'e': spell.Spell(ch['spells'][2]),
            'r': spell.Spell(ch['spells'][3])
        }

        for i in args.spell:
            if i == 'p':
                print('\n{0}\n{1}'.format(ability[i]['name'],
                                          ability[i]['sanitizedDescription']))
            else:
                print(ability[i])

            print('\n_______________________________________________________')
    else:
        print('Champion name not found.')


if __name__ == '__main__':
    main()
