from itertools import combinations
import csv
import sys
import time
from tools import profile

BUDGET = 500


@profile
def main():
    if len(sys.argv) == 2:
        fichier_csv = sys.argv[1]
    else:
        print(f"\nUsage: python {sys.argv[0]} fichier_donnees\n")
        sys.exit()
    liste_actions = lire_donnees(fichier_csv)
    debut = time.time()
    meilleur_portfolio, cout_portfolio, profit_portfolio = calc_resultat(liste_actions)
    duree = time.time() - debut
    affiche_resultat(meilleur_portfolio, cout_portfolio, profit_portfolio, duree)


def lire_donnees(fichier_csv):
    with open(fichier_csv) as fichier_donnees:
        next(fichier_donnees)
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
                    break

            if total_profit > meilleur_profit:
                meilleur_profit = total_profit
                meilleur_portfolio = portfolio
                cout_portfolio = cout

    return meilleur_portfolio, cout_portfolio, meilleur_profit / 100


def affiche_resultat(meilleur_portfolio, cout, profit, duree):
    print(f"action,\t\tcoût(€)\t\trendement(%)")
    for action in meilleur_portfolio:
        print(f"{action[0]},\t{action[1]},\t\t{action[2]}")

    print(f"Coût   : {round(cout, 2)} €")
    print(f"Profit : {round(profit,2)} €")
    print(f"Calcul : {round(duree,2)} s")


if __name__ == "__main__":
    main()
