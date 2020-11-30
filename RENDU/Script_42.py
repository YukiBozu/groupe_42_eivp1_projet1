#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Oct 20 21:22:50 2020

@author: lola x yukio
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from datetime import date

FICHIER = 'EIVP_KM.csv'
CAPTEURS = ['noise', 'temp', 'humidity', 'lum', 'co2']
TYPES_CAPTEURS = {'id':'Int8', 'noise':np.float32, 'temp':np.float32, 'humidity':np.float32,
                    'lum':np.float32 , 'co2':np.float32, 'sent_at':str}
VARIABLES = CAPTEURS + ['humidex']
UNITES = {'lum':'lux', 'noise':'dBa', 'temp':'°C', 'humidity':'%', 'co2':'ppm', 'humidex':''}



# lecture du fichier
def lecture_fichier(path):
    df=pd.read_csv(path, sep=';', header=0, index_col=0, dtype=TYPES_CAPTEURS, parse_dates=['sent_at'])
    df['humidex']=df.apply(lambda x: calcul_humidex(x['temp'],x['humidity']), axis=1)
    return df

def dates_croissantes(date1, date2):
    """ Remet les dates dans l'ordre si besoin
    """
    if date1 and date2 and date2 < date1:
        return date2, date1
    else:
        return date1, date2

# manque peut-être la possibilité d'appeler les variables avec des synonymes (ex: pour temp, "température" ou "temperature")

# /!\ dans les fonctions ci-dessous, les paramètres start et end peuvent ne pas être définis (=None)

def intervale_dates(df, date_deb, date_fin):
    date_deb, date_fin = dates_croissantes(date_deb, date_fin)
    if date_deb == '' or date_deb == None:
        date_deb = df['sent_at'].min()
    if date_fin == '' or date_fin == None:
        date_fin = df['sent_at'].max()
    if date_deb < df['sent_at'].min():
        date_deb = df['sent_at'].min()
    if date_fin > df['sent_at'].max():
        date_fin = df['sent_at'].max()
    if date_deb > df['sent_at'].max():
        date_deb = df['sent_at'].max()
    return date_deb, date_fin

def commande_display(df, args):
    variable = args.variable
    display(df, variable, args.start_date, args.end_date)

def display(df, nom_variable, date_deb, date_fin, withStat=False):
    date_deb, date_fin = intervale_dates(df, date_deb, date_fin)
    # filtrage par rapport aux dates
    df_filtre = df[(df['sent_at'] >= str(date_deb)) & (df['sent_at'] <= str(date_fin))]
    # tri des données selon les dates
    df_filtre_tri = df_filtre.sort_values(by=['sent_at'])

     # Sans les stats:
    if not withStat:
        titre = nom_variable
        df_filtre_tri.plot(x="sent_at", xlabel= f"date",
                             y=nom_variable , ylabel= f"{UNITES[nom_variable]}", color='blue', rot=30)
        plt.title(titre)
        plt.show()
    # Avec les stats:
    else:
        if len(df_filtre_tri.index) > 1:
            # calcul des statistiques
            data = df_filtre_tri[nom_variable]
            moyenne = data.mean()
            # moyenne_geo = data.geometric_mean()
            # moyenne_harmo = data.harmonic_mean()
            ecart_type = data.std()
            variance = data.var()
            mediane = data.median()
            min = data.min()
            max = data.max()
            # affichage de la courbe et des stats
            _, ax = plt.subplots()
            # df_filtre_tri.plot(x="sent_at", y=nom_variable, color='blue', rot=30, ax=ax)
            df_filtre_tri.plot(x="sent_at", xlabel= f"date", ax=ax,
                                y=nom_variable, ylabel= f"{UNITES[nom_variable]}", color='blue', rot=30)
            plt.axhline(moyenne, color='r', label='moyenne')
            plt.axhline(min, color='g', label='min')
            plt.axhline(max, color='c', label='max')
            plt.axhline(mediane, color='y', label='mediane')
            ax.fill_between(x=df_filtre_tri["sent_at"], y1=(moyenne - ecart_type), y2=(moyenne + ecart_type), facecolor='blue', alpha=0.5, label='intervale écart type')
            labels = [f"moyenne = {moyenne:.2f} {UNITES[nom_variable]}",
                        f"min = {min:.2f} {UNITES[nom_variable]}",
                        # "min = {:.2f} {}".format(min, UNITES[nom_variable]),
                        f"max = {max:.2f} {UNITES[nom_variable]}",
                        f"médiane = {mediane:.2f} {UNITES[nom_variable]}",
                        f"écart type = {ecart_type:.2f} {UNITES[nom_variable]}"]
            handles, _ = ax.get_legend_handles_labels()
            plt.legend(handles=handles[1:], labels=labels)
            titre = f"Statistiques de {nom_variable}, variance = {variance:.2f}"
            # print (moyenne_geo)
            # print (moyenne_harmo)
            plt.title(titre)
            plt.show()
        # Avec les stats mais dates hors de l'intervale donc df de longueur <= 1
        else:
            date_min = df['sent_at'].min().date()
            date_max = df['sent_at'].max().date()
            print(f'enter a date between [{date_min} ; {date_max}]')
            # print('enter a date between [{} ; {}]'.format(df['sent_at'].min(), df['sent_at'].max()))
    return
    

def calcul_humidex(temp, humidity):
    exp = (7.5 * temp) / (237.7 + temp)
    humidex = temp + 5/9 * 6.112 * pow(10, exp) * (humidity / 100)
    return humidex

# def display_humidex(date_deb, date_fin):
#     if date_deb == '':
#         date_deb = df['sent_at'].min()
#     if date_fin == '':
#         date_fin = df['sent_at'].max()
#     # filtrage par rapport aux dates
#     df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
#     # tri des données selon les dates
#     df_filtre_tri = df_filtre.sort_values(by=['sent_at'])
#     # calcul de l'humidex
#     df_filtre_tri['humidex'] = df_filtre_tri[['temp', 'humidity']].apply(lambda x: calcul_humidex(x[0],x[1]), axis=1)

#     # affichage
#     df_filtre_tri.plot(x="sent_at", y='humidex', color='blue', rot=30)
#     plt.title('Humidex')
#     plt.show()


def commande_displayStat(df, args):
    variable = args.variable
    display(df, variable, args.start_date, args.end_date, withStat=True)
    # displayStat(df, variable, start_date, end_date)

# def displayStat(df, nom_variable, date_deb, date_fin):
#     if date_deb == '' or date_deb == None:
#         date_deb = df['sent_at'].min()
#     if date_fin == '' or date_fin == None:
#         date_fin = df['sent_at'].max()
#     # filtrage par rapport aux dates
#     df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
#     # tri des données selon les dates
#     df_filtre_tri = df_filtre.sort_values(by=['sent_at'])
#     # calcul des statistiques
#     data = df_filtre_tri[nom_variable]
#     moyenne = data.mean()
#     ecart_type = data.std()
#     variance = data.var()
#     mediane = data.median()
#     min = data.min()
#     max = data.max()

    # # affichage de la courbe et des stats
    # _, ax = plt.subplots()
    # df_filtre_tri.plot(x="sent_at", y=nom_variable, color='blue', rot=30, ax=ax)
    # plt.axhline(moyenne, color='r', label='moyenne')
    # plt.axhline(min, color='g', label='min')
    # plt.axhline(max, color='c', label='max')
    # plt.axhline(mediane, color='y', label='mediane')
    # # ax.fill_between(x=df_filtre_tri["sent_at"], y1=(moyenne - variance), y2=(moyenne + variance))
    # ax.fill_between(x=df_filtre_tri["sent_at"], y1=(moyenne - ecart_type), y2=(moyenne + ecart_type), facecolor='blue', alpha=0.5, label='intervale écart type')
    # # plt.axhline(variance, color='k', label='variance')
    # # plt.axhline(ecart_type, color='m', label='ecart type')
    # labels = [f"moyenne = {moyenne:.2f} {UNITES[nom_variable]}",
    #             f"min = {min:.2f} {UNITES[nom_variable]}",
    #             f"max = {max:.2f} {UNITES[nom_variable]}",
    #             f"médiane = {mediane:.2f} {UNITES[nom_variable]}",
    #             f"écart type = {ecart_type:.2f} {UNITES[nom_variable]}"]
    # handles, _ = ax.get_legend_handles_labels()
    # # print("moyenne : ", moyenne)
    # # print("min : ", min)
    # # print("max : ", max)
    # # print("mediane : ", mediane)
    # # print("variance: ", variance)
    # # print("ecart type : ", ecart_type)
    # plt.legend(handles=handles[1:], labels=labels)
    # titre = "Statistiques : %s" % nom_variable
    # plt.title(titre)
    # plt.show()


def commande_correlation(df, args):
    variable1 = args.variable1
    variable2 = args.variable2
    display_correlation(df, variable1, variable2, args.start_date, args.end_date)

def display_correlation(df, variable1, variable2, date_deb, date_fin):
    date_deb, date_fin = intervale_dates(df, date_deb, date_fin)
    # filtrage par rapport aux dates
    df_filtre = df[(df['sent_at'] >= str(date_deb)) & (df['sent_at'] <= str(date_fin))]
    # tri des données selon les dates
    df_filtre_tri = df_filtre.sort_values(by=['sent_at'])
    # calcul de la corrélation entre les deux variables
    corr = df_filtre_tri[variable1].corr(df_filtre_tri[variable2], method='spearman')

    # affichage
    _, ax = plt.subplots()
    df_filtre_tri.plot(kind='line', x='sent_at', y=variable1, color='blue', ax=ax, rot=30)
    # df_filtre_tri.plot(kind='line', x="sent_at", xlabel= f"date", ax=ax,
    #                     y=variable1, ylabel= f"{variable1} ({UNITES[variable1]})", color='blue', rot=30)
    df_filtre_tri.plot(kind='line', x='sent_at', xlabel= f"date", y=variable2, color='red', ax=ax, rot=30)
    # df_filtre_tri.plot(kind='line', x="sent_at", xlabel= f"date", ax=ax,
    #                     y=variable2, ylabel= f"{variable2} ({UNITES[variable2]})", color='blue', rot=30)
    titre = "Corrélation (%s, %s) = %f" % (variable1, variable2, corr)
    plt.title(titre)
    plt.show()


def commande_display_capteurs(df, args):
    variable = args.variable
    mode = args.mode
    display_capteurs(df, variable, mode, args.start_date, args.end_date)

def display_capteurs(df, variable, mode, date_deb, date_fin):
    date_deb, date_fin = intervale_dates(df, date_deb, date_fin)
    # filtrage par rapport aux dates
    df_filtre = df[(df['sent_at'] >= str(date_deb)) & (df['sent_at'] <= str(date_fin))]
    # tri des données selon les dates
    df_filtre_tri = df_filtre.sort_values(by=['sent_at'])
    # extraction des capteurs
    capteurs = df_filtre_tri['id'].unique()
    # choix d'un graphe fusionné ou séparé
    if mode=='f':
        _, ax = plt.subplots()
    else:
        ax = None

    # affichage de chaque capteur
    colors = ['r', 'b', 'g', 'k', 'm', 'y', 'b']
    for i, capteur in enumerate(capteurs):
        df_capteur = df_filtre_tri[df_filtre_tri['id'] == capteur]
        label = "capteur %s" % capteur 
        df_capteur.plot(x="sent_at", xlabel= f"date", ax=ax,
                        y=variable, ylabel= f"{UNITES[variable]}", label=label, color=colors[i], rot=30)
    titre = "Capteurs : dimension %s" % (variable)
    plt.title(titre)
    plt.show()


def commande_similarités(df, args):
    variable = args.variable
    affichage = args.affichage
    similarités(df, variable, affichage, args.start_date, args.end_date)

def similarités(df, variable, affichage, date_deb, date_fin):
    date_deb, date_fin = intervale_dates(df, date_deb, date_fin)
    # filtrage par rapport aux dates
    df_filtre = df[(df['sent_at'] >= str(date_deb)) & (df['sent_at'] <= str(date_fin))]
    # extraction des capteurs
    nom_capteurs = df_filtre['id'].unique()
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

    elif affichage == 'c':
        # affichage des courbes
        fig, ax = plt.subplots()
        colors = ['r', 'b', 'g', 'k', 'm', 'y', 'b']
        labels = []
        for i, capteur_moy in enumerate(capteurs_moy):
            label = "capteur %s" % nom_capteurs[i]
            labels.append(label)
            # capteur_moy.plot(x="sent_at", y=variable, label=label, color=colors[i], ax=ax, rot=30)
            capteur_moy.plot(x="sent_at", xlabel= f"date", ax=ax,
                                y=variable, ylabel= f"{UNITES[variable]}", label=label, color=colors[i], rot=30)
        handles, _ = ax.get_legend_handles_labels()
        plt.legend(handles=handles[0:], labels=labels)
        titre = "Capteurs: dimension %s" % (variable)
        plt.title(titre)
        plt.show()



#--------------------------- MAIN --------------------------------------------------

COMMANDES_ACCEPTEES = ["display", "displayStat", "corrélation"]

if __name__ == '__main__':

    import argparse
    # devrait lire la première ligne du fichier csv pour récupérer les noms de variable et les mettre dans choices
    _DESCRIPTION = "TP EIVP"
    parser = argparse.ArgumentParser(description=_DESCRIPTION)
    # parser.add_argument("commande", help=f"commande parmi {COMMANDES_ACCEPTEES}")
    subparsers = parser.add_subparsers(help="commande 'display', 'displayStat' ou 'corrélation'", dest='subparser_name')

    # parse pour la commande display
    parser_a = subparsers.add_parser('display', help="display variable [start_date] [end_date]")
    parser_a.add_argument("variable", choices=VARIABLES, help="nom de la variable à plotter")
    parser_a.add_argument('start_date', nargs='?', type=date.fromisoformat, help="start_date (optionnel)")
    parser_a.add_argument('end_date', nargs='?', type=date.fromisoformat, help="end_date (optionnel)")
    parser_a.set_defaults(func=commande_display)
    # parse pour la commande displayStat
    parser_b = subparsers.add_parser('displayStat', help="displayStat variable [start_date] [end_date]")
    parser_b.add_argument("variable", choices=VARIABLES, help="nom de la variable à plotter")
    parser_b.add_argument('start_date', nargs='?', type=date.fromisoformat, help="start_date (optionnel)")
    parser_b.add_argument('end_date', nargs='?', type=date.fromisoformat, help="end_date (optionnel)")
    parser_b.set_defaults(func=commande_displayStat)
    # parse pour la commande corrélation
    parser_c = subparsers.add_parser('corrélation', aliases=['corr', 'correlation'], help="corrélation variable1 variable2 [start_date] [end_date]")
    parser_c.add_argument("variable1", choices=VARIABLES, help="nom de la variable à plotter")
    parser_c.add_argument("variable2", choices=VARIABLES, help="nom de la variable à plotter")
    parser_c.add_argument('start_date', nargs='?', type=date.fromisoformat, help="start_date (optionnel)")
    parser_c.add_argument('end_date', nargs='?', type=date.fromisoformat, help="end_date (optionnel)")
    parser_c.set_defaults(func=commande_correlation)
    # parse pour la commande display_capteurs
    parser_a = subparsers.add_parser('display_capteurs', help="display_capteurs variable fusion [start_date] [end_date]")
    parser_a.add_argument("variable", choices=CAPTEURS, help="nom de la variable à plotter")
    parser_a.add_argument('mode', choices=['f', 's'], help="type d'affichage: fusion ou séparation")
    parser_a.add_argument('start_date', nargs='?', type=date.fromisoformat, help="start_date (optionnel)")
    parser_a.add_argument('end_date', nargs='?', type=date.fromisoformat, help="end_date (optionnel)")
    parser_a.set_defaults(func=commande_display_capteurs)
    # parse pour la commande similarités
    parser_a = subparsers.add_parser('similarités', help="similarités variable affichage [start_date] [end_date]")
    parser_a.add_argument("variable", choices=VARIABLES, help="nom de la variable à plotter")
    parser_a.add_argument('affichage', choices=['m', 'c'], help="type d'affichage: matrice ou courbes")
    parser_a.add_argument('start_date', nargs='?', type=date.fromisoformat, help="start_date (optionnel)")
    parser_a.add_argument('end_date', nargs='?', type=date.fromisoformat, help="end_date (optionnel)")
    parser_a.set_defaults(func=commande_similarités)
    
    args = parser.parse_args()
    if args.subparser_name:
        df = lecture_fichier(FICHIER)
        args.func(df, args)
    else:
        print("commande 'display', 'displayStat', 'corrélation' ou 'similarités'")

# if __name__ == "__main__":
#     try:
#         df = lecture_fichier()

#         print("tableau des arguments:%s" % sys.argv)
#         # verification du nombre d'arguments en ligne de commande
#         if len(sys.argv) < 2:
#             print("Nombre d'arguments insuffisant, choisir une action parmi 'display', 'displayStat', 'corrélation', 'similarités'")
#             sys.exit(0)
#         elif len(sys.argv) < 3:
#             print("Nombre d'arguments insuffisant, choisir une variable parmi 'noise', 'temp', 'humidity', 'lum', 'co2'")
#             print("Optionnelement, choisir un intervalle de temps au format AAAA-MM-JJ")
#             sys.exit(0)

#         action = sys.argv[1]
#         # print("Optionnelement, choisir un intervalle de temps au format AAAA-MM-JJ")
#         if action in ['display', 'displayStat']:
#             # récuperation des autres arguments
#             variable = sys.argv[2]
#             if variable != 'humidex' and variable not in df.columns:
#                 print("Variable non connue, choisir une variable parmi 'noise', 'temp', 'humidity', 'lum', 'co2'")
#                 sys.exit(0)

#             # dates optionnelles
#             if len(sys.argv) > 3:
#                 try:
#                     date_deb = date.fromisoformat(sys.argv[3])
#                 except:
#                     print('Date invalide, entrer date au format : AAAA-MM-JJ')
#                     sys.exit(0)
#                 date_deb = sys.argv[3]
#             else:
#                 date_deb = ''
#             if len(sys.argv) > 4:
#                 date_fin =  sys.argv[4]
#             else:
#                 date_fin = ''

#             if action == 'display':
#                 display(df, variable, date_deb, date_fin)
#                 # if variable == 'humidex':
#                 #     display_humidex(df, date_deb, date_fin)
#                 # else:
#                 #     display(df, variable, date_deb, date_fin)
#             elif action == 'displayStat':
#                 display_stat(df, variable, date_deb, date_fin)

#         elif action == 'corrélation':
#             # récupération des autres arguments
#             variable1 = sys.argv[2]
#             variable2 = sys.argv[3]
#             if len(sys.argv) < 4:
#                 print("Nombre d'arguments insuffisant, choisir une seconde variable parmi 'noise', 'temp', 'humidity', 'lum', 'co2'")
#                 print("Optionnellement, choisir un intervalle de temps au format AAAA-MM-JJ")
#                 sys.exit(0)
#             elif not variable1 in df.columns:
#                 print("Variable 1 non connue, choisir une variable parmi 'noise', 'temp', 'humidity', 'lum', 'co2'")
#                 sys.exit(0)
#             if not variable2 in df.columns:
#                 print("Variable 2 non connue, choisir une variable parmi 'noise', 'temp', 'humidity', 'lum', 'co2'")
#                 sys.exit(0)

#             # dates optionnelles
#             if len(sys.argv) > 4:
#                 date_deb = sys.argv[4]
#             else:
#                 date_deb = ''
#             if len(sys.argv) > 5:
#                 date_fin =  sys.argv[5]
#             else:
#                 date_fin = ''

#             display_corrélation(df, variable1, variable2, date_deb, date_fin)

#         elif action == 'displayCapteurs':
#             variable = sys.argv[2]
#             fusion = False
#             if len(sys.argv) > 3:
#                 mode = sys.argv[3]
#                 if mode in ['f', 'F']:
#                     fusion = True
#                 elif mode in ['s', 'S']:
#                     fusion = False
#                 else:
#                     print("Option de courbe inconnue")
#                     sys.exit(0)

#             # dates optionnelles
#             if len(sys.argv) > 4:
#                 date_deb = sys.argv[4]
#             else:
#                 date_deb = ''
#             if len(sys.argv) > 5:
#                 date_fin = sys.argv[5]
#             else:
#                 date_fin = ''
#             display_capteurs(df, variable, fusion, date_deb, date_fin)

#         elif action == 'similarités':
#             variable = sys.argv[2]
#             affichage = 'c'
#             if len(sys.argv) > 3:
#                 affichage = sys.argv[3]
#                 if affichage not in ['m', 'c']:
#                     print("Préciser l'option d'affichage inconnue, commandes acceptées : 'm' pour matrice, 'c' pour courbe")
#                     sys.exit(0)

#             # dates optionnelles
#             if len(sys.argv) > 4:
#                 date_deb = sys.argv[4]
#             else:
#                 date_deb = ''
#             if len(sys.argv) > 5:
#                 date_fin = sys.argv[5]
#             else:
#                 date_fin = ''

#             similarités(df, variable, affichage, date_deb, date_fin)

#         else:
#             print("action inconnue")

#     except Exception as e:
#         print("Erreur rencontrée : %s" % e)
