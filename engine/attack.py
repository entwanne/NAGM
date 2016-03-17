from .gobject import GObject
from . import formula
from . import meta

@meta.apply
class Attack(GObject):
    __attributes__ = ('name', 'type', 'effects',)

    def use(self, sender, receiver):
        tr = self.type.over(receiver.type)
        ctx = {'type_rapport': tr}
        ctx.update({'s_{}'.format(attr): value for (attr, value) in sender.stats.values.items()})
        ctx.update({'r_{}'.format(attr): value for (attr, value) in receiver.stats.values.items()})

        effects = {'r': {}, 's': {}}
        for attr, form in self.effects.items():
            key, stat = attr.split('_', 1) # 'r_hp' -> 'r', 'hp' 
            diff = formula.strict_apply(form, ctx) # error if diff is not numeric
            effects[key][stat] = diff

        if effects['r']:
            receiver.apply_stats(effects['r'])
        if effects['s']:
            sender.apply_stats(effects['s'])
        return effects['s'], effects['r']
