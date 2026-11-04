"""Build one clean table, then inject realistic quality problems (thesis Table 4)."""
import random
import re
from datetime import date, timedelta

import pandas as pd

from src.data_gen.vocab import ALIASES, PRODUCTS, SUPPLIERS, TABLE_SCHEMAS

WORDS = {1: "one", 2: "two", 3: "three", 5: "five", 10: "ten"}


def _spaced(pack: str) -> str:            # "1kg" -> "1 kg"
    return re.sub(r"(\d)([A-Za-z])", r"\1 \2", pack)


def build_clean(rng: random.Random, table_type: str):
    if table_type == "inventory":
        prods = rng.sample(PRODUCTS, k=rng.randint(15, len(PRODUCTS)))
    else:
        prods = [rng.choice(PRODUCTS) for _ in range(rng.randint(40, 250))]
    is_purchase = table_type == "purchases"

    unit_price = [round(p.price * rng.uniform(0.95, 1.15) / 5) * 5 for p in prods]
    cost_price = [round(p.price * rng.uniform(0.75, 0.90) / 5) * 5 for p in prods]

    def qty(p):
        q = rng.choice([0.25, 0.5, 1, 1.5, 2, 2.5, 5]) if p.unit in ("kg", "l") else rng.randint(1, 12)
        return q * 10 if is_purchase else q

    quantity = [qty(p) for p in prods]
    price_for_total = cost_price if is_purchase else unit_price
    start = date(2025, 1, 1)
    prefix = "PO-" if is_purchase else "INV"

    cols = {
        "invoice_id": [f"{prefix}{rng.randint(1000, 9999)}" for _ in prods],
        "transaction_date": sorted(start + timedelta(days=rng.randint(0, 364)) for _ in prods),
        "product_name": [f"{p.name} {p.pack}".strip() for p in prods],
        "product_category": [p.category for p in prods],
        "supplier_name": [rng.choice(SUPPLIERS) for _ in prods],
        "quantity": quantity,
        "unit_of_measure": [p.unit for p in prods],
        "unit_price": unit_price,
        "cost_price": cost_price,
        "total_amount": [round(q * pr, 2) for q, pr in zip(quantity, price_for_total)],
        "stock_level": [rng.randint(0, 150) for _ in prods],
        "reorder_level": [rng.choice([5, 10, 15, 20, 25]) for _ in prods],
    }
    return {l: cols[l] for l in TABLE_SCHEMAS[table_type]}, prods


def _corrupt(rng, label, v, p, level):
    messy = rng.random() < level
    if label == "product_name":
        if not messy:
            return v
        n = rng.choice([p.name, p.name.lower(), p.name.upper(), p.local])
        if not p.pack:
            return n
        return rng.choice([f"{n} {p.pack}", f"{n}-{_spaced(p.pack)}",
                           f"{n.upper()} ({p.pack.upper()})", f"{n} {_spaced(p.pack)}"])
    if label == "quantity":
        if messy and rng.random() < 0.5:
            return rng.choice([f"{v} {p.unit}", f"{v}{p.unit}", WORDS.get(v, str(v))])
        return v
    if label in ("unit_price", "cost_price", "total_amount"):
        if rng.random() < level * 0.04:
            return rng.choice([0, 0.0, -abs(v)])               # zero / negative prices
        if messy and rng.random() < 0.6:
            return rng.choice([f"Rs. {v:,.2f}", f"Rs.{v:,.0f}", f"{v:,.2f}", f"LKR {v:,.2f}"])
        return v
    if label == "transaction_date":
        fmt = rng.choice(["iso", "dmy", "long"]) if messy else "iso"
        return {"iso": v.isoformat(), "dmy": v.strftime("%d/%m/%y"),
                "long": f"{v.day} {v:%b %Y}"}[fmt]            # portable on Windows
    if label == "stock_level":
        return -rng.randint(1, 20) if rng.random() < level * 0.05 else v
    if label in ("supplier_name", "product_category"):
        return rng.choice([v.lower(), v.upper(), f" {v} ", v]) if messy else v
    return v


def corrupt_column(rng, label, values, prods, level):
    out = []
    for v, p in zip(values, prods):
        if rng.random() < level * 0.12:                         # missing cell
            out.append(rng.choice([None, "", " "]))
        else:
            out.append(_corrupt(rng, label, v, p, level))
    return out


def junk_column(rng, n):                                        # label = "other"
    kind = rng.choice(["notes", "rownum", "code"])
    if kind == "rownum":
        return list(range(1, n + 1))
    if kind == "notes":
        return [rng.choice(["", "", "", "ok", "damaged", "promo", "check price", "returned", "urgent"])
                for _ in range(n)]
    return [f"X{rng.randint(100, 999)}" for _ in range(n)]


def generate_source_table(rng, table_type):
    clean, prods = build_clean(rng, table_type)
    level = rng.choice([0.2, 0.5, 0.9])                         # how messy this table is
    dirty = {l: corrupt_column(rng, l, vals, prods, level) for l, vals in clean.items()}
    if rng.random() < 0.3:
        clean["other"] = dirty["other"] = junk_column(rng, len(prods))
    order = list(dirty)
    if rng.random() < 0.5:                                      # position must not be a shortcut
        rng.shuffle(order)
    return pd.DataFrame(clean)[order], pd.DataFrame(dirty)[order], level


def make_headers(rng, labels, style, split):
    if style == "canonical":
        return list(labels)
    if style == "missing":
        return [None] * len(labels)
    if style == "generic":
        return [f"Col{i + 1}" for i in range(len(labels))]
    headers = []
    for l in labels:                                            # style == "alias"
        if split == "test" and rng.random() < 0.5:
            headers.append(rng.choice(ALIASES[l][-2:]))         # unseen aliases
        else:
            headers.append(rng.choice(ALIASES[l][:-2]))
    return headers