import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date

def lecture_fichier():
    df=pd.read_csv('EIVP_KM.csv',sep=';')
    return df

# manque peut-être la possibilité d'appeler les variables avec des synonymes (ex: pour temp, "température" ou "temperature")

# /!\ dans les fonctions ci-dessous, les paramètres start et end peuvent ne pas être définis (=None)

def commande_display(df, args):
    variable = args.variable
    start_date, end_date = dates_croissantes(args.start_date, args.end_date)
    display(df, variable, start_date, end_date)

def display(df, nom_variable, date_deb, date_fin):
    if date_deb == '' or date_deb == None:
        date_deb = df['sent_at'].min()
    if date_fin == '' or date_fin == None:
        date_fin = df['sent_at'].max()
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
    df_filtre.plot(x="sent_at", y=nom_variable, color='blue')
    plt.show()
    return

def commande_displayStat(df, args):
    variable = args.variable
    start_date, end_date = dates_croissantes(args.start_date, args.end_date)
    displayStat(df, variable, start_date, end_date)

def displayStat(df, nom_variable, date_deb, date_fin):
    if date_deb == '' or date_deb == None:
        date_deb = df['sent_at'].min()
    if date_fin == '' or date_fin == None:
        date_fin = df['sent_at'].max()
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
    data = df_filtre[nom_variable]
    moyenne = data.mean()
    ecart_type = data.std()
    variance = data.var()
    mediane = data.median()
    min = data.min()
    max = data.max()
    ax = df_filtre.plot(x="sent_at", y=nom_variable, color='blue')
    plt.axhline(moyenne, color='r', label='moyenne')
    plt.axhline(min, color='g', label='min')
    plt.axhline(max, color='g', label='max')
    plt.axhline(mediane, color='y', label='mediane')
    labels = ["moyenne", "min", "max", "mediane"]
    handles, _ = ax.get_legend_handles_labels()
    plt.text(1,50, 'ecart type %f' % ecart_type)
    plt.text(1,60, 'variance %f' % variance)
    plt.legend(handles=handles[1:], labels=labels)
    titre = "Statistiques %s" % nom_variable
    plt.title(titre)
    plt.show()
    return

# Manque fonction "display" avec variable "humidex" :

# def calcul_humidex(temp, humidity):
#     exp = 7.5 * (temp / 237.7 + temp)
#     h = temp + 5/9 * 6.112 * pow(10, exp) * humidity
#     return h

# def display_humidex(date_deb, date_fin):
#     if date_deb == '':
#         date_deb = df['sent_at'].min()
#     if date_fin == '':
#         date_fin = df['sent_at'].max()
#     df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
#     df_humidex = df_filtre[['temp', 'humidity']].apply(lambda x: calcul_humidex(x[0],x[1]))
#     df_humidex.plot(x="sent_at", y='humidex', color='blue')
#     plt.show()
#     return

def commande_correlation(df, args):
    variable1 = args.variable1
    variable2 = args.variable2
    start_date, end_date = dates_croissantes(args.start_date, args.end_date)
    correlation(df, variable1, variable2, start_date, end_date)

def correlation(df, variable1, variable2, date_deb, date_fin):
    if date_deb == '' or date_deb == None:
        date_deb = df['sent_at'].min()
    if date_fin == '' or date_fin == None:
        date_fin = df['sent_at'].max()
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
    corr = df_filtre[variable1].corr(df_filtre[variable2])
    print("correlation entre %s et %s = %f" % (variable1, variable2, corr))
    ax = plt.gca()
    df.plot(kind='line', x='sent_at', y=variable1, color='blue', ax=ax)
    df.plot(kind='line', x='sent_at', y=variable2, color='red', ax=ax)
    plt.show()
    return

# Manque fonction "similarity" + trouver automatiquement les périodes horaires d'occupation des bureaux

def dates_croissantes(date1, date2):
    """ Remet les dates dans l'ordre si besoin
    """
    if date1 and date2 and date2 < date1:
        return date2, date1
    else:
        return date1, date2


#--------------------------- MAIN --------------------------------------------------

COMMANDES_ACCEPTEES = ["display", "displayStat", "corrélation"]

if __name__ == '__main__':
    import sys
    import argparse
    # devrait lire la première ligne du fichier csv pour récupérer les noms de variable et les mettre dans choices
    _DESCRIPTION = "TP EIVP"
    parser = argparse.ArgumentParser(description=_DESCRIPTION)
    # parser.add_argument("commande", help=f"commande parmi {COMMANDES_ACCEPTEES}")
    subparsers = parser.add_subparsers(help="commande 'display', 'displayStat' ou 'corrélation'", dest='subparser_name')
    # parse pour la commande display
    parser_a = subparsers.add_parser('display', help="display variable [start_date] [end_date]")
    parser_a.add_argument("variable", choices=['noise', 'temp', 'humidity', 'lum', 'co2'], help="nom de la variable à plotter")
    parser_a.add_argument('start_date', nargs='?', type=date.fromisoformat, help="start_date")
    parser_a.add_argument('end_date', nargs='?', type=date.fromisoformat, help="end_date")
    parser_a.set_defaults(func=commande_display)
    # parse pour la commande displayStat
    parser_b = subparsers.add_parser('displayStat', help="displayStat variable [start_date] [end_date]")
    parser_b.add_argument("variable", choices=['noise', 'temp', 'humidity', 'lum', 'co2'], help="nom de la variable à plotter")
    parser_b.add_argument('start_date', nargs='?', type=date.fromisoformat, help="start_date")
    parser_b.add_argument('end_date', nargs='?', type=date.fromisoformat, help="end_date")
    parser_b.set_defaults(func=commande_displayStat)
    # parse pour la commande corrélation
    parser_c = subparsers.add_parser('corrélation', aliases=['corr', 'correlation'], help="corrélation variable1 variable2 [start_date] [end_date]")
    parser_c.add_argument("variable1", choices=['noise', 'temp', 'humidity', 'lum', 'co2'], help="nom de la variable à plotter")
    parser_c.add_argument("variable2", choices=['noise', 'temp', 'humidity', 'lum', 'co2'], help="nom de la variable à plotter")
    parser_c.add_argument('start_date', nargs='?', type=date.fromisoformat, help="start_date")
    parser_c.add_argument('end_date', nargs='?', type=date.fromisoformat, help="end_date")
    parser_c.set_defaults(func=commande_correlation)
    args = parser.parse_args()
    if args.subparser_name:
        df = lecture_fichier()
        args.func(df, args)
    else:
        print("commande 'display', 'displayStat' ou 'corrélation'")
