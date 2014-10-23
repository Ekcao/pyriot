class Spell():

    def __init__(self, spell):
        self.spell = spell
        self.vars = spell.get('vars')
        self.coeffs = self.coefficient()
        self.tooltip = self.eval_tooltip()

    def coefficient(self):
        damage_type = {
            'spelldamage': ' AP',
            'bonusattackdamage': ' bonus AD',
            'attackdamage': ' AD'
        }

        self.coeffs = {}
        if self.vars:
            for i in range(len(self.vars)):
                link = self.vars[i]['link']
                k = self.vars[i]['key']
                coeff_type = damage_type[link]
                self.coeffs[k] = str(self.vars[i]['coeff'][0]) + coeff_type

        return self.coeffs

    def eval_tooltip(self):
        self.tooltip = self.spell['sanitizedTooltip']

        # Replace ei with effect burns (e.g. 50/60/70/80/90)
        for i in range(1, len(self.spell['effectBurn'])):
            self.tooltip = self.tooltip.replace(
                '{{ e' + str(i) + ' }}',
                self.spell['effectBurn'][i]
            )

        if not self.coeffs:
            return self.tooltip

        try:
            for i in range(len(self.vars)):
                k = self.vars[i]['key']

                self.tooltip = self.tooltip.replace(
                    '{{ ' + k + ' }}',
                    self.coeffs[k]
                )
        except KeyError:
            pass

        return self.tooltip

    def __str__(self):
        s = '\n{0}\nRange: {1} | Cost: {2} | Cooldown: {3}'.format(
            self.spell['name'],
            self.spell['rangeBurn'].capitalize(),
            self.spell['resource'].replace(
                '{{ cost }}', self.spell['costBurn']
            ),
            self.spell['cooldownBurn']
        )

        s += '\n' + self.tooltip
        return s
