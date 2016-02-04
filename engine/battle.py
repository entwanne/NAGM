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
"""

@meta.apply
class FakeTrainer(Trainer):
    pass

@meta.apply
class Battle(GObject):
    "Battle between trainers"

    __attributes__ = ('trainers', 'beasts')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for trainer in self.trainers:
            trainer.battle = self
        self.turn = 0
        self.turn_action = False

    @classmethod
    def from_args(cls, *args):
        args = (
            (obj, obj.beast) if isinstance(obj, Trainer)
            else (FakeTrainer(beast=obj), obj)
            for obj in args
        )
        trainers, beasts = zip(*args)
        return cls(trainers=trainers, beasts=beasts)

    def attack(self, beast, att):
        print(beast.name, 'uses', att.name)
        i = self.beasts.index(beast)
        beast.attack(att, self.beasts[not i])
        self.turn_action = False

    def end(self):
        for trainer in self.trainers:
            trainer.battle = None

    def step(self, game):
        if any(beast.ko for beast in self.beasts if beast):
            self.end()
            return
        if not self.turn_action:
            self.turn_action = True
            self.trainers[self.turn].battle_step(
                self,
                self.beasts[self.turn],
            )
            self.turn = (self.turn + 1) % len(self.trainers)

    @sighandler
    def action(self, game, player):
        pass
