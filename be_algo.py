from itertools import combinations
import csv
import time

BUDGET = 500
FICHIER_ACTIONS = "data/test_shares.csv"
DEBUT = time.time()


def main():
    liste_actions = lire_donnees()
    meilleur_portfolio, cout_portfolio, profit_portfolio = calc_resultat(liste_actions)
    affiche_resultat(meilleur_portfolio, cout_portfolio, profit_portfolio)


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

    return meilleur_portfolio, cout_portfolio, meilleur_profit / 100


def affiche_resultat(meilleur_portfolio, cout, profit):
    print(f"action,\t\tcoût($),\tprofit(%))")
    for action in meilleur_portfolio:
        print(f"{action[0]},\t{action[1]},\t\t{action[2]}")

    print(f"Coût   : {cout} $")
    print(f"Profit : {profit} $")
    print(f"Calcul : ", time.time() - DEBUT, "s")


if __name__ == "__main__":
    main()