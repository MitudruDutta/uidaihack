"""
UIDAI Hackathon - District Name Standardizer
Based on official district names as of 2024-2025
"""

DISTRICT_MAPPING = {
    # Andaman & Nicobar
    'Andamans': 'Andaman Islands',
    'Nicobars': 'Nicobar Islands',
    'North And Middle Andaman': 'North and Middle Andaman',
    
    # Andhra Pradesh / Telangana
    'Anantapur': 'Anantapuramu',
    'Ananthapur': 'Anantapuramu',
    'Ananthapuramu': 'Anantapuramu',
    'chittoor': 'Chittoor',
    'Cuddapah': 'YSR',
    'Y. S. R': 'YSR',
    'N. T. R': 'NTR',
    'Nellore': 'Sri Potti Sriramulu Nellore',
    'Spsr Nellore': 'Sri Potti Sriramulu Nellore',
    'Visakhapatanam': 'Visakhapatnam',
    'Mahabub Nagar': 'Mahabubnagar',
    'Mahbubnagar': 'Mahabubnagar',
    'Rangareddi': 'Rangareddy',
    'rangareddi': 'Rangareddy',
    'K.V.Rangareddy': 'Rangareddy',
    'K.v. Rangareddy': 'Rangareddy',
    'Ranga Reddy': 'Rangareddy',
    'Jagitial': 'Jagtial',
    'Jangoan': 'Jangaon',
    'Komaram Bheem': 'Kumuram Bheem Asifabad',
    'Medchal-malkajgiri': 'Medchal-Malkajgiri',
    'Medchal Malkajgiri': 'Medchal-Malkajgiri',
    'Medchal?malkajgiri': 'Medchal-Malkajgiri',
    'Medchal\u2212malkajgiri': 'Medchal-Malkajgiri',
    'Medchal\u00e2\u0088\u0092malkajgiri': 'Medchal-Malkajgiri',
    'Warangal Urban': 'Hanumakonda',
    'Warangal (urban)': 'Hanumakonda',
    'Warangal Rural': 'Warangal',
    'Yadadri.': 'Yadadri Bhuvanagiri',
    
    # Assam
    'Kamrup Metro': 'Kamrup Metropolitan',
    'Marigaon': 'Morigaon',
    'North Cachar Hills': 'Dima Hasao',
    'Sibsagar': 'Sivasagar',
    'South Salmara Mankachar': 'South Salmara-Mankachar',
    'Tamulpur District': 'Tamulpur',
    
    # Arunachal Pradesh
    'Shi-yomi': 'Shi Yomi',
    
    # Bihar
    'Aurangabad(BH)': 'Aurangabad',
    'Aurangabad(bh)': 'Aurangabad',
    'Kaimur (Bhabua)': 'Kaimur',
    'Kaimur- Bhabua': 'Kaimur',
    'Bhabua': 'Kaimur',
    'Monghyr': 'Munger',
    'Purnea': 'Purnia',
    'Purbi Champaran': 'East Champaran',
    'Purba Champaran': 'East Champaran',
    'Pashchim Champaran': 'West Champaran',
    'Sheikpura': 'Sheikhpura',
    'Samstipur': 'Samastipur',
    
    # Chhattisgarh
    'Dakshin Bastar Dantewada': 'Dantewada',
    'Uttar Bastar Kanker': 'Kanker',
    'Kabeerdham': 'Kabirdham',
    'Kawardha': 'Kabirdham',
    'Janjgir - Champa': 'Janjgir-Champa',
    'Janjgir Champa': 'Janjgir-Champa',
    'Janjgir-champa': 'Janjgir-Champa',
    'Gaurela-pendra-marwahi': 'Gaurela-Pendra-Marwahi',
    'Gaurella Pendra Marwahi': 'Gaurela-Pendra-Marwahi',
    'ManendragarhChirmiriBharatpur': 'Manendragarh-Chirmiri-Bharatpur',
    'Manendragarh\u2013Chirmiri\u2013Bharatpur': 'Manendragarh-Chirmiri-Bharatpur',
    'Mohalla-Manpur-Ambagarh Chowki': 'Mohla-Manpur-Ambagarh Chowki',
    'Mohla-Manpur-Ambagarh Chouki': 'Mohla-Manpur-Ambagarh Chowki',
    'Khairagarh Chhuikhadan Gandai': 'Khairagarh-Chhuikhadan-Gandai',
    'Gariyaband': 'Gariaband',
    'Bijapur(CGH)': 'Bijapur',
    
    # Dadra and Nagar Haveli
    'Dadra & Nagar Haveli': 'Dadra and Nagar Haveli',
    
    # Delhi
    'North East': 'North East Delhi',
    'North East *': 'North East Delhi',
    'North East   *': 'North East Delhi',
    'Najafgarh': 'South West Delhi',
    
    # Gujarat
    'Banas Kantha': 'Banaskantha',
    'Sabar Kantha': 'Sabarkantha',
    'Kachchh': 'Kutch',
    'Surendra Nagar': 'Surendranagar',
    'Mahesana': 'Mehsana',
    'Panch Mahals': 'Panchmahal',
    'Panchmahals': 'Panchmahal',
    'Chhotaudepur': 'Chhota Udepur',
    'The Dangs': 'Dang',
    'Dohad': 'Dahod',
    'Arvalli': 'Aravalli',
    
    # Haryana
    'Gurgaon': 'Gurugram',
    'Mewat': 'Nuh',
    'Yamuna Nagar': 'Yamunanagar',
    
    # Himachal Pradesh
    'Lahul & Spiti': 'Lahaul and Spiti',
    'Lahul and Spiti': 'Lahaul and Spiti',
    
    # Jammu & Kashmir / Ladakh
    'Baramula': 'Baramulla',
    'Badgam': 'Budgam',
    'Bandipore': 'Bandipora',
    'Bandipur': 'Bandipora',
    'Shupiyan': 'Shopian',
    'Punch': 'Poonch',
    'punch': 'Poonch',
    'Leh (ladakh)': 'Leh',
    'udhampur': 'Udhampur',
    'Rajauri': 'Rajouri',
    
    # Jharkhand
    'Hazaribag': 'Hazaribagh',
    'Kodarma': 'Koderma',
    'Palamau': 'Palamu',
    'Pakaur': 'Pakur',
    'Sahebganj': 'Sahibganj',
    'Seraikela-kharsawan': 'Seraikela Kharsawan',
    'Seraikela-Kharsawan': 'Seraikela Kharsawan',
    'East Singhbum': 'East Singhbhum',
    'Purbi Singhbhum': 'East Singhbhum',
    'Pashchimi Singhbhum': 'West Singhbhum',
    
    # Karnataka
    'Bangalore': 'Bengaluru Urban',
    'Bengaluru': 'Bengaluru Urban',
    'Bengaluru South': 'Bengaluru Urban',
    'Bangalore Rural': 'Bengaluru Rural',
    'Belgaum': 'Belagavi',
    'Bellary': 'Ballari',
    'Gulbarga': 'Kalaburagi',
    'Mysore': 'Mysuru',
    'Shimoga': 'Shivamogga',
    'Tumkur': 'Tumakuru',
    'Bijapur(KAR)': 'Vijayapura',
    'Hasan': 'Hassan',
    'Chickmagalur': 'Chikkamagaluru',
    'Chikmagalur': 'Chikkamagaluru',
    'Davangere': 'Davanagere',
    'Chamrajanagar': 'Chamarajanagar',
    'Chamrajnagar': 'Chamarajanagar',
    'Ramanagar': 'Ramanagara',
    'yadgir': 'Yadgir',
    
    # Kerala
    'Kasargod': 'Kasaragod',
    
    # Madhya Pradesh
    'Ashok Nagar': 'Ashoknagar',
    'Hoshangabad': 'Narmadapuram',
    'Narsimhapur': 'Narsinghpur',
    'East Nimar': 'Khandwa',
    'West Nimar': 'Khargone',
    
    # Maharashtra
    'Ahmadnagar': 'Ahilyanagar',
    'Ahmednagar': 'Ahilyanagar',
    'Ahmed Nagar': 'Ahilyanagar',
    'Chatrapati Sambhaji Nagar': 'Chhatrapati Sambhajinagar',
    'Osmanabad': 'Dharashiv',
    'Bid': 'Beed',
    'Buldana': 'Buldhana',
    'Gondiya': 'Gondia',
    'Raigarh(MH)': 'Raigad',
    'Mumbai': 'Mumbai City',
    'Mumbai( Sub Urban )': 'Mumbai Suburban',
    
    # Mizoram
    'Mammit': 'Mamit',
    'Saiha': 'Siaha',
    
    # Nagaland
    'Chumukedima': 'Chumoukedima',
    
    # Odisha
    'Anugal': 'Angul',
    'Anugul': 'Angul',
    'ANGUL': 'Angul',
    'Baleshwar': 'Balasore',
    'Baleswar': 'Balasore',
    'BALANGIR': 'Balangir',
    'Boudh': 'Baudh',
    'Debagarh': 'Deogarh',
    'Jagatsinghapur': 'Jagatsinghpur',
    'Jajapur': 'Jajpur',
    'jajpur': 'Jajpur',
    'JAJPUR': 'Jajpur',
    'Khorda': 'Khordha',
    'Nabarangapur': 'Nabarangpur',
    'NAYAGARH': 'Nayagarh',
    'NUAPADA': 'Nuapada',
    'Sundergarh': 'Sundargarh',
    'Sonapur': 'Subarnapur',
    
    # Puducherry
    'Pondicherry': 'Puducherry',
    
    # Punjab
    'Firozpur': 'Ferozepur',
    'Nawanshahr': 'Shahid Bhagat Singh Nagar',
    'Shaheed Bhagat Singh Nagar': 'Shahid Bhagat Singh Nagar',
    'Mohali': 'Sahibzada Ajit Singh Nagar',
    'S.A.S Nagar': 'Sahibzada Ajit Singh Nagar',
    'S.A.S Nagar(Mohali)': 'Sahibzada Ajit Singh Nagar',
    'SAS Nagar (Mohali)': 'Sahibzada Ajit Singh Nagar',
    'Muktsar': 'Sri Muktsar Sahib',
    
    # Rajasthan
    'Chittaurgarh': 'Chittorgarh',
    'Dhaulpur': 'Dholpur',
    'Ganganagar': 'Sri Ganganagar',
    'Jalor': 'Jalore',
    'Jhunjhunun': 'Jhunjhunu',
    'Deeg\xa0': 'Deeg',
    
    # Sikkim
    'East': 'Gangtok',
    'East Sikkim': 'Gangtok',
    'West': 'Gyalshing',
    'West Sikkim': 'Gyalshing',
    'North': 'Mangan',
    'North Sikkim': 'Mangan',
    'South': 'Namchi',
    'South Sikkim': 'Namchi',
    
    # Tamil Nadu
    'Kancheepuram': 'Kanchipuram',
    'Kanyakumari': 'Kanniyakumari',
    'The Nilgiris': 'The Nilgiris',
    'Nilgiris': 'The Nilgiris',
    'Thiruvallur': 'Thiruvallur',
    'Tiruvallur': 'Thiruvallur',
    'Thiruvarur': 'Thiruvarur',
    'Tiruvarur': 'Thiruvarur',
    'Tirupattur': 'Tirupathur',
    'Tuticorin': 'Thoothukudi',
    'Thoothukkudi': 'Thoothukudi',
    'Villupuram': 'Viluppuram',
    
    # Uttar Pradesh
    'Allahabad': 'Prayagraj',
    'Faizabad': 'Ayodhya',
    'Jyotiba Phule Nagar': 'Amroha',
    'Jyotiba Phule Nagar *': 'Amroha',
    'Sant Ravidas Nagar': 'Bhadohi',
    'Sant Ravidas Nagar Bhadohi': 'Bhadohi',
    'Rae Bareli': 'Raebareli',
    'Bara Banki': 'Barabanki',
    'Bulandshahar': 'Bulandshahr',
    'Bagpat': 'Baghpat',
    'Kushi Nagar': 'Kushinagar',
    'Kheri': 'Lakhimpur Kheri',
    'Lakhimpur': 'Lakhimpur Kheri',
    'Mahrajganj': 'Maharajganj',
    'Shrawasti': 'Shravasti',
    'Siddharth Nagar': 'Siddharthnagar',
    
    # Uttarakhand
    'Hardwar': 'Haridwar',
    'Garhwal': 'Pauri Garhwal',
    
    # West Bengal
    'Coochbehar': 'Cooch Behar',
    'Koch Bihar': 'Cooch Behar',
    'Darjiling': 'Darjeeling',
    'Hooghiy': 'Hooghly',
    'Hugli': 'Hooghly',
    'hooghly': 'Hooghly',
    'HOOGHLY': 'Hooghly',
    'Haora': 'Howrah',
    'Hawrah': 'Howrah',
    'HOWRAH': 'Howrah',
    'KOLKATA': 'Kolkata',
    'Maldah': 'Malda',
    'MALDA': 'Malda',
    'NADIA': 'Nadia',
    'nadia': 'Nadia',
    'Puruliya': 'Purulia',
    'Barddhaman': 'Paschim Bardhaman',
    'Bardhaman': 'Paschim Bardhaman',
    'Burdwan': 'Paschim Bardhaman',
    'East Midnapore': 'Purba Medinipur',
    'East Midnapur': 'Purba Medinipur',
    'east midnapore': 'Purba Medinipur',
    'East midnapore': 'Purba Medinipur',
    'Medinipur': 'Paschim Medinipur',
    'Medinipur West': 'Paschim Medinipur',
    'West Midnapore': 'Paschim Medinipur',
    'West Medinipur': 'Paschim Medinipur',
    'South Dinajpur': 'Dakshin Dinajpur',
    'Dinajpur Dakshin': 'Dakshin Dinajpur',
    'North Dinajpur': 'Uttar Dinajpur',
    'Dinajpur Uttar': 'Uttar Dinajpur',
    'North Twenty Four Parganas': 'North 24 Parganas',
    '24 Paraganas North': 'North 24 Parganas',
    'South 24 Pargana': 'South 24 Parganas',
    'South 24 parganas': 'South 24 Parganas',
    'South 24 pargana': 'South 24 Parganas',
    '24 Paraganas South': 'South 24 Parganas',
    'South Twenty Four Parganas': 'South 24 Parganas',
    'South  Twenty Four Parganas': 'South 24 Parganas',
}

# Junk entries to discard
JUNK_ENTRIES = {
    'IDPL COLONY', 'Near University Thana', 'NEAR SHOBHA', 'Greater Kailash 2',
    'Near meera hospital', 'Behind Zudio', 'Near Dhyana Ashram',
    'Near Uday nagar NIT garden', 'Naihati Anandabazar', 'Domjur',
    'Bally Jagachha', 'STATE BANK OF INDIA', '\\\\', '\\', 'Balianta',
    'Amta - II', 'Dakshin Gangotri', 'Kadiri Road', 'South DumDum(M)',
    'Dist : Thane', 'Sonapur',
}


def clean_asterisk(name):
    """Remove asterisks and extra spaces"""
    if '*' in name:
        name = name.replace(' *', '').replace('*', '').strip()
    name = ' '.join(name.split())
    return name


def standardize_district(name):
    """Standardize a single district name"""
    if name is None or not isinstance(name, str):
        return None
    
    # Clean whitespace and special chars
    name = str(name).strip()
    name = name.replace('\xa0', ' ').strip()
    name = clean_asterisk(name)
    
    # Check if junk
    if name in JUNK_ENTRIES:
        return None
    
    # Apply mapping
    if name in DISTRICT_MAPPING:
        return DISTRICT_MAPPING[name]
    
    return name


def standardize_dataframe(df):
    """Standardize district names in dataframe"""
    df = df.copy()
    original_districts = df['district'].copy()
    
    df['district'] = df['district'].apply(standardize_district)
    
    # Remove junk rows
    junk_mask = df['district'].isnull()
    junk_count = junk_mask.sum()
    df = df[~junk_mask].copy()
    
    # Count standardized
    if len(df) > 0:
        changed = (original_districts.loc[df.index] != df['district']).sum()
    else:
        changed = 0
    
    return df, changed, junk_count


def run_standardization():
    """Run on all datasets"""
    import pandas as pd
    import os
    
    os.chdir('/home/btwitsvoid/Documents/ML Project/uidaihack')
    os.makedirs('data/clean', exist_ok=True)
    
    datasets = [
        ('enrolment', 'data/enrolment.csv'),
        ('biometric', 'data/biometric.csv'),
        ('demographic', 'data/demographic.csv'),
    ]
    
    print("=" * 70)
    print("DISTRICT STANDARDIZATION")
    print("=" * 70)
    
    for name, path in datasets:
        print(f"\n{name.upper()}:")
        df = pd.read_csv(path)
        orig_len = len(df)
        orig_districts = df['district'].nunique()
        
        df, changed, junk = standardize_dataframe(df)
        
        print(f"  Rows: {orig_len:,} -> {len(df):,} (removed {junk:,} junk)")
        print(f"  Districts standardized: {changed:,}")
        print(f"  Unique districts: {orig_districts} -> {df['district'].nunique()}")
        
        df.to_csv(f'data/clean/{name}_std.csv', index=False)
        print(f"  Saved: data/clean/{name}_std.csv")
    
    # Cross-check
    print("\n" + "=" * 70)
    print("CROSS-DATASET VERIFICATION")
    print("=" * 70)
    
    all_districts = set()
    for name, _ in datasets:
        df = pd.read_csv(f'data/clean/{name}_std.csv')
        all_districts.update(df['district'].unique())
    
    print(f"\nTotal unique districts across all datasets: {len(all_districts)}")
    
    # List remaining non-standard looking names
    print("\nDistricts to review (potential issues):")
    for d in sorted(all_districts):
        if d != d.strip() or d.lower() != d.title().lower().replace("'S", "'s"):
            if d.isupper() or d.islower():
                print(f"  Case issue: {d}")


if __name__ == '__main__':
    run_standardization()
