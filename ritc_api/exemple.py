"""Exemple : affiche l'etat du cas et le carnet de chaque titre.

Usage : python -m ritc_api.exemple VOTRE_CLE_API
"""
import sys
import time

from ritc_api import RITClient


def main():
    api = RITClient(sys.argv[1] if len(sys.argv) > 1 else "VOTRE_CLE_API")
    case = api.case()
    print(f"Cas: {case['name']} | statut: {case['status']} | tick: {case['tick']}")
    while api.is_active():
        for sec in api.securities():
            bid, ask = api.best_bid_ask(sec["ticker"])
            print(f"{sec['ticker']:>6} bid={bid} ask={ask} pos={sec['position']}")
        time.sleep(1)


if __name__ == "__main__":
    main()
