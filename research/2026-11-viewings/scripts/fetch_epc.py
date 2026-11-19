#!/usr/bin/env python3
"""Energy certificates by postcode: floor area, band, date, improvements.
Needs EPC_API_KEY="email:key" (free, from epc.opendatacommunities.org).
Writes data/epc_<postcode>.json and data/epc_status.json."""
import base64, datetime as dt, json, os, sys
from pathlib import Path
import requests, yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"; DATA.mkdir(exist_ok=True)
API = "https://epc.opendatacommunities.org/api/v1/domestic"

def status(ok, err=None):
    (DATA / "epc_status.json").write_text(json.dumps({"ok": ok, "error": err, "at": dt.datetime.now().isoformat(timespec="seconds")}))

key = os.environ.get("EPC_API_KEY")
if not key:
    status(False, "no EPC_API_KEY"); sys.exit("fetch_epc: set EPC_API_KEY=email:key")
hdr = {"Accept": "application/json", "Authorization": "Basic " + base64.b64encode(key.encode()).decode()}
try:
    for h in yaml.safe_load((ROOT / "houses.yaml").read_text())["houses"]:
        if not h["postcode"]: continue
        pc = h["postcode"]
        r = requests.get(f"{API}/search", params={"postcode": pc, "size": 500}, headers=hdr, timeout=60); r.raise_for_status()
        certs = r.json().get("rows", [])
        for c in certs:
            rr = requests.get(f"{API}/recommendations/{c['lmk-key']}", headers=hdr, timeout=60)
            c["recommendations"] = rr.json().get("rows", []) if rr.ok and rr.text else []
        (DATA / f"epc_{pc.replace(' ', '')}.json").write_text(json.dumps(certs, indent=1))
        print(pc, len(certs))
    status(True)
except Exception as e:
    status(False, f"{type(e).__name__}: {e}"[:300]); sys.exit(f"fetch_epc failed: {e}")
