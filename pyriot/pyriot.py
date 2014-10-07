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


def print_spell(spell):
    fmt = '\n{0}  RANGE: {1}  COST: {2}  COOLDOWN: {3}'
    description = fmt.format(
        spell['name'],
        spell['rangeBurn'],
        spell['costBurn'],
        spell['cooldownBurn']
    )
    print(description)
    print(spell_tooltip(spell))


def spell_tooltip(spell):
    tooltip = spell['sanitizedTooltip']

    damage_type = {
        'spelldamage': ' AP',
        'bonusattackdamage': ' bonus AD',
        'attackdamage': ' AD'
    }

    # Replace ei with effect burns (e.g. 50/60/70/80/90)
    for i in range(1, len(spell['effectBurn'])):
        tooltip = tooltip.replace(
            '{{ e' + str(i) + ' }}',
            spell['effectBurn'][i]
        )

    # Replace ai with spell coefficient and damage type
    # Some spells have no ratio
    try:
        for i in range(len(spell['vars'])):
            link = spell['vars'][i]['link']
            ratio_type = damage_type[link]

            tooltip = tooltip.replace(
                '{{ a' + str(i + 1) + ' }}',
                str(spell['vars'][i]['coeff'][0]) + ratio_type
            )
    except KeyError:
        pass

    return tooltip


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

    name = args.champ.capitalize()
    if name in champs['data'].keys():
        ch = champs['data'][name]

        ability = {
            'p': ch['passive']['sanitizedDescription'],
            'q': ch['spells'][0],
            'w': ch['spells'][1],
            'e': ch['spells'][2],
            'r': ch['spells'][3]
        }

        for i in args.spell:
            if i == 'p':
                print(ability['p'])
            else:
                print_spell(ability[i])
    else:
        print('Champion name not found.')

if __name__ == '__main__':
    main()
