from .gobject import GObject
from .character import Trainer
from . import meta
from .signals import sighandler

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

@meta.apply
class FakeTrainer(Trainer):
    pass

@meta.apply
class Battle(GObject):
    "Battle between trainers"

    __attributes__ = ('trainers', 'beasts', 'trainer_actions', 'waiting')

    def __init__(self, **kwargs):
        kwargs.setdefault('trainer_actions', {})
        kwargs.setdefault('waiting', False)
        super().__init__(**kwargs)

    @classmethod
    def spawn(cls, **kwargs):
        battle = cls(**kwargs)
        for trainer in battle.trainers:
            trainer.ghostify()
            trainer.battle = battle
        return battle

    @classmethod
    def from_args(cls, *args):
        args = (
            (obj, obj.beast) if isinstance(obj, Trainer)
            else (FakeTrainer(beast=obj), obj)
            for obj in args
        )
        trainers, beasts = zip(*args)
        return cls.spawn(trainers=trainers, beasts=beasts)

    def attack(self, beast, att):
        print(beast.name, 'uses', att.name)
        i = self.beasts.index(beast)
        beast.attack(att, self.beasts[not i])
        self.waiting = False

    def end(self):
        for trainer in self.trainers:
            trainer.battle = None
            trainer.pop_ghost()

    def step(self, game):
        if len(self.trainer_actions) == len(self.trainers):
            for action, beast in self.trainer_actions.values():
                if action is None:
                    self.end()
                    return
                else:
                    self.attack(beast, action)
            self.waiting = False
            self.trainer_actions = {}
        if any(beast.ko for beast in self.beasts if beast):
            self.end()
            return
        if not self.waiting:
            self.trainer_actions = {}
            self.waiting = True
            for trainer, beast in zip(self.trainers, self.beasts):
                trainer.battle_step(self, beast)

    @sighandler
    def action(self, game, trainer, action, beast):
        self.trainer_actions[trainer] = action, beast
