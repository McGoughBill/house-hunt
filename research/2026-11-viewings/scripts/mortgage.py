#!/usr/bin/env python3
"""Borrowing at a range of rates.
mortgage.py borrow MONTHLY [YEARS]   -> loan a monthly payment buys at 3.5-6.5%
mortgage.py pay LOAN [YEARS]         -> monthly payment on a loan at 3.5-6.5%"""
import sys

def pay(loan, r, years):
    i, n = r / 1200, years * 12
    return loan * i / (1 - (1 + i) ** -n)

def borrow(monthly, r, years):
    return monthly / pay(1, r, years)

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    mode, x = sys.argv[1], float(sys.argv[2]); years = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    f = borrow if mode == "borrow" else pay
    for r in [3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5]:
        print(f"{r:.1f}%  £{f(x, r, years):,.0f}")
