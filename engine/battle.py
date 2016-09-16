from .gobject import GObject
from .character import Trainer
from .object import Object
from . import meta
from .signals import sighandler
from .map import BaseMap

from collections import OrderedDict

"""
IDÉES

Supprimer méthode action de la Battle
Dans la boucle événementielle du jeu, si un combat est en cours (game.player.battle), celui-ci aura une fonction step appelée à chaque tour, et qui s'occupera de gérer les déplacements du joueur.
Ainsi, c'est la Battle qui s'occupe de spawner des choix aux utilisateurs, et d'attendre une réponse du dresseur / du pokemon via un signal retour.
Ainsi, un joueur réel peut temporiser la réponse en fonction des événements (l'event action sera par exemple associé à un Choice qui fera utiliser une attaque), tandis qu'un PNJ répondra tout de suite

Déroulement standard de la méthod Battle.step:
- return si précédent dresseur n'a pas répondu
- Appel de trainer.battle_action(self, beast) sur le prochain dresseur
Cette méthode est ensuite différentes suivant les dresseurs (Trainer, Player).
Dans le premier cas, elle fait appel à l'IA du dresseur pour lancer un signal.
Dans le second, elle crée une boîte de dialogue Choice associée aux bons signaux.
Les signaux auront comme receveur des méthodes permettant d'utiliser une attaque ou un objet.

Dans un premier temps, ne pas implémenter les déplacements en combat ni les objets, simplement un combat tour par tour.

-> Voir la Battle comme une Map
-> mais comment faire en sorte que le joueur en combat ne quitte pas sa map actuelle ?
  - utiliser un autre event (ghost) pour mettre à la place ?
  - méthodes pour créer un ghost et pour reprendre sa place
  - les ghosts sont de simple events (n'intéragissent pas, ne se déplacent pas) non traversables

Revoir fonctionnement actuel : les deux joueurs doivent décider de leurs actions (attaque, objet) en même temps
Les actions sont exécutées ensuite.
Méthode `use` de l'attaque/objet pour l'utilisation en combat ?
`use(battle, trainer, beast, target)`
"""

class ExitBattleException(Exception):
    pass
class ExitBattle(GObject):
    def use(self, sender, target):
        raise ExitBattleException

class SwitchBeastException(Exception):
    pass
class SwitchBeast(GObject):
    def use(self, sender, beast):
        raise SwitchBeastException(beast)

class BattleView:
    '''A representation of the battle, with the pont of view of a specific trainer'''
    def __init__(self, battle, pos, adv_pos):
        self.battle = battle
        self.pos = pos
        self.adv_pos = adv_pos

    @property
    def trainer(self):
        'Self trainer'
        return self.battle.trainers[self.pos]

    @property
    def beast(self):
        'Current beast of the trainer'
        return self.battle.beasts[self.pos]

    @beast.setter
    def beast(self, b):
        self.battle.beasts[self.pos] = b

    @property
    def adv_trainer(self):
        'Adversary trainer'
        return self.battle.trainers[self.adv_pos]

    @property
    def adv_beast(self):
        'Current beast of the adversary'
        return self.battle.beasts[self.adv_pos]

    def attack(self, att, target):
        'Use an attack'
        sender = self.beast
        self.battle.actions[self] = (att, sender, target)

    def object(self, obj, target):
        'Use an object'
        self.battle.actions[self] = (obj, self.trainer, target)

    def switch(self, beast):
        'Switch beast'
        self.battle.actions[self] = (SwitchBeast(), None, beast)

    def exit(self):
        'Exit battle'
        self.battle.actions[self] = (ExitBattle(), None, None)

@meta.apply
class FakeTrainer(Trainer):
    'Class used for wild beasts'
    def ghostify(self):
        pass

    def pop_ghost(self):
        pass

@meta.apply
class Battle(BaseMap):
    "Battle between trainers"

    __attributes__ = ('trainers', 'beasts', 'actions', 'waiting')

    def __init__(self, **kwargs):
        kwargs.setdefault('actions', {})
        kwargs.setdefault('waiting', False)
        super().__init__(**kwargs)
        if len(self.beasts) != len(self.trainers):
            raise ValueError('beasts and trainers lists should have same size')
        n = len(self.trainers)
        self.views = [BattleView(self, i, (i + 1) % n) for i in range(n)]

    @classmethod
    def spawn(cls, **kwargs):
        'Create a new battle between two trainers, and move them to the battle'
        #beasts = [trainer.beasts[0] for trainer in kwargs['trainers']]
        beasts = [next(b for b in trainer.beasts if not b.ko) for trainer in kwargs['trainers']]
        battle = cls(beasts=beasts, **kwargs)
        for i, trainer in enumerate(battle.trainers):
            trainer.ghostify()
            trainer.move(7 * i + 8, 7 * i + 2, 0, battle)
            trainer.turn(0, -1)
        return battle

    @classmethod
    def from_args(cls, *args):
        'Create a battle between trainers or beasts'
        trainers = []
        for obj in args:
            if isinstance(obj, Trainer):
                trainers.append(obj)
            else:
                trainers.append(FakeTrainer(beasts=[obj]))
        return cls.spawn(trainers=trainers)

    def end(self):
        'End battle'
        for trainer in self.trainers:
            trainer.end_battle()

    def execute(self):
        'Execute trainers actions'
        # in the future, sort trainer_actions by sender.speed (or max speed if sender has no speed, e.g. sender is a trainer)
        # speed is a stat, so particular to a game
        # have a subclass of list to store actions, that will be extended by games (__iter__() -> sorted(__iter__())) or a method in Battle class to sort actions
        # how to handle on which beast an effect is applied, without repetitions ?
        for view, (action, sender, target) in self.actions.items():
            try:
                action.use(sender, target)
            except SwitchBeastException as e:
                # or no arg in exception and ask trainer to choose
                # function to choose will be necessary when a beast faints
                # or both (with arg when trainer choose to switch, without when switch is forced)
                view.beast = e.args[0]
        self.actions = {}

    def step(self, game):
        'Ask trainers the action they want to execute'
        try:
            if len(self.actions) == len(self.trainers):
                self.execute()
                self.waiting = False
            # have an exception when a beast faints
            # raised by a method of the Stat class ?
            # (when trying to set hp to 0 -> exception)
            # + better handling of all game exceptions
            if any(beast.ko for beast in self.beasts if beast):
                raise ExitBattleException
            if not self.waiting:
                self.waiting = True
                for view in self.views:
                    view.trainer.battle_step(view)
        except ExitBattleException:
            self.end()
