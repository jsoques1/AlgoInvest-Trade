#!/usr/bin/env python

import csv
import time
import sys
from tools import profile

STEP = 100
BUDGET = 500 * STEP


@profile
def main():
    if len(sys.argv) == 2:
        fichier_csv = sys.argv[1]
    else:
        print(f"\nUsage: python {sys.argv[0]} fichier_donnees\n")
        sys.exit()

    debut = time.time()
    liste_actions = lire_donnees(fichier_csv)
    meilleur_portfolio = calc_knapsack_resultat(liste_actions)
    affiche_resultat(meilleur_portfolio, time.time() - debut)


def lire_donnees(fichier):
    try:
        with open(fichier) as fichier_donnees:
            next(fichier_donnees)
            donnees = csv.reader(fichier_donnees, delimiter=',')

            liste_actions = []
            for ligne in donnees:
                if float(ligne[1]) <= 0 or float(ligne[2]) <= 0:
                    pass
                else:
                    action = (ligne[0], int(float(ligne[1])*STEP), float(ligne[2]),
                              (float(ligne[1]) * float(ligne[2])) / 100)
                    liste_actions.append(action)

            return liste_actions

    except FileNotFoundError:
        print(f"\nUsage: python optimized.py fichier_donnees: Le fichier_donnees n'existe pas\n")
        sys.exit()


def calc_knapsack_resultat(liste_actions):
    budget = BUDGET
    nb_actions = len(liste_actions)
    cout = []
    profit = []

    for action in liste_actions:
        cout.append(action[1])
        profit.append(action[3])

    ks = [[0 for x in range(budget + 1)] for x in range(nb_actions + 1)]

    for i in range(1, nb_actions + 1):

        for w in range(1, budget + 1):
            if cout[i-1] <= w:
                ks[i][w] = max(profit[i-1] + ks[i-1][w-cout[i-1]], ks[i-1][w])
            else:
                ks[i][w] = ks[i-1][w]

    meilleur_portfolio = []

    while budget >= 0 and nb_actions >= 0:

        if ks[nb_actions][budget] == \
                ks[nb_actions-1][budget - cout[nb_actions-1]] + profit[nb_actions-1]:

            meilleur_portfolio.append(liste_actions[nb_actions-1])
            budget -= cout[nb_actions-1]

        nb_actions -= 1

    return meilleur_portfolio


def affiche_resultat(meilleur_portfolio, duree):
    cout = []
    profit = []
    print(f"action,\t\tcoût(€)\t\trendement(%)")

    for action in meilleur_portfolio:
        print(f"{action[0]},\t{action[1] / STEP},\t\t{action[2]}")
        cout.append(action[1])
        profit.append(action[3])

    print(f"Coût : {sum(cout) / 100} €")
    print(f"Profit : {sum(profit)} €")
    print(f"Calcul : {duree} s")


if __name__ == "__main__":
    main()
