#!usr/bin/env python
#-*- coding:utf-8 -*-
#
# 05/02/2015
# HeathSilcox
# movejpgs.py

from listing import *
from Tkinter import *
from zipfile import *
from unidecode import unidecode
import os, shutil

class Interface(Frame):
	'''Classe de gestion de la frame principale'''
	def __init__(self, parent, repA, repB):
		'''Initialisation des objets'''
		Frame.__init__(self, parent)
		self.parent                      = parent
		self.repA                        = repA
		self.repB                        = repB

		self.g                           = GestionFichier()

		self.zoneSaisie                  = Entry(self)
		self.bouton_chantier             = Button(self)
		self.bouton_chantier['text']     = 'Chantier'
		self.bouton_chantier['command']  = self.creerChantier
		self.bouton_supprimer            = Button(self)
		self.bouton_supprimer['text']    = 'Suppr.'
		self.bouton_supprimer['command'] = self.supprimerDossier
		self.bouton_semaine              = Button(self)
		self.bouton_semaine['text']      = 'Semaine'
		self.bouton_semaine['command']   = self.runToplevel 
		self.listeDossier                = Listbox(self)

		self.zoneSaisie.bind('<Return>', self.creerChantier)
		self.listeDossier.bind('<Delete>', self.supprimerDossier)

	def placementWidgets(self):
		'''Placement des widgets'''
		self.zoneSaisie.grid(row = 0, column = 0, sticky = NSEW)
		self.bouton_chantier.grid(row = 0, column = 1, sticky = NSEW)
		self.bouton_supprimer.grid(row = 0, column = 2, sticky = NSEW)
		self.bouton_semaine.grid(row = 0, column = 3, sticky = NSEW)
		self.listeDossier.grid(row = 1, column = 0, columnspan = 4, sticky = NSEW)

		return 0
		
	def supprimerDossier(self, event = None):
		'''Supprime le dossier actif et le retire de la liste'''
		try:
			indice     = self.listeDossier.curselection()
			nomDossier = self.listeDossier.get(indice)

			os.rmdir(self.repB + '/' + nomDossier)

			self.listeDossier.delete(indice)
		except:
			pass

		return 0

	def creerChantier(self, event = None):
		'''Crée un dossier et l'ajoute à la liste'''
		try:
			saisie = self.zoneSaisie.get()
			saisie = saisie[:1].upper() + saisie[1:len(saisie)]
			saisie = '_'.join(saisie.split())
			saisie = unidecode(saisie)

			os.mkdir(self.repB + '/' + saisie)

			self.listeDossier.insert(END, saisie)
			self.zoneSaisie.delete(0, END)
		except:
			pass

		return 0

	def afficherDossier(self):
		'''Affiche les dossiers dans la listeDossier'''
		self.listeDossier.delete(0, END)

		for dossier in self.g.fListing(self.repB, 'dossier'):
			self.listeDossier.insert(END, dossier)

		return 0

	def runToplevel(self):
		'''Fonction permettant l'initialisation à la construction du Toplevel'''
		try:
			indice    = self.listeDossier.curselection()
			selection = self.listeDossier.get(indice)

			toplevel = InterfaceToplevel(self.parent, selection, self.repB, self.repA)
			toplevel.placementWidgets()
			toplevel.afficherSemaine()

			toplevel.update_idletasks()

			largeurEcran = toplevel.winfo_screenwidth()
			hauteurEcran = toplevel.winfo_screenheight()

			centrerFenetre_x = largeurEcran/2 - toplevel.winfo_width()/2
			centrerFenetre_y = hauteurEcran/2 - toplevel.winfo_height()/2

			toplevel.geometry("%dx%d+%d+%d" % (toplevel.winfo_width(), toplevel.winfo_height(), centrerFenetre_x, centrerFenetre_y))
		except:
			pass

		return 0

class InterfaceToplevel(Toplevel):
	'''Gestion du Toplevel d'Interface'''
	def __init__(self, parent, selection, repB, repA): #Le parent est la fenetre
		'''Initialisation des objets'''
		Toplevel.__init__(self, parent)
		self.parent    = parent
		self.selection = selection
		self.repA      = repA
		self.repB      = repB
		self.g         = GestionFichier()

		self.frame     = Frame(self)

		self.title('Semaine')
		self.transient(self.parent)

		self.zoneSaisie          = Entry(self.frame)
		self.bouton_creerSemaine = Button(self.frame, text = 'Créer', command = self.creerSemaine)
		self.listeSemaine        = Listbox(self.frame)
		self.bouton_delete       = Button(self.frame, text = 'Suppr.', command = self.supprimerSemaine)
		self.bouton_ouvrir       = Button(self.frame, text = 'Ouvrir', command = self.ouvrirExplorer)

		self.zoneSaisie.bind('<Return>', self.creerSemaine)
		self.listeSemaine.bind('<Delete>', self.supprimerSemaine)

	def placementWidgets(self):
		'''Positionnement des widgets'''
		self.frame.grid(row = 0, column = 0, sticky = NSEW)
		self.zoneSaisie.grid(row = 0, column = 0, sticky = NSEW)
		self.bouton_creerSemaine.grid(row = 0, column = 1, sticky = NSEW)
		self.bouton_delete.grid(row = 0, column = 2, sticky = NSEW)
		self.bouton_ouvrir.grid(row = 0, column = 3, sticky = NSEW)
		self.listeSemaine.grid(row = 1, column = 0, columnspan = 4, sticky = NSEW)

		return 0

	def creerSemaine(self, event = None):
		'''Fonction permettant de créer un sous-dossier semaine dans le dossier de la sélection courante'''
		try:
			saisie = self.zoneSaisie.get()
			saisie = saisie[:1].upper() + saisie[1:len(saisie)]
			saisie = '_'.join(saisie.split())
			saisie = unidecode(saisie)

			chemin = self.repB + '/' + self.selection + '/' + saisie

			os.mkdir(chemin)

			self.zipperDossier(chemin)
			self.deplacerImages(chemin)

			self.listeSemaine.insert(END, saisie)
			self.zoneSaisie.delete(0, END)
		except:
			pass

		return 0

	def afficherSemaine(self):
		'''Fonction qui affiche les dossiers correspondants aux semaines dans la liste'''
		self.listeSemaine.delete(0, END)

		for semaine in self.g.fListing(self.repB + '/' + self.selection, 'dossier'):
			self.listeSemaine.insert(END, semaine)

		return 0

	def supprimerSemaine(self, event = None):
		'''Supprime le dossier (si vide) correspondant, et le retire de la liste'''
		try:
			indice     = self.listeSemaine.curselection()
			nomDossier = self.listeSemaine.get(indice)

			os.rmdir(self.repB + '/' + self.selection + '/' + nomDossier)

			self.listeSemaine.delete(indice)
		except:
			pass

		return 0

	def deplacerImages(self, chemin):
		'''Fonction qui déplace les images du repSource au repCible'''
		for image in self.g.fListingType(self.g.fListing(self.repA, 'fichier'), 'jpg'):
			shutil.move(self.repA + '/' + image, chemin)

		return 0

	def zipperDossier(self, chemin):
		'''Fonction qui zip le dossier au format .zip'''
		saisie = self.zoneSaisie.get()
		saisie = saisie[:1].upper() + saisie[1:len(saisie)]
		saisie = '_'.join(saisie.split())
		saisie = unidecode(saisie)

		with ZipFile(saisie + '.zip', 'w') as fichier: 
			for image in self.g.fListingType(self.g.fListing(self.repA, 'fichier'), 'jpg'):
				fichier.write(image, os.path.basename(image))

			fichier.close()

		#shutil.move(self.repB + '/' + self.selection + '/' + saisie + '.zip', chemin)

		return 0

	def ouvrirExplorer(self):
		'''Fonction qui ouvre l'explorer au répertoire nomChantier'''
		try:
			indice = self.listeSemaine.curselection()
			selectionSemaine = self.listeSemaine.get(indice)

			chemin = self.repB + '/' + self.selection

			os.system('start ' + chemin)
		except:
			pass

		return 0

if __name__ == '__main__':
	if os.name == 'posix':
		repSrc = raw_input('Chemin du répertoire source : ')
		repTgt = raw_input('Chemin du répertoire cible : ')

	elif os.name == 'nt':
		repSrc = 'C:/Users/Heath/Pictures/Pellicule'
		repTgt = 'C:/users/Heath/Pictures'

	else:
		repSrc = raw_input('OS inconnu, renseignez le répertoire source : ')
		repTgt = raw_input('OS inconnu, renseignez le répertoire cible : ')

	fen = Tk()
	fen.title('Move JPGs')

	interface = Interface(fen, repSrc, repTgt)
	interface.placementWidgets()
	interface.afficherDossier()
	interface.grid(row = 0, column = 0, sticky = NSEW)

	fen.update_idletasks()

	largeurEcran = fen.winfo_screenwidth()
	hauteurEcran = fen.winfo_screenheight()

	centrerFenetre_x = largeurEcran/2 - fen.winfo_width()/2
	centrerFenetre_y = hauteurEcran/2 - fen.winfo_height()/2

	fen.geometry("%dx%d+%d+%d" % (fen.winfo_width(), fen.winfo_height(), centrerFenetre_x, centrerFenetre_y))

	fen.mainloop()

