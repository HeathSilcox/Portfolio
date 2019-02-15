#-*- coding:utf-8 -*-
#
# 06/06/2016
# Heath P. Silcox
# pendu.py


import fonctions as f
import random, donnees

f.initialisation()
pseudo = input('Votre pseudo : ')
nom, score, nouveauJoueur = f.verifierScores(pseudo)

if nouveauJoueur:
	print('Bienvenue {}, vous debutez avec un score de {}.'.format(nom, score))
else:
	print('Re {}, votre score total est de {}.'.format(nom, score))

recommencer = True

while recommencer:
	motClair = random.choice(donnees.mots)
	motCache = len(motClair) * '*'
	donnees.chances = 8

	f.core(motClair, motCache)
	f.conditionWin(motClair, motCache)
	f.ajouterScores(pseudo, donnees.chances)

	flag = input("Rejouer ? (o/n)").lower()

	if flag.lower() != 'o':
		break