
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import sys


df=pd.read_csv('EIVP_KM.csv',sep=';')


def display(nom_variable, date_deb, date_fin):
    if date_deb == '':
        date_deb = df['sent_at'].min()
    if date_fin == '':
        date_fin = df['sent_at'].max()
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
    df_filtre.plot(x="sent_at", y=nom_variable, color='blue')
    plt.show()
    return


def display_stats(nom_variable, date_deb, date_fin):
    if date_deb == '':
        date_deb = df['sent_at'].min()
    if date_fin == '':
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


def calcul_humidex(temp, humidity):
    exp = 7.5 * (temp / 237.7 + temp)
    h = temp + 5/9 * 6.112 * pow(10, exp) * humidity
    return h


def display_humidex(date_deb, date_fin):
    if date_deb == '':
        date_deb = df['sent_at'].min()
    if date_fin == '':
        date_fin = df['sent_at'].max()
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
    df_humidex = df_filtre[['temp', 'humidity']].apply(lambda x: calcul_humidex(x[0],x[1]))
    df_humidex.plot(x="sent_at", y='humidex', color='blue')
    plt.show()
    return


def display_correlation(variable1, variable2, date_deb, date_fin):
    if date_deb == '':
        date_deb = df['sent_at'].min()
    if date_fin == '':
        date_fin = df['sent_at'].max()
    df_filtre = df[(df['sent_at'] >= date_deb) & (df['sent_at'] <= date_fin)]
    corr = df_filtre[variable1].corr(df_filtre[variable2])
    print("correlation entre %s et %s = %f" % (variable1, variable2, corr))
    ax = plt.gca()
    df.plot(kind='line', x='sent_at', y=variable1, color='blue', ax=ax)
    df.plot(kind='line', x='sent_at', y=variable2, color='red', ax=ax)
    plt.show()
    return


if __name__ == '__main__':
    import sys
    import argparse
    _DESCRIPTION = ""
    parser = argparse.ArgumentParser(description=_DESCRIPTION)
    parser.add_argument("display")
    parser.add_argument("displayStat")
    args = parser.parse_args()
    print(args.display)
    print(args.displayStat)
    print("fin")
    # sys.exit()


    