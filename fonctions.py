#-*- coding:utf-8 -*-
#
# 06/06/2016
# Heath P. Silcox
# fonctions.py

import donnees, pickle, os, random


def initialisation():
	print()
	print('Le Pendu'.center(50))
	print('\nVous avez 8 chances pour trouver le mot.\nVos coups restants seront sauvegardes et ajoutes a votre score total.')
	print()

def verifierScores(pseudo):
	if not os.path.exists('scores'):
		with open('scores', 'wb') as fichier:
			pkl = pickle.Pickler(fichier)
			pkl.dump({pseudo:0})

		nouveauJoueur = True
		return pseudo, 0, nouveauJoueur

	with open('scores', 'rb') as fichier:
		unpkl = pickle.Unpickler(fichier)
		res_1 = unpkl.load()

	if pseudo not in res_1.keys():
		with open('scores', 'wb') as fichier:
			res_1[pseudo] = 0
			pkl = pickle.Pickler(fichier)
			pkl.dump(res_1)

		nouveauJoueur = True
		score = 0

	else:
		nouveauJoueur = False
		score = res_1[pseudo]

	return pseudo, score, nouveauJoueur

def ajouterScores(pseudo, score):
	with open('scores', 'rb') as fichier:
		unpkl = pickle.Unpickler(fichier)
		res = unpkl.load()

	res[pseudo] += score

	with open('scores', 'wb') as fichier:
		pkl = pickle.Pickler(fichier)
		pkl.dump(res)

def core(motClair, motCache):
	while donnees.chances > 0 and motClair != motCache:
		print('Mot a deviner : {}\t\tIl vous reste {} chances.'.format(motCache.upper(), donnees.chances))
		saisie = input('>>> ')

		if saisie in motClair:
			motCache = list(motCache)
			for ind, w in enumerate(motClair):
				if saisie == w:
					motCache[ind] = saisie

			motCache = ''.join(motCache)

		else:
			donnees.chances -= 1

def conditionWin(motClair, motCache):
	if motClair == motCache:
		print('\n\tBien joue ! Le mot etait', motClair.upper())
	else: 
		print('\n\tPerdu ! Le mot etait', motClair.upper())