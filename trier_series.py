#-*- coding:utf-8 -*-
#
# 15/04/2015
# HeathSilcox
# trier_series.py

import os
import tkFileDialog as tkf
from tkinter import *
from tkinter import filedialog
from allmodules import *
from itertools import chain

class Interface(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.title('trier_series.py')

		self.defaut = StringVar(self)
		self.defaut.set('Saison 1')
		self.valeur = IntVar(self)
		self.valeur.set(2)

		self.l_nom   = Label(self, text = 'Nom de la série ')
		self.nom     = Entry(self)
		self.label   = Label(self, text = 'Choisir le dossier ')
		self.b       = Button(self, text = 'Parcourir', command = self.recupererChemin)
		self.formatA = Radiobutton(self, text = 'Nom - S01E01, Nom - S02E10..', value = 1, command = lambda: self.valeur.set(1))
		self.formatB = Radiobutton(self, text = 'Nom - A01, Nom - B10..', value = 2, command = lambda: self.valeur.set(2))
		self.saison  = OptionMenu(self, self.defaut, 'Saison 1', 'Saison 2', 'Saison 3', 'Saison 4', 'Saison 5', 'Saison 6', 'Saison 7', 'Saison 8', 'Saison 9')
		self.b_creer = Button(self, text = 'Créer', command = self.creer)

		self.chemin = str()

	def placementWidgets(self):
		self.l_nom.grid(row   = 0, column = 0, sticky = NE)
		self.nom.grid(row     = 0, column = 1, sticky = NSEW)
		self.label.grid(row   = 1, column = 0, sticky = NE)
		self.b.grid(row       = 1, column = 1, sticky = NSEW)
		self.formatA.grid(row = 2, column = 0, columnspan = 2, sticky = NW)
		self.formatB.grid(row = 3, column = 0, columnspan = 2, sticky = NW)
		self.saison.grid(row  = 4, column = 0, columnspan = 2, sticky = NSEW)
		self.b_creer.grid(row = 5, column = 0, columnspan = 2, sticky = NSEW)

	def recupererChemin(self):
		self.chemin = filedialog.askdirectory()

	def creer(self):
		#Nom de la série = self.nom.get()
		#Nom du dossier  = self.chemin
		#Format          = self.valeur.get()
		#Saison          = self.defaut.get()
		#Format 1        = Nom - S1E01
		#Format 2        = Nom - A01

		videos = MonModule().listing(self.chemin, 'fichier')
		if os.path.exists(self.chemin + '/' + 'Thumbs.db'):
			videos.remove('Thumbs.db')
		saisons = list()
		formatA = list()
		formatB = list()
		[saisons.append('Saison ' + str(n+1)) for n in range(9)]
		[formatA.append('S0' + str(n+1)) for n in range(9)]
		[formatB.append(n) for n in 'ABCDEFGHI'] ; n = 0


		if self.valeur.get() == 1: #Si c'est le format 1
			suffixes = list()

			for saison, fA in zip(saisons, formatA): #On parcourt Saison et S
				if self.defaut.get() == saison: #Choix user == Saison 1,2,3..9 ?
					for n in range(len(videos)):
						if n < 9:
							suffixes.append(fA + 'E0' + str(n+1))
						else:
							suffixes.append(fA + 'E' + str(n+1))


		if self.valeur.get() == 2: #Si c'est le format 2
			suffixes = list()

			for saison, fB in zip(saisons, formatB):
				if self.defaut.get() == saison:
					for n in range(len(videos)):
						if n < 9:
							suffixes.append(fB + '0' + str(n+1))
						else:
							suffixes.append(fB + str(n+1))

 
		for video, suf in zip(videos, suffixes):
			nom, extension = os.path.splitext(video)

			os.rename(video, self.nom.get() + ' - ' + suf + extension)



interface = Interface()
interface.placementWidgets()

interface.mainloop()


























