# Contributing

Liste non exhaustive des trucs à faire, sans aucun ordre en particulier. 

(Il est même possible que certaines de ces tâches ne soient pas nécessaire à réaliser
selon ce qu'on veut faire dans le projet).

NOTE : il ne faut **JAMAIS** commit directement sur master (éventuellement pour des petits fixs).
Pour travailler sur une tâche, vous pouvez créer une branch sur le répo principale (ou bien fork si
vous voulez), puis faire vos modifs sur ça. Une fois que vous estimez que ce que vous avez fait est 
prêt (ou bien pour avoir le feedback des autres plus facilement), vous pouvez faire une pull request
sur github.


## Terrain bitmap destructible (compliqué, mais sûrement nécessaire)

TODO : se mettre d'accord et rédiger exactement comment on veut faire ici.


## Système basique pour gérer le state management (facile™ et bon à avoir)

Dans, le jeu, il y aura plusieurs "états" principales dans lequel peut être l'application
(par exemple menu principal, phase gameplay, menu d'options, page des crédits, etc). Afin de simplifier
le changement entre ces différents états et de d'isoler tous ces différents composants dans le code, 
il est peut-être nécessaire d'ajouter un système pour switch entre eux. Cela pourrait éventuellement
se faire avec une classe "StateManager" qui peut contenir une State, et une autre classe "State" (dont
toutes les autres states sont dérivés) contenant une référence vers le manager. (et possiblement des méthodes
update et draw affin d'être indépendant du reste du programme).


## Toolkit de widget (moyen, bon à avoir)

On pourrait peut-être faire un système de widgets (boutons, labels, etc) afin de réaliser les menus et 
interfaces du jeu plus facilement. Ça fonctionnerait surement de manière similaire aux objets, donc il y
a peut-être moyen de réutiser une grande partie du code existant dans ce cas ?


## Identifications d'objets (facile ?)

Il est important pour les objets qu'ils puissent interagir entre eux (notamment accéder aux propriétés
les un des autres, checks les collisions, etc). Cependant, actuellement, si un objet récupère un autre
objet dans l'ObjectManager, il ne lui est pas possible d'identifier de quel type d'objet il s'agit
(personnage ? projectile ? autre chose ?). 

Je vois deux solutions possibles (mais si vous avez des meilleures idées n'hésitez pas) :
1) Il est sûrement possible d'utiliser la built-in type() de python pour faire cela, mais je ne sais pas si c'est 
efficace coté performance où si ça a des répercutions sur la qualité du code. (note random: en python il est possible
de passer des types comme paramètres de fonction, il y a peut-être moyen de faire des interfaces clean sur 
l'ObjectManager avec ça)
2) Une autre option serait d'attribuer une propriété "id" à chaque type d'objet, et ainsi chaque instance de
l'objet aurait ainsi cet identifiant.


## Différentes formes de hitbox (ex : cercle) ("très" compliqué et probablement pas nécessaire)

Actuellement, les hitbox des objets, implémentés dans le EntityObject, sont forcément rectangulaires.
Peut-être qu'on pourrait créer un système de collisions plus complexes afin qu'une hitbox puisse être 
d'autres formes """simples""" tel que des cercles, triangles, etc.

Une autre chose qui pourrait possiblement être utile serait de prendre en compte les rotations dans les
hitbox, mais là encore, c'est très complexe de le faire de manière clean.


## Gameplay (duh)

Pour tout ce qui est gameplay, je pense que ce serait mieux qu'on en parle irl ou en visio pour déterminer
avec précision comment se déroule une partie.
