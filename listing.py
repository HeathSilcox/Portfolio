#!usr/bin/env python
#-*- coding: utf-8 -*-
#
# 14/12/2014
# HeathSilcox
# listing.py

import os, sys, shutil
from itertools import chain

class GestionFichier(object):
	def __init__(self):
		self.rep_cour = os.getcwd()

	def fListing(self, rep, filtre):
		'''Fonction qui renvoie un listing du répertoire rep, avec différents filtres : fichier, dossier, all'''
		
		if not os.path.exists(rep):
			return 0
		if filtre != 'fichier' and filtre != 'dossier' and filtre != 'all':
			return 0

		os.chdir(rep)
		li_fichier = []
		li_dossier = []
		li_all     = []

		for x in os.listdir(rep):
			li_all.append(x)
			if os.path.isfile(x):
				li_fichier.append(x)
			elif os.path.isdir(x):
				li_dossier.append(x)

		if filtre == 'fichier':
			return li_fichier
		elif filtre == 'dossier':
			return li_dossier
		elif filtre == 'all':
			return li_all

	def fListingType(self, liste, filtre):
		'''Fonction qui renvoie une liste en utilisant une liste et un filtre à types de fichiers (jpg, png, bmp, gif, tiff)'''

		filtre_liste = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff']

		if not type(liste) == list:
			return 0
		if not filtre in filtre_liste:
			return 0

		li_jpg  = []
		li_jpeg = []
		li_png  = []
		li_bmp  = []
		li_gif  = []
		li_tiff = []

		for element in liste:
			if element.endswith('jpg') and filtre == 'jpg':
				li_jpg.append(element)

			elif element.endswith('jpeg') and filtre == 'jpeg':
				li_jpeg.append(element)

			elif element.endswith('png') and filtre == 'png':
				li_png.append(element)

			elif element.endswith('bmp') and filtre == 'bmp':
				li_bmp.append(element)

			elif element.endswith('gif') and filtre == 'gif':
				li_gif.append(element)

			elif element.endswith('tiff') and filtre == 'tiff':
				li_tiff.append(element)

		if filtre == 'jpg':
			return li_jpg
		elif filtre == 'jpeg':
			return li_jpeg
		elif filtre == 'png':
			return li_png
		elif filtre == 'bmp':
			return li_bmp
		elif filtre == 'gif':
			return li_gif
		elif filtre == 'tiff':
			return li_tiff

	def fSmartFilesMove(self, repATrier, liste):
		'''Fonction qui range intelligement un répertoire selon la liste de fichiers envoyée (jpg, png, etc.. dans images, etc...)
		e.g : 
		listing = fListing(rep, 'fichier')
		fSmartFilesMove(rep, listing)
		'''

		if not os.path.exists(repATrier):
			return 0
		if not type(liste) == list:
			return 0
		
		li_jpg = self.fListingType(liste, 'jpg') #Contient les noms de fichiers de liste avec l'extension .jpg
		li_jpeg = self.fListingType(liste, 'jpeg')
		li_png = self.fListingType(liste, 'png')
		li_bmp = self.fListingType(liste, 'bmp')
		li_gif = self.fListingType(liste, 'gif')
		li_tiff = self.fListingType(liste, 'tiff')

		for image in chain(li_jpg, li_jpeg, li_png, li_bmp, li_gif):
			shutil.move(repATrier + '/' + image, 'C:/Users/Heath/Pictures/Pellicule')


if __name__ == '__main__':
	gestion = GestionFichier()
	rep = raw_input('Repertoire a trier : ')
	liste = gestion.fListing(rep, 'fichier')
	gestion.fSmartFilesMove(rep, liste)

	#print help(GestionFichier)

