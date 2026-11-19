"""Client minimal pour l'API REST du Rotman Interactive Trader (RIT).

API : http://localhost:9999/v1, authentification par l'en-tete X-API-Key.
"""
import time
import requests


class RITError(Exception):
    """Erreur renvoyee par l'API RIT."""


class RITClient:
    def __init__(self, api_key, base_url="http://localhost:9999/v1", timeout=5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"X-API-Key": api_key})

    # --- bas niveau -------------------------------------------------------
    def _request(self, method, path, params=None, retries=5):
        url = f"{self.base_url}{path}"
        for _ in range(retries):
            resp = self.session.request(method, url, params=params, timeout=self.timeout)
            if resp.status_code == 429:  # limite de requetes : on attend
                try:
                    wait = float(resp.json().get("wait", 0.5))
                except ValueError:
                    wait = float(resp.headers.get("Retry-After", 0.5))
                time.sleep(wait)
                continue
            if resp.status_code == 401:
                raise RITError("Cle API invalide (401).")
            if not resp.ok:
                raise RITError(f"{method} {path} -> {resp.status_code}: {resp.text}")
            return resp.json() if resp.content else None
        raise RITError(f"{method} {path} : limite de requetes depassee.")

    def _get(self, path, **params):
        return self._request("GET", path, {k: v for k, v in params.items() if v is not None})

    # --- cas / trader -----------------------------------------------------
    def case(self):
        return self._get("/case")

    def tick(self):
        return self.case()["tick"]

    def is_active(self):
        return self.case()["status"] == "ACTIVE"

    def trader(self):
        return self._get("/trader")

    def limits(self):
        return self._get("/limits")

    def news(self, since=None, limit=None):
        return self._get("/news", since=since, limit=limit)

    def assets(self, ticker=None):
        return self._get("/assets", ticker=ticker)

    # --- titres -----------------------------------------------------------
    def securities(self, ticker=None):
        return self._get("/securities", ticker=ticker)

    def book(self, ticker, limit=None):
        return self._get("/securities/book", ticker=ticker, limit=limit)

    def best_bid_ask(self, ticker):
        b = self.book(ticker, limit=1)
        bid = b["bids"][0]["price"] if b["bids"] else None
        ask = b["asks"][0]["price"] if b["asks"] else None
        return bid, ask

    def history(self, ticker, period=None, limit=None):
        return self._get("/securities/history", ticker=ticker, period=period, limit=limit)

    def time_and_sales(self, ticker, after=None, period=None, limit=None):
        return self._get("/securities/tas", ticker=ticker, after=after, period=period, limit=limit)

    def positions(self):
        return {s["ticker"]: s["position"] for s in self.securities()}

    # --- ordres -----------------------------------------------------------
    def orders(self, status="OPEN"):
        return self._get("/orders", status=status)

    def order(self, order_id):
        return self._get(f"/orders/{order_id}")

    def place_order(self, ticker, action, quantity, order_type="MARKET", price=None, dry_run=None):
        params = {"ticker": ticker, "type": order_type, "quantity": quantity, "action": action}
        if order_type == "LIMIT":
            if price is None:
                raise ValueError("Un ordre LIMIT exige un prix.")
            params["price"] = price
        if dry_run is not None:
            params["dry_run"] = int(dry_run)
        return self._request("POST", "/orders", params)

    def buy(self, ticker, quantity, price=None):
        return self.place_order(ticker, "BUY", quantity, "LIMIT" if price else "MARKET", price)

    def sell(self, ticker, quantity, price=None):
        return self.place_order(ticker, "SELL", quantity, "LIMIT" if price else "MARKET", price)

    def cancel_order(self, order_id):
        return self._request("DELETE", f"/orders/{order_id}")

    def cancel_all(self, ticker=None):
        params = {"ticker": ticker} if ticker else {"all": 1}
        return self._request("POST", "/commands/cancel", params)

    # --- offres (tenders) et baux (leases) --------------------------------
    def tenders(self):
        return self._get("/tenders")

    def accept_tender(self, tender_id, price=None):
        return self._request("POST", f"/tenders/{tender_id}", {"price": price} if price else None)

    def decline_tender(self, tender_id):
        return self._request("DELETE", f"/tenders/{tender_id}")

    def leases(self):
        return self._get("/leases")

    def lease(self, ticker, **params):
        return self._request("POST", "/leases", {"ticker": ticker, **params})

    def use_lease(self, lease_id, **params):
        return self._request("POST", f"/leases/{lease_id}", params)

    def release_lease(self, lease_id):
        return self._request("DELETE", f"/leases/{lease_id}")
