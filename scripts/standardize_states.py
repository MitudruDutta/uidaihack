import pandas as pd
import os

# Known mappings - states/UTs with variant spellings
STATE_MAP = {
    # West Bengal variants
    "WEST BENGAL": "West Bengal",
    "WESTBENGAL": "West Bengal",
    "West Bangal": "West Bengal",
    "West Bengli": "West Bengal",
    "West bengal": "West Bengal",
    "Westbengal": "West Bengal",
    "west Bengal": "West Bengal",
    
    # Odisha variants
    "ODISHA": "Odisha",
    "Orissa": "Odisha",
    "odisha": "Odisha",
    
    # Andhra Pradesh variants
    "andhra pradesh": "Andhra Pradesh",
    
    # Chhattisgarh variants
    "Chhatisgarh": "Chhattisgarh",
    
    # Uttarakhand variants
    "Uttaranchal": "Uttarakhand",
    
    # Tamil Nadu variants
    "Tamilnadu": "Tamil Nadu",
    
    # Puducherry variants
    "Pondicherry": "Puducherry",
    
    # Jammu and Kashmir variants
    "Jammu & Kashmir": "Jammu and Kashmir",
    
    # Andaman and Nicobar Islands variants
    "Andaman & Nicobar Islands": "Andaman and Nicobar Islands",
    
    # Dadra and Nagar Haveli and Daman and Diu (merged UT since 2020)
    "Dadra & Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "Dadra and Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "Daman & Diu": "Dadra and Nagar Haveli and Daman and Diu",
    "Daman and Diu": "Dadra and Nagar Haveli and Daman and Diu",
    
    # Cities/Districts -> Their actual states
    # These are garbage entries - cities mistakenly entered as states
    "BALANAGAR": "Telangana",           # Balanagar is in Hyderabad, Telangana
    "Darbhanga": "Bihar",               # Darbhanga is a district in Bihar
    "GURGAON": "Haryana",               # Gurgaon/Gurugram is in Haryana
    "Greater Kailash 2": "Delhi",       # GK2 is in Delhi
    "Jaipur": "Rajasthan",              # Jaipur is capital of Rajasthan
    "Madanapalle": "Andhra Pradesh",    # Madanapalle is in Annamayya district, AP
    "Nagpur": "Maharashtra",            # Nagpur is in Maharashtra
    "PUTHUR": "Tamil Nadu",             # Puthur is in Tamil Nadu
    "Pune City": "Maharashtra",         # Pune is in Maharashtra
    "Puttenahalli": "Karnataka",        # Puttenahalli is in Bangalore, Karnataka
    "Raja Annamalai Puram": "Tamil Nadu", # RA Puram is in Chennai, Tamil Nadu
    
    # Garbage/Invalid
    "100000": "UNKNOWN",                # Looks like a pincode, will drop later
}

os.chdir("/home/btwitsvoid/Documents/ML Project/uidaihack")

for name in ["enrolment", "biometric", "demographic"]:
    df = pd.read_csv(f"data/{name}.csv")
    
    before_states = df['state'].nunique()
    before_unknown = len(df[df['state'].isin(['100000'])])
    
    # Apply mapping
    df['state'] = df['state'].replace(STATE_MAP)
    
    # Remove UNKNOWN entries
    unknown_count = len(df[df['state'] == 'UNKNOWN'])
    df = df[df['state'] != 'UNKNOWN']
    
    after_states = df['state'].nunique()
    
    df.to_csv(f"data/{name}.csv", index=False)
    print(f"{name}: {before_states} -> {after_states} states, removed {unknown_count} invalid rows")

print("\n✓ State names standardized")

# Verify final state list
print("\nFINAL STATES:")
df = pd.read_csv("data/enrolment.csv")
for s in sorted(df['state'].unique()):
    print(f"  {s}")
