from .gobject import GObject
from . import formula
from . import meta

@meta.apply
class Attack(GObject):
    __attributes__ = ('name', 'type', 'effects',)

    def use(self, sender, receiver):
        tr = self.type.over(receiver.type)
        ctx = {'type_rapport': tr}
        for b, beast in (('s', sender), ('r', receiver)):
            for stat, value in beast.stats.values.items():
                ctx['{}_{}'.format(b, stat)] = value
                for attr in value.__attributes__:
                    ctx['{}_{}_{}'.format(b, stat, attr)] = getattr(value, attr)

        effects = {'r': {}, 's': {}}
        for attr, form in self.effects.items():
            key, stat = attr.split('_', 1) # 'r_hp' -> 'r', 'hp' 
            # error if value is not numeric
            effects[key][stat] = formula.strict_apply(form, ctx)

        if effects['r']:
            receiver.apply_stats(effects['r'])
        if effects['s']:
            sender.apply_stats(effects['s'])
        return set(effects['s']), set(effects['r'])
