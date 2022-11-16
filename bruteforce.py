from itertools import combinations
import csv
import time
from tools import profile

BUDGET = 500
FICHIER_ACTIONS = "data/test_shares.csv"
DEBUT = time.time()


@profile
def main():
    liste_actions = lire_donnees()
    meilleur_portfolio, cout_portfolio, profit_portfolio, duree = calc_resultat(liste_actions)
    affiche_resultat(meilleur_portfolio, cout_portfolio, profit_portfolio, duree)


def lire_donnees():
    with open(FICHIER_ACTIONS) as fichier_donnees:
        donnees = csv.reader(fichier_donnees, delimiter=',')

        liste_actions = []
        for ligne in donnees:
            liste_actions.append((ligne[0], float(ligne[1]), float(ligne[2]), float(ligne[1]) * float(ligne[2])))

        return liste_actions


def calc_resultat(liste_actions):
    meilleur_profit = 0
    cout_portfolio = 0
    meilleur_portfolio = []

    for i in range(1, len(liste_actions) + 1):
        portfolios = combinations(liste_actions, i)

        for portfolio in portfolios:
            cout = 0
            total_profit = 0
            for action in portfolio:
                cout += action[1]
                if cout <= BUDGET:
                    total_profit += action[3]
                else:
                    continue

            if total_profit > meilleur_profit:
                meilleur_profit = total_profit
                meilleur_portfolio = portfolio
                cout_portfolio = cout

    duree = time.time() - DEBUT
    return meilleur_portfolio, cout_portfolio, meilleur_profit / 100, duree


def affiche_resultat(meilleur_portfolio, cout, profit, duree):
    print(f"action,\t\tcoût(€),\trendement(%))")
    for action in meilleur_portfolio:
        print(f"{action[0]},\t{action[1]},\t\t{action[2]}")

    print(f"Coût   : {cout} $")
    print(f"Profit : {profit} $")
    print(f"Calcul : {duree} s")


if __name__ == "__main__":
    main()
