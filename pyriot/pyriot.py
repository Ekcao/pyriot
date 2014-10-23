import os.path
import json
import argparse
import riotlol
import spell


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


# def print_spell(spell):
#     fmt = '\n{0}\nRange: {1}  Cost: {2}  Cooldown: {3}'
#     description = fmt.format(
#         spell['name'],
#         spell['rangeBurn'].capitalize(),
#         spell['resource'].replace(
#             '{{ cost }}', spell['costBurn']
#         ),
#         spell['cooldownBurn']
#     )
#     print(description)
#     print(spell_tooltip(spell))
#
#
# def coefficient(spell):
#     coeffs = {}
#
#     damage_type = {
#         'spelldamage': ' AP',
#         'bonusattackdamage': ' bonus AD',
#         'attackdamage': ' AD'
#     }
#
#     try:
#         for i in range(len(spell['vars'])):
#             coeff = spell['vars'][i]['link']
#             k = spell['vars'][i]['key']
#             coeff_type = damage_type[coeff]
#             coeffs[k] = str(spell['vars'][i]['coeff'][0]) + coeff_type
#     except KeyError:
#         pass
#
#     return coeffs
#
#
# def spell_tooltip(spell):
#     tooltip = spell['sanitizedTooltip']
#
# Replace ei with effect burns (e.g. 50/60/70/80/90)
#     for i in range(1, len(spell['effectBurn'])):
#         tooltip = tooltip.replace(
#             '{{ e' + str(i) + ' }}',
#             spell['effectBurn'][i]
#         )
#
#     coeffs = coefficient(spell)
#
#     if not coeffs:
#         return tooltip
#
#     try:
#         for i in range(len(spell['vars'])):
#             k = spell['vars'][i]['key']
#
#             tooltip = tooltip.replace(
#                 '{{ ' + k + ' }}',
#                 coeffs[k]
#             )
#     except KeyError:
#         pass
#
#     return tooltip


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
            'p': ch['passive'],
            'q': spell.Spell(ch['spells'][0]),
            'w': spell.Spell(ch['spells'][1]),
            'e': spell.Spell(ch['spells'][2]),
            'r': spell.Spell(ch['spells'][3])
        }

        for i in args.spell:
            if i == 'p':
                print('\n{0}\n{1}'.format(
                    ability[i]['name'],
                    ability[i]['sanitizedDescription']
                ))
            else:
                print(ability[i])

            print('\n_______________________________________________________')
    else:
        print('Champion name not found.')

if __name__ == '__main__':
    main()
