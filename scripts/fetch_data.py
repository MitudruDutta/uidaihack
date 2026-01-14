import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.data.gov.in/resource"

DATASETS = {
    "enrolment": "ecd49b12-3084-4521-8f7e-ca8bf72069ba",
    "biometric": "65454dab-1517-40a3-ac1d-47d4dfe6891c",
    "demographic": "19eac040-0b94-49fa-b239-4f2fd8677d53"
}

STATES = [
    "Tamil Nadu", "Andhra Pradesh", "Uttar Pradesh", "West Bengal", "Maharashtra",
    "Karnataka", "Kerala", "Gujarat", "Odisha", "Rajasthan", "Bihar", "Telangana",
    "Madhya Pradesh", "Assam", "Punjab", "Jharkhand", "Chhattisgarh", "Himachal Pradesh",
    "Haryana", "Uttarakhand", "Jammu and Kashmir", "Delhi", "Tripura", "Manipur",
    "Goa", "Meghalaya", "Arunachal Pradesh", "Nagaland", "Mizoram", "Sikkim",
    "Puducherry", "Chandigarh", "Andaman and Nicobar Islands", "Ladakh",
    "Dadra and Nagar Haveli and Daman and Diu", "Lakshadweep"
]

def fetch_dataset(name, resource_id, limit=10000):
    all_records = []
    for state in STATES:
        offset = 0
        state_count = 0
        print(f"[{name}] {state}...", end=" ", flush=True)
        
        while True:
            try:
                resp = requests.get(f"{BASE_URL}/{resource_id}", params={
                    "api-key": API_KEY, "format": "json",
                    "limit": limit, "offset": offset, "filters[state]": state
                }, timeout=30)
                records = resp.json().get("records", [])
                if not records:
                    break
                all_records.extend(records)
                state_count += len(records)
                offset += limit
                if len(records) < limit:
                    break
                time.sleep(0.1)
            except Exception as e:
                print(f"Error: {e}")
                break
        print(state_count)
    return pd.DataFrame(all_records)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    for name, rid in DATASETS.items():
        print(f"\n=== {name.upper()} ===")
        df = fetch_dataset(name, rid)
        df.to_csv(f"data/{name}.csv", index=False)
        print(f"Saved: {len(df)} records")
