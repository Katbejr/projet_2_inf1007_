# ritc_api

Client Python indépendant pour l'API REST du Rotman Interactive Trader (RIT).
Il ne réutilise aucun code de `trading_app`.

- URL par défaut : `http://localhost:9999/v1` (le client RIT doit être ouvert, API activée).
- Clé API : dans RIT, menu **API**, puis passée au constructeur.
- Gère automatiquement la limite de requêtes (HTTP 429).

```python
from ritc_api import RITClient

api = RITClient("VOTRE_CLE_API")
print(api.case())
print(api.best_bid_ask("CRZY"))
api.buy("CRZY", 100)               # ordre au marché
api.sell("CRZY", 100, price=10.5)  # ordre limite
api.cancel_all()
```

Méthodes : `case`, `tick`, `trader`, `limits`, `news`, `assets`, `securities`,
`book`, `best_bid_ask`, `history`, `time_and_sales`, `positions`, `orders`,
`order`, `place_order`, `buy`, `sell`, `cancel_order`, `cancel_all`,
`tenders`, `accept_tender`, `decline_tender`, `leases`, `lease`,
`use_lease`, `release_lease`.
