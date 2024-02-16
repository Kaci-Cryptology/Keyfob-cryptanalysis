# Introduction

Ce dépôt fournit une description complète du cryptosystème Hitag-2, basée sur l'étude de plusieurs articles scientifiques. Vous pouvez trouver ce document dans le répertoire "Hitag-2 cryptanalysis". Il comprend également des implémentations de chaque attaque et des optimisations possibles

# Implémentations 

* `BruteForce.ipynb`: Ce fichier comprend à la fois l'algorithme Hitag2 et une attaque de type bruteforce qui cible la clé secrète sur un processeur central (CPU) en utilisant Python
* `GDop1.ipynb`:Une première optimisation de l'attaque bruteforce, l'attaque Guess and Determine version récursive. Elle cible l'état initial qui a généré le keystream, puis permet de récupérer la clé secrète
* `GDop2.ipynb`: Une deuxième optimisation qui consiste à supprimer la récursion de l'attaque, améliorant ainsi son efficacité

* `GDop3.ipynb`: Une troisième optimisation consiste à précalculer les fonctions 'expand' et 'f' et à les stocker dans des tableaux afin d'éviter leur appel à chaque itération de la boucle
* `GDop4.ipynb`: Une dernière optimisation consiste à précalculer et à mémoriser les sous-filtres, améliorant ainsi les performances en évitant de recalculer ces valeurs à chaque utilisation

* `BruteForceGPU.ipynb`: Une version parallèle de l'attaque bruteforce est implémentée en utilisant Numba CUDA, permettant une exécution simultanée sur plusieurs processeurs graphiques.
* `BruteForce.py GDop1.py GDop2.py and GDop3.py`: Tous les fichiers .py ne doivent pas être exécutés directement, ils servent de code source pour les notebooks

# Exécution 

Pour exécuter les différentes attaques, il suffit de :

# Pour les fichiers .ipynb, toutes les instructions nécessaires sont fournies dans le notebook lui-même. Il suffit de suivre les indications qui y sont données.
# Pour la version OpenCL, vous trouverez un fichier README qui explique en détail le déroulement et l'exécution de l'attaque.
