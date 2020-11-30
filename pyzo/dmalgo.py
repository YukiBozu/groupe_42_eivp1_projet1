#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 21:22:50 2020

@author: lola
"""

import pandas as pd
import sys

import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform


# lecture du fichier
df=pd.read_csv('EIVP_KM.csv',sep=';', parse_dates=['sent_at'])

def display(nom_variable, date_deb, date_fin):
    if date_deb == '':
        date_deb = df['sent_at'].min()
    if date_fin == '':
        date_fin = df['sent_at'].max()
    # filtrage par rapport aux dates
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
    # tri des données selon les dates
    df_filtre_tri = df_filtre.sort_values(by=['sent_at'])

    # affichage
    df_filtre_tri.plot(x="sent_at", y=nom_variable, color='blue', rot=30)
    plt.title(variable)
    plt.show()

def calcul_humidex(temp, humidity):
    exp = 7.5 * (temp / 237.7 + temp)
    h = temp + 5/9 * 6.112 * pow(10, exp) * humidity
    return temp


def display_humidex(date_deb, date_fin):
    if date_deb == '':
        date_deb = df['sent_at'].min()
    if date_fin == '':
        date_fin = df['sent_at'].max()
    # filtrage par rapport aux dates
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
    # tri des données selon les dates
    df_filtre_tri = df_filtre.sort_values(by=['sent_at'])
    # calcul de l'humidex
    df_filtre_tri['humidex'] = df_filtre_tri[['temp', 'humidity']].apply(lambda x: calcul_humidex(x[0],x[1]), axis=1)

    # affichage
    df_filtre_tri.plot(x="sent_at", y='humidex', color='blue', rot=30)
    plt.title('Humidex')
    plt.show()
    
def display_stats(nom_variable, date_deb, date_fin):
    if date_deb == '':
        date_deb = df['sent_at'].min()
    if date_fin == '':
        date_fin = df['sent_at'].max()
    # filtrage par rapport aux dates
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
    # tri des données selon les dates
    df_filtre_tri = df_filtre.sort_values(by=['sent_at'])

    # calcul des statistiques
    data = df_filtre_tri[nom_variable]
    moyenne = data.mean()
    ecart_type = data.std()
    variance = data.var()
    mediane = data.median()
    min = data.min()
    max = data.max()

    # affichage de la courbe et des stats
    fig, ax = plt.subplots()
    df_filtre_tri.plot(x="sent_at", y=nom_variable, color='blue', rot=30)
    plt.axhline(moyenne, color='r', label='moyenne')
    plt.axhline(min, color='g', label='min')
    plt.axhline(max, color='g', label='max')
    plt.axhline(mediane, color='y', label='mediane')
    labels = ["moyenne", "min", "max", "mediane"]
    handles, _ = ax.get_legend_handles_labels()
    plt.text(1,50, 'ecart type %f' % ecart_type)
    plt.text(1,60, 'variance %f' % variance)
    plt.legend(handles=handles[1:], labels=labels)
    titre = "Statistiques %s" % variable
    plt.title(titre)
    plt.show()

def display_correlation(variable1, variable2, date_deb, date_fin):
    if date_deb == '':
        date_deb = df['sent_at'].min()
    if date_fin == '':
        date_fin = df['sent_at'].max()
    # filtrage par rapport aux dates
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
    # tri des données selon les dates
    df_filtre_tri = df_filtre.sort_values(by=['sent_at'])

    # calcul de la correlation entre les deux variables
    corr = df_filtre_tri[variable1].corr(df_filtre[variable2])

    # affichage
    fig, ax = plt.subplots()
    df_filtre_tri.plot(kind='line', x='sent_at', y=variable1, color='blue', ax=ax, rot=30)
    df_filtre_tri.plot(kind='line', x='sent_at', y=variable2, color='red', ax=ax, rot=30)
    titre = "Correlation (%s, %s) = %f" % (variable1, variable2, corr)
    plt.title(titre)
    plt.show()

def display_capteurs(variable, fusion, date_deb, date_fin):
    if date_deb == '':
        date_deb = df['sent_at'].min()
    if date_fin == '':
        date_fin = df['sent_at'].max()

    # filtrage par rapport aux dates
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
    # tri des données selon les dates
    df_filtre_tri = df_filtre.sort_values(by=['sent_at'])

    # extraction des capteurs
    capteurs = df_filtre_tri['id'].unique()

    # choix d'un graphe fusionné ou séparé
    if fusion:
        fig, ax = plt.subplots()
    else:
        ax = None

    # affichage de chaque capteur
    colors = ['r', 'b', 'g', 'k', 'm', 'y', 'b']
    for i, capteur in enumerate(capteurs):
        df_capteur = df_filtre_tri[df_filtre_tri['id'] == capteur]
        label = "capteur %s" % capteur
        df_capteur.plot(x="sent_at", y=variable, label=label, color=colors[i], ax=ax, rot=30)

    titre = "Capteurs: dimension %s" % (variable)
    plt.title(titre)
    plt.show()


def display_similarites(variable, affichage, date_deb, date_fin):
    if date_deb == '':
        date_deb = df['sent_at'].min()
    if date_fin == '':
        date_fin = df['sent_at'].max()

    # filtrage par rapport aux dates
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]

    # extraction des capteurs
    nom_capteurs = df_filtre['id'].unique()

    fig, ax = plt.subplots()
    # calcul moyenne journalière de chaque capteur

    capteurs_moy = []
    for i, capteur in enumerate(nom_capteurs):
        df_capteur = df_filtre[df_filtre['id'] == capteur]
        df_capteur_date = df_capteur.set_index('sent_at')
        df_capteur_date_moy = df_capteur_date.resample('D').mean()
        df_capteur_date_moy.fillna(method="bfill", inplace=True)
        capteurs_moy.append(df_capteur_date_moy[variable])

    if affichage == 'm':
        # affichage d'une matrice de similarité
        # creation du dataframe regroupant les données des capteurs en colonnes
        capteurs_concat = pd.concat(capteurs_moy, axis=1)
        capteurs_concat.columns = nom_capteurs
        # calcul des distances euclidiennes entre colonnes dans une matrice
        capteurs_matrice = capteurs_concat.to_numpy()
        dist_matrice = squareform(pdist(capteurs_concat.T, metric='euclidean'))
        # affichage de la matrice
        fig, ax = plt.subplots()
        cax = ax.matshow(dist_matrice, interpolation='nearest')
        fig.colorbar(cax)
        titre = "Distance Capteurs: dimension %s" % (variable)
        plt.title(titre)
        plt.show()

    elif affichage in ['c', 'C']:
        # affichage des courbes
        colors = ['r', 'b', 'g', 'k', 'm', 'y', 'b']
        for i, capteur_moy in enumerate(capteurs_moy):
            label = "capteur %s" % nom_capteurs[i]
            capteur_moy.plot(x="sent_at", y=variable, label=label, color=colors[i], ax=ax, rot=30)

        titre = "Capteurs: dimension %s" % (variable)
        plt.title(titre)
        plt.show()


if __name__ == "__main__":
    try:
        print("tableau des arguments:%s" % sys.argv)
        # verification du nombre d'arguments en ligne de commande
        if len(sys.argv) < 3:
            print("Nb arguments insuffisants")
            sys.exit(0)

        action = sys.argv[1]
        if action in ['display', 'displayStats']:
            # récuperation des autres arguments
            variable = sys.argv[2]
            if variable != 'humidex' and variable not in df.columns:
                print('variable non connue')
                sys.exit(0)

            # dates optionnelles
            if len(sys.argv) > 3:
                date_deb = sys.argv[3]
            else:
                date_deb = ''
            if len(sys.argv) > 4:
                date_fin =  sys.argv[4]
            else:
                date_fin = ''

            if action == 'display':
                if variable == 'humidex':
                    display_humidex(date_deb, date_fin)
                else:
                    display(variable, date_deb, date_fin)
            elif action == 'displayStats':
                display_stats(variable, date_deb, date_fin)

        elif action == 'correlation':
            # récupération des autres arguments
            variable1 = sys.argv[2]
            variable2 = sys.argv[3]
            if not variable1 in df.columns:
                print("variable1 non connue")
                sys.exit(0)
            if not variable2 in df.columns:
                print("variable2 non connue")
                sys.exit(0)

            # dates optionnelles
            if len(sys.argv) > 4:
                date_deb = sys.argv[4]
            else:
                date_deb = ''
            if len(sys.argv) > 5:
                date_fin =  sys.argv[5]
            else:
                date_fin = ''

            display_correlation(variable1, variable2, date_deb, date_fin)

        elif action == 'displayCapteurs':
            variable = sys.argv[2]
            fusion = False
            if len(sys.argv) > 3:
                mode = sys.argv[3]
                if mode in ['f', 'F']:
                    fusion = True
                elif mode in ['s', 'S']:
                    fusion = False
                else:
                    print("Option de courbe inconnue")
                    sys.exit(0)

            # dates optionnelles
            if len(sys.argv) > 4:
                date_deb = sys.argv[4]
            else:
                date_deb = ''
            if len(sys.argv) > 5:
                date_fin = sys.argv[5]
            else:
                date_fin = ''
            display_capteurs(variable, fusion, date_deb, date_fin)

        elif action == 'displaySim':
            variable = sys.argv[2]
            affichage = 'c'
            if len(sys.argv) > 3:
                affichage = sys.argv[3]
                if affichage not in ['m', 'M', 'c', 'C']:
                    print("Option d'affichage inconnue")
                    sys.exit(0)

            # dates optionnelles
            if len(sys.argv) > 4:
                date_deb = sys.argv[4]
            else:
                date_deb = ''
            if len(sys.argv) > 5:
                date_fin = sys.argv[5]
            else:
                date_fin = ''

            display_similarites(variable, affichage, date_deb, date_fin)

        else:
            print("action inconnue")

    except Exception as e:
        print("Erreur rencontrée:%s" % e)
