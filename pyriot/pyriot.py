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


def spell_tooltip(champ, spell_string):
    tooltip = spell_string['sanitizedTooltip']

    damage_type = {
        'spelldamage': ' AP',
        'bonusattackdamage': ' bonus AD',
        'attackdamage': ' AD'
    }

    for i in range(1, len(spell_string['effectBurn'])):
        pattern = '{{ e' + str(i) + ' }}'
        tooltip = tooltip.replace(
            pattern,
            spell_string['effectBurn'][i]
        )

    try:
        ratio_type = str()
        spell_link = spell_string['vars'][0]['link']
        ratio_type = damage_type[spell_link]

        tooltip = tooltip.replace(
            '{{ a1 }}',
            str(spell_string['vars'][0]['coeff'][0]) + ratio_type
        )
    except KeyError:
        pass

    return tooltip


def main():
    print('')
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
                print()
            elif i.lower() == 'q':
                print(spell_tooltip(ch, ch['spells'][0]))
                print()
            elif i.lower() == 'w':
                print(spell_tooltip(ch, ch['spells'][1]))
                print()
            elif i.lower() == 'e':
                print(spell_tooltip(ch, ch['spells'][2]))
                print()
            elif i.lower() == 'r':
                print(spell_tooltip(ch, ch['spells'][3]))
                print()
            else:
                print("\nNot found")


if __name__ == '__main__':
    main()
