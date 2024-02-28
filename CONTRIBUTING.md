# Contributing

Liste non exhaustive des trucs à faire, sans aucun ordre en particulier. 

(Il est même possible que certaines de ces tâches ne soient pas nécessaire à réaliser
selon ce qu'on veut faire dans le projet).

NOTE : il ne faut **JAMAIS** commit directement sur master (éventuellement pour des petits fixs).
Pour travailler sur une tâche, vous pouvez créer une branch sur le répo principale (ou bien fork si
vous voulez), puis faire vos modifs sur ça. Une fois que vous estimez que ce que vous avez fait est 
prêt (ou bien pour avoir le feedback des autres plus facilement), vous pouvez faire une pull request
sur github.


À l'origine ce fichier contenait une liste de tâches à faire, mais la plupart ont été réalisés. Du
coup à la place, voici une liste non exhaustive d'endroits/modules importants dans la codebase


| Chemin/module   | Diminutif | Bût                                                                                              |
|-----------------|-----------|:-------------------------------------------------------------------------------------------------|
| engine.globals  | g         | - Stocker des variables globales pour le bon fonctionnement du jeu. (DT) - Fonctions pour l'I/O. |
| engine.graphics | gr        | - Fonctions de dessins qui prennent des mètres en entrée.                                        |
| engine.metrics  | m         | - Variables globales + fonction pour gérer les coordonnées en mètres.                            |
| engine.object.* | N/A       | - Contient toutes les classes liées aux objets et à la physique.                                 |
| engine.state.*  | N/A       | - Contient toutes les classes pour le management des states.                                     |
| gameplaystate   | N/A       | - Contient la state du gameplay principale.                                                      |
| playeraction.*  | N/A       | - Contient toutes les actions que peut réaliser le joueur.                                       |
| items.*         | N/A       | - Contient les classes de tous les items du jeu.                                                 |
| globalresources | res       | - Contient toutes les ressources (textures) devant être stocker durant l'exécution du programme. |
| menus.*         | N/A       | - Contient toutes les states des menus du jeu hors gameplay.                                     |


## Créer un objet

Pour ajouter un nouvel objet dans le jeu, il existe les classes EntityObject et KinematicObject pour faire cela.

```py
import engine.object.entityobject as entityobject

class MyObject(entityobject.EntityObject):
    def __init__(self, x: float, y: float, w: float, h: float, sprite):
        super().__init__(x, y, w, h, sprite)
        # Placez votre propre logique d'initialisation ici (si nécessaire).
    
    def update(self, dt: float):
        pass    # Placez votre propre logique ici

    def draw(self):
        pass    # Placez votre propre logique de rendu ici (en utilisant les fonctions de engine.graphics)
```

Une fois l'objet créer, il est possible de l'ajouter à un object manager.

```py
import myobject
import engine.object.objectmanager as objectmanager

object_manager = objectmanager.ObjectManager()
object_manager.add_object(myobject.MyObject([...]))

# Dans l'event loop
object_manager.update(dt)
# ...
object_manager.draw()

```
