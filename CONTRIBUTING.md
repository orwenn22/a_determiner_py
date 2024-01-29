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


## Toolkit de widget (moyen, bon à avoir)

On pourrait peut-être faire un système de widgets (boutons, labels, etc) afin de réaliser les menus et 
interfaces du jeu plus facilement. Ça fonctionnerait surement de manière similaire aux objets, donc il y
a peut-être moyen de réutiser une grande partie du code existant dans ce cas ?


## Différentes formes de hitbox (ex : cercle) ("très" compliqué et probablement pas nécessaire)

Actuellement, les hitbox des objets, implémentés dans le EntityObject, sont forcément rectangulaires.
Peut-être qu'on pourrait créer un système de collisions plus complexes afin qu'une hitbox puisse être 
d'autres formes """simples""" tel que des cercles, triangles, etc.

Une autre chose qui pourrait possiblement être utile serait de prendre en compte les rotations dans les
hitbox, mais là encore, c'est très complexe de le faire de manière clean.


## Gameplay (duh)

Pour tout ce qui est gameplay, je pense que ce serait mieux qu'on en parle irl ou en visio pour déterminer
avec précision comment se déroule une partie.
