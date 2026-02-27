"""
Disaster Data Preprocessing Pipeline
=====================================
Comprehensive preprocessing for disaster events dataset with automatic handling
Includes: GLIDE parsing, intelligent imputation, feature engineering, and validation

Author: Graduation Project 2026
Date: February 26, 2026
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler

# ============================================================================
# PART 1: MAPPING DICTIONARIES (Research-based - Update with your findings)
# ============================================================================

# GLIDE Type Code to Disaster Type Mapping
GLIDE_TYPE_TO_DISASTER = {
    'FL': 'Flood',
    'FF': 'Flash Flood',
    'EQ': 'Earthquake',
    'DR': 'Drought',
    'TC': 'Tropical Cyclone',
    'ST': 'Storm',
    'EP': 'Epidemic',
    'TS': 'Tsunami',
    'VO': 'Volcanic Activity',
    'WF': 'Wildfire',
    'LS': 'Landslide',
    'AV': 'Avalanche',
    'CW': 'Cold Wave',
    'HT': 'Heat Wave',
    'ET': 'Extreme Temperature',
    'IN': 'Insect Infestation',
    'AC': 'Accident',
    'FR': 'Fire',
    'TO': 'Tornado',
    'SS': 'Storm Surge',
}

# Reverse mapping: Disaster Type to GLIDE Code
DISASTER_TO_GLIDE_TYPE = {v: k for k, v in GLIDE_TYPE_TO_DISASTER.items()}

# ISO Country Codes to Country Names (Add more as needed)
ISO_TO_COUNTRY = {
    'AFG': 'Afghanistan', 'ALB': 'Albania', 'DZA': 'Algeria', 'AGO': 'Angola',
    'ARG': 'Argentina', 'ARM': 'Armenia', 'AUS': 'Australia', 'AUT': 'Austria',
    'BGD': 'Bangladesh', 'BLR': 'Belarus', 'BEL': 'Belgium', 'BEN': 'Benin',
    'BOL': 'Bolivia', 'BIH': 'Bosnia and Herzegovina', 'BRA': 'Brazil', 'BGR': 'Bulgaria',
    'BFA': 'Burkina Faso', 'BDI': 'Burundi', 'KHM': 'Cambodia', 'CMR': 'Cameroon',
    'CAN': 'Canada', 'CAF': 'Central African Republic', 'TCD': 'Chad', 'CHL': 'Chile',
    'CHN': 'China', 'COL': 'Colombia', 'COD': 'Democratic Republic of the Congo',
    'COG': 'Congo', 'CRI': 'Costa Rica', 'HRV': 'Croatia', 'CUB': 'Cuba',
    'CZE': 'Czech Republic', 'DNK': 'Denmark', 'DJI': 'Djibouti', 'DOM': 'Dominican Republic',
    'ECU': 'Ecuador', 'EGY': 'Egypt', 'SLV': 'El Salvador', 'ERI': 'Eritrea',
    'EST': 'Estonia', 'ETH': 'Ethiopia', 'FIN': 'Finland', 'FRA': 'France',
    'GAB': 'Gabon', 'GMB': 'Gambia', 'GEO': 'Georgia', 'DEU': 'Germany',
    'GHA': 'Ghana', 'GRC': 'Greece', 'GTM': 'Guatemala', 'GIN': 'Guinea',
    'HTI': 'Haiti', 'HND': 'Honduras', 'HUN': 'Hungary', 'ISL': 'Iceland',
    'IND': 'India', 'IDN': 'Indonesia', 'IRN': 'Iran', 'IRQ': 'Iraq',
    'IRL': 'Ireland', 'ISR': 'Israel', 'ITA': 'Italy', 'JAM': 'Jamaica',
    'JPN': 'Japan', 'JOR': 'Jordan', 'KAZ': 'Kazakhstan', 'KEN': 'Kenya',
    'KOR': 'South Korea', 'PRK': 'North Korea', 'KWT': 'Kuwait', 'KGZ': 'Kyrgyzstan',
    'LAO': 'Laos', 'LVA': 'Latvia', 'LBN': 'Lebanon', 'LSO': 'Lesotho',
    'LBR': 'Liberia', 'LBY': 'Libya', 'LTU': 'Lithuania', 'MDG': 'Madagascar',
    'MWI': 'Malawi', 'MYS': 'Malaysia', 'MLI': 'Mali', 'MRT': 'Mauritania',
    'MEX': 'Mexico', 'MNG': 'Mongolia', 'MAR': 'Morocco', 'MOZ': 'Mozambique',
    'MMR': 'Myanmar', 'NAM': 'Namibia', 'NPL': 'Nepal', 'NLD': 'Netherlands',
    'NZL': 'New Zealand', 'NIC': 'Nicaragua', 'NER': 'Niger', 'NGA': 'Nigeria',
    'NOR': 'Norway', 'PAK': 'Pakistan', 'PAN': 'Panama', 'PNG': 'Papua New Guinea',
    'PRY': 'Paraguay', 'PER': 'Peru', 'PHL': 'Philippines', 'POL': 'Poland',
    'PRT': 'Portugal', 'ROU': 'Romania', 'RUS': 'Russia', 'RWA': 'Rwanda',
    'SAU': 'Saudi Arabia', 'SEN': 'Senegal', 'SRB': 'Serbia', 'SLE': 'Sierra Leone',
    'SGP': 'Singapore', 'SVK': 'Slovakia', 'SVN': 'Slovenia', 'SOM': 'Somalia',
    'ZAF': 'South Africa', 'SSD': 'South Sudan', 'ESP': 'Spain', 'LKA': 'Sri Lanka',
    'SDN': 'Sudan', 'SWZ': 'Eswatini', 'SWE': 'Sweden', 'CHE': 'Switzerland',
    'SYR': 'Syria', 'TWN': 'Taiwan', 'TJK': 'Tajikistan', 'TZA': 'Tanzania',
    'THA': 'Thailand', 'TGO': 'Togo', 'TTO': 'Trinidad and Tobago', 'TUN': 'Tunisia',
    'TUR': 'Turkey', 'TKM': 'Turkmenistan', 'UGA': 'Uganda', 'UKR': 'Ukraine',
    'ARE': 'United Arab Emirates', 'GBR': 'United Kingdom', 'USA': 'United States',
    'URY': 'Uruguay', 'UZB': 'Uzbekistan', 'VEN': 'Venezuela', 'VNM': 'Vietnam',
    'YEM': 'Yemen', 'ZMB': 'Zambia', 'ZWE': 'Zimbabwe',
}

# Reverse mapping: Country to ISO
COUNTRY_TO_ISO = {v: k for k, v in ISO_TO_COUNTRY.items()}

# Country to Continent Mapping
COUNTRY_TO_CONTINENT = {
    # Africa
    'Algeria': 'Africa', 'Angola': 'Africa', 'Benin': 'Africa', 'Botswana': 'Africa',
    'Burkina Faso': 'Africa', 'Burundi': 'Africa', 'Cameroon': 'Africa', 'Cape Verde': 'Africa',
    'Central African Republic': 'Africa', 'Chad': 'Africa', 'Comoros': 'Africa', 'Congo': 'Africa',
    'Democratic Republic of the Congo': 'Africa', 'Djibouti': 'Africa', 'Egypt': 'Africa',
    'Equatorial Guinea': 'Africa', 'Eritrea': 'Africa', 'Eswatini': 'Africa', 'Ethiopia': 'Africa',
    'Gabon': 'Africa', 'Gambia': 'Africa', 'Ghana': 'Africa', 'Guinea': 'Africa',
    'Guinea-Bissau': 'Africa', 'Kenya': 'Africa', 'Lesotho': 'Africa', 'Liberia': 'Africa',
    'Libya': 'Africa', 'Madagascar': 'Africa', 'Malawi': 'Africa', 'Mali': 'Africa',
    'Mauritania': 'Africa', 'Mauritius': 'Africa', 'Morocco': 'Africa', 'Mozambique': 'Africa',
    'Namibia': 'Africa', 'Niger': 'Africa', 'Nigeria': 'Africa', 'Rwanda': 'Africa',
    'Senegal': 'Africa', 'Seychelles': 'Africa', 'Sierra Leone': 'Africa', 'Somalia': 'Africa',
    'South Africa': 'Africa', 'South Sudan': 'Africa', 'Sudan': 'Africa', 'Tanzania': 'Africa',
    'Togo': 'Africa', 'Tunisia': 'Africa', 'Uganda': 'Africa', 'Zambia': 'Africa', 'Zimbabwe': 'Africa',
    
    # Asia
    'Afghanistan': 'Asia', 'Armenia': 'Asia', 'Azerbaijan': 'Asia', 'Bangladesh': 'Asia',
    'Bhutan': 'Asia', 'Brunei': 'Asia', 'Cambodia': 'Asia', 'China': 'Asia',
    'Georgia': 'Asia', 'India': 'Asia', 'Indonesia': 'Asia', 'Iran': 'Asia',
    'Iraq': 'Asia', 'Israel': 'Asia', 'Japan': 'Asia', 'Jordan': 'Asia',
    'Kazakhstan': 'Asia', 'Kuwait': 'Asia', 'Kyrgyzstan': 'Asia', 'Laos': 'Asia',
    'Lebanon': 'Asia', 'Malaysia': 'Asia', 'Maldives': 'Asia', 'Mongolia': 'Asia',
    'Myanmar': 'Asia', 'Nepal': 'Asia', 'North Korea': 'Asia', 'Oman': 'Asia',
    'Pakistan': 'Asia', 'Palestine': 'Asia', 'Philippines': 'Asia', 'Qatar': 'Asia',
    'Saudi Arabia': 'Asia', 'Singapore': 'Asia', 'South Korea': 'Asia', 'Sri Lanka': 'Asia',
    'Syria': 'Asia', 'Taiwan': 'Asia', 'Tajikistan': 'Asia', 'Thailand': 'Asia',
    'Timor-Leste': 'Asia', 'Turkey': 'Asia', 'Turkmenistan': 'Asia', 'United Arab Emirates': 'Asia',
    'Uzbekistan': 'Asia', 'Vietnam': 'Asia', 'Yemen': 'Asia',
    
    # Europe
    'Albania': 'Europe', 'Austria': 'Europe', 'Belarus': 'Europe', 'Belgium': 'Europe',
    'Bosnia and Herzegovina': 'Europe', 'Bulgaria': 'Europe', 'Croatia': 'Europe', 'Czech Republic': 'Europe',
    'Denmark': 'Europe', 'Estonia': 'Europe', 'Finland': 'Europe', 'France': 'Europe',
    'Germany': 'Europe', 'Greece': 'Europe', 'Hungary': 'Europe', 'Iceland': 'Europe',
    'Ireland': 'Europe', 'Italy': 'Europe', 'Latvia': 'Europe', 'Lithuania': 'Europe',
    'Luxembourg': 'Europe', 'Macedonia': 'Europe', 'Moldova': 'Europe', 'Montenegro': 'Europe',
    'Netherlands': 'Europe', 'Norway': 'Europe', 'Poland': 'Europe', 'Portugal': 'Europe',
    'Romania': 'Europe', 'Russia': 'Europe', 'Serbia': 'Europe', 'Slovakia': 'Europe',
    'Slovenia': 'Europe', 'Spain': 'Europe', 'Sweden': 'Europe', 'Switzerland': 'Europe',
    'Ukraine': 'Europe', 'United Kingdom': 'Europe',
    
    # Americas
    'Argentina': 'Americas', 'Bahamas': 'Americas', 'Barbados': 'Americas', 'Belize': 'Americas',
    'Bolivia': 'Americas', 'Brazil': 'Americas', 'Canada': 'Americas', 'Chile': 'Americas',
    'Colombia': 'Americas', 'Costa Rica': 'Americas', 'Cuba': 'Americas', 'Dominica': 'Americas',
    'Dominican Republic': 'Americas', 'Ecuador': 'Americas', 'El Salvador': 'Americas', 'Guatemala': 'Americas',
    'Guyana': 'Americas', 'Haiti': 'Americas', 'Honduras': 'Americas', 'Jamaica': 'Americas',
    'Mexico': 'Americas', 'Nicaragua': 'Americas', 'Panama': 'Americas', 'Paraguay': 'Americas',
    'Peru': 'Americas', 'Saint Lucia': 'Americas', 'Suriname': 'Americas', 'Trinidad and Tobago': 'Americas',
    'United States': 'Americas', 'Uruguay': 'Americas', 'Venezuela': 'Americas',
    
    # Oceania
    'Australia': 'Oceania', 'Fiji': 'Oceania', 'New Zealand': 'Oceania', 'Papua New Guinea': 'Oceania',
    'Samoa': 'Oceania', 'Solomon Islands': 'Oceania', 'Tonga': 'Oceania', 'Vanuatu': 'Oceania',
}

# Country to Region Mapping (Sub-continental)
COUNTRY_TO_REGION = {
    # Eastern Africa
    'Burundi': 'Eastern Africa', 'Comoros': 'Eastern Africa', 'Djibouti': 'Eastern Africa',
    'Eritrea': 'Eastern Africa', 'Ethiopia': 'Eastern Africa', 'Kenya': 'Eastern Africa',
    'Madagascar': 'Eastern Africa', 'Malawi': 'Eastern Africa', 'Mauritius': 'Eastern Africa',
    'Mozambique': 'Eastern Africa', 'Rwanda': 'Eastern Africa', 'Somalia': 'Eastern Africa',
    'South Sudan': 'Eastern Africa', 'Tanzania': 'Eastern Africa', 'Uganda': 'Eastern Africa',
    'Zambia': 'Eastern Africa', 'Zimbabwe': 'Eastern Africa',
    
    # Western Africa
    'Benin': 'Western Africa', 'Burkina Faso': 'Western Africa', 'Cape Verde': 'Western Africa',
    'Gambia': 'Western Africa', 'Ghana': 'Western Africa', 'Guinea': 'Western Africa',
    'Guinea-Bissau': 'Western Africa', 'Liberia': 'Western Africa', 'Mali': 'Western Africa',
    'Mauritania': 'Western Africa', 'Niger': 'Western Africa', 'Nigeria': 'Western Africa',
    'Senegal': 'Western Africa', 'Sierra Leone': 'Western Africa', 'Togo': 'Western Africa',
    
    # Southern Asia
    'Afghanistan': 'Southern Asia', 'Bangladesh': 'Southern Asia', 'Bhutan': 'Southern Asia',
    'India': 'Southern Asia', 'Iran': 'Southern Asia', 'Maldives': 'Southern Asia',
    'Nepal': 'Southern Asia', 'Pakistan': 'Southern Asia', 'Sri Lanka': 'Southern Asia',
    
    # South-Eastern Asia
    'Brunei': 'South-Eastern Asia', 'Cambodia': 'South-Eastern Asia', 'Indonesia': 'South-Eastern Asia',
    'Laos': 'South-Eastern Asia', 'Malaysia': 'South-Eastern Asia', 'Myanmar': 'South-Eastern Asia',
    'Philippines': 'South-Eastern Asia', 'Singapore': 'South-Eastern Asia', 'Thailand': 'South-Eastern Asia',
    'Timor-Leste': 'South-Eastern Asia', 'Vietnam': 'South-Eastern Asia',
    
    # Eastern Asia
    'China': 'Eastern Asia', 'Japan': 'Eastern Asia', 'Mongolia': 'Eastern Asia',
    'North Korea': 'Eastern Asia', 'South Korea': 'Eastern Asia', 'Taiwan': 'Eastern Asia',
    
    # Add more regions as needed...
}

# Disaster Type to Group Mapping
DISASTER_TO_GROUP = {
    'Flood': 'Hydrological', 'Flash Flood': 'Hydrological', 'Storm Surge': 'Hydrological',
    'Drought': 'Climatological', 'Wildfire': 'Climatological', 'Extreme Temperature': 'Climatological',
    'Cold Wave': 'Climatological', 'Heat Wave': 'Climatological',
    'Earthquake': 'Geophysical', 'Volcanic Activity': 'Geophysical', 'Tsunami': 'Geophysical',
    'Storm': 'Meteorological', 'Tropical Cyclone': 'Meteorological', 'Tornado': 'Meteorological',
    'Epidemic': 'Biological', 'Insect Infestation': 'Biological',
    'Landslide': 'Hydrological', 'Avalanche': 'Hydrological',
}

# TODO: Add your research findings here!
# Expected disaster durations in days (average) - RESEARCH THESE VALUES!
DISASTER_DURATION_DAYS = {
    'Flood': 10,                 # River floods typically last several days to weeks
    'Epidemic': 365,             # Often lasts months to years
    'Drought': 730,              # Can last 1–2 years
    'Storm': 3,                  # Typical storm duration
    'Insect Infestation': 90,    # Can persist for months
    'Earthquake': 1,             # Main shock is short, impact period ~1 day
    'Landslide': 1,              # Sudden event
    'Wildfire': 60,              # Large fires can last weeks to months
    'Volcanic Activity': 180,    # Eruptions can last weeks to months
    'Extreme Temperature': 10,   # Heatwaves/cold waves usually days to weeks
    'Mass movement (dry)': 1,    # Sudden dry landslide/rockfall
    'Animal accident': 1,        # Instant event
    'Default': 1,                # Default for unknown disaster types
}

# TODO: Add country centroids (latitude, longitude) - RESEARCH THESE!
# This is a SAMPLE - you should populate with accurate centroids
COUNTRY_CENTROIDS = {
    'Cabo Verde': ('16.5388 N', '23.0418 W'),
    'Comoros (the)': ('11.8750 S', '43.8722 E'),
    'Burkina Faso': ('12.2383 N', '1.5616 W'),
    'Algeria': ('28.0339 N', '1.6596 E'),
    'Gambia (the)': ('13.4432 N', '15.3101 W'),
    'Guinea-Bissau': ('11.8037 N', '15.1804 W'),
    'Egypt': ('26.8206 N', '30.8025 E'),
    'Ghana': ('7.9465 N', '1.0232 W'),
    'Ethiopia': ('9.1450 N', '40.4897 E'),
    'Botswana': ('22.3285 S', '24.6849 E'),
    'Congo (the)': ('0.2280 S', '15.8277 E'),
    'Benin': ('9.3077 N', '2.3158 E'),
    'Côte d’Ivoire': ('7.5400 N', '5.5471 W'),
    'Cameroon': ('7.3697 N', '12.3547 E'),
    'Central African Republic': ('6.6111 N', '20.9394 E'),
    'Djibouti': ('11.8251 N', '42.5903 E'),
    'Burundi': ('3.3731 S', '29.9189 E'),
    'Uganda': ('1.3733 N', '32.2903 E'),
    'Niger (the)': ('17.6078 N', '8.0817 E'),
    'Morocco': ('31.7917 N', '7.0926 W'),
    'Mali': ('17.5707 N', '3.9962 W'),
    'Mauritania': ('21.0079 N', '10.9408 W'),
    'Senegal': ('14.4974 N', '14.4524 W'),
    'Chad': ('15.4542 N', '18.7322 E'),
    'Sudan (the)': ('12.8628 N', '30.2176 E'),
    'Libya': ('26.3351 N', '17.2283 E'),
    'Réunion': ('21.1151 S', '55.5364 E'),
    'Mozambique': ('18.6657 S', '35.5296 E'),
    'Tunisia': ('33.8869 N', '9.5375 E'),
    'Mauritius': ('20.3484 S', '57.5522 E'),
    'Somalia': ('5.1521 N', '46.1996 E'),
    'Kenya': ('0.0236 S', '37.9062 E'),
    'Tanzania, United Republic of': ('6.3690 S', '34.8888 E'),
    'Togo': ('8.6195 N', '0.8248 E'),
    'Malawi': ('13.2543 S', '34.3015 E'),
    'Lesotho': ('29.6099 S', '28.2336 E'),
    'Madagascar': ('18.7669 S', '46.8691 E'),
    'Nigeria': ('9.0820 N', '8.6753 E'),
    'Rwanda': ('1.9403 S', '29.8739 E'),
    'Sierra Leone': ('8.4606 N', '11.7799 W'),
    'South Africa': ('30.5595 S', '22.9375 E'),
    'Congo (the Democratic Republic of the)': ('4.0383 S', '21.7587 E'),
    'Zimbabwe': ('19.0154 S', '29.1549 E'),
    'Zambia': ('13.1339 S', '27.8493 E'),
    'Guinea': ('9.9456 N', '9.6966 W'),
    'Angola': ('11.2027 S', '17.8739 E'),
    'Gabon': ('0.8037 S', '11.6094 E'),
    'Liberia': ('6.4281 N', '9.4295 W'),
    'Namibia': ('22.9576 S', '18.4904 E'),
    'Swaziland': ('26.5225 S', '31.4659 E'),
    'Sao Tome and Principe': ('0.1864 N', '6.6131 E'),
    'Eritrea': ('15.1794 N', '39.7823 E'),
    'Seychelles': ('4.6796 S', '55.4920 E'),
    'Saint Helena, Ascension and Tristan da Cunha': ('24.1435 S', '10.0307 W'),
    'Equatorial Guinea': ('1.6508 N', '10.2679 E'),
    'South Sudan': ('6.8770 N', '31.3070 E'),
}


# ============================================================================
# PART 2: GLIDE PARSING FUNCTIONS
# ============================================================================

def parse_glide(glide_code: str) -> Dict[str, Optional[str]]:
    """
    Parse GLIDE code into components
    Format: XX-YYYY-NNNNNN-CCC
    
    Returns dict with: type_code, year, sequence, country_code
    """
    if pd.isna(glide_code) or not isinstance(glide_code, str):
        return {'type_code': None, 'year': None, 'sequence': None, 'country_code': None}
    
    # Standard GLIDE pattern: XX-YYYY-NNNNNN-CCC
    pattern = r'^([A-Z]{2})-(\d{4})-(\d+)-([A-Z]{3})$'
    match = re.match(pattern, glide_code.strip())
    
    if match:
        return {
            'type_code': match.group(1),
            'year': int(match.group(2)),
            'sequence': int(match.group(3)),
            'country_code': match.group(4)
        }
    
    # Try partial matches
    # Pattern: XX-YYYY-NNNNNN (missing country)
    pattern2 = r'^([A-Z]{2})-(\d{4})-(\d+)$'
    match2 = re.match(pattern2, glide_code.strip())
    if match2:
        return {
            'type_code': match2.group(1),
            'year': int(match2.group(2)),
            'sequence': int(match2.group(3)),
            'country_code': None
        }
    
    return {'type_code': None, 'year': None, 'sequence': None, 'country_code': None}


def construct_glide(disaster_type: str, year: int, sequence: int, country: str) -> Optional[str]:
    """
    Construct GLIDE code from components
    Used to fill missing GLIDE values
    """
    try:
        # Get type code
        type_code = DISASTER_TO_GLIDE_TYPE.get(disaster_type)
        if not type_code:
            return None
        
        # Get ISO code
        iso_code = COUNTRY_TO_ISO.get(country)
        if not iso_code:
            return None
        
        # Construct GLIDE
        glide = f"{type_code}-{int(year)}-{int(sequence):06d}-{iso_code}"
        return glide
    except:
        return None


# ============================================================================
# PART 3: CORE PREPROCESSING CLASS
# ============================================================================

class DisasterDataPreprocessor:
    """
    Comprehensive disaster data preprocessing pipeline
    Handles: GLIDE parsing, intelligent imputation, validation, feature engineering
    """
    
    def __init__(self):
        self.fitted = False
        
        # Statistics to learn from training data
        self.median_deaths_by_type = {}
        self.median_injured_by_type = {}
        self.median_affected_by_group = {}  # Will use (country, type, decade)
        self.median_damages_by_type = {}
        
        # KNN Imputer for correlated numerical features
        self.knn_imputer = KNNImputer(n_neighbors=5, weights='distance')
        self.impact_scaler = StandardScaler()
        self.knn_fitted = False
        
        # Sequence number tracker for GLIDE construction
        self.sequence_counter = {}
        
    def fit(self, df: pd.DataFrame) -> 'DisasterDataPreprocessor':
        """
        Learn statistics from training data
        Call this ONLY on training set!
        """
        print("=" * 80)
        print("FITTING PREPROCESSOR ON TRAINING DATA")
        print("=" * 80)
        
        # Learn median values for imputation
        self.median_deaths_by_type = df.groupby('Disaster Type')['Total Deaths'].median().to_dict()
        self.median_injured_by_type = df.groupby('Disaster Type')['No Injured'].median().to_dict()
        self.median_damages_by_type = df.groupby('Disaster Type')["Total Damages ('000 US$)"].median().to_dict()
        
        # Learn median affected by (Country, Disaster Type, Decade)
        # This is more granular for better imputation
        df_temp = df.copy()
        df_temp['Decade'] = (df_temp['Year'] // 10) * 10
        grouped = df_temp.groupby(['Country', 'Disaster Type', 'Decade'])['No Affected'].median()
        self.median_affected_by_group = grouped.to_dict()
        
        # Track max sequence numbers per year for GLIDE construction
        glide_parsed = df['Glide'].apply(parse_glide)
        for idx, parsed in glide_parsed.items():
            if parsed['year'] and parsed['sequence']:
                year = parsed['year']
                seq = parsed['sequence']
                if year not in self.sequence_counter:
                    self.sequence_counter[year] = seq
                else:
                    self.sequence_counter[year] = max(self.sequence_counter[year], seq)
        
        # Fit KNN Imputer on impact metrics (correlated features)
        impact_cols = ['Total Deaths', 'No Injured', 'No Affected', 'No Homeless', "Total Damages ('000 US$)"]
        impact_data = df[impact_cols].copy()
        
        # Replace 0s with NaN temporarily to let KNN learn patterns (disasters often have 0 impact)
        # But keep track of original zeros
        try:
            # Fit scaler on non-null values
            mask = impact_data.notna()
            if mask.any().any():
                self.impact_scaler.fit(impact_data[mask.any(axis=1)])
                self.knn_fitted = True
                print("✓ KNN imputer fitted on impact metrics")
            else:
                self.knn_fitted = False
                print("⚠ Warning: Not enough data to fit KNN imputer")
        except Exception as e:
            self.knn_fitted = False
            print(f"⚠ Warning: Could not fit KNN imputer: {e}")
        
        self.fitted = True
        print("✓ Preprocessor fitted successfully!")
        return self
    
    def transform(self, df: pd.DataFrame, is_training: bool = False) -> pd.DataFrame:
        """
        Apply preprocessing transformations
        Works on both training and new data automatically
        
        Parameters:
        -----------
        df : DataFrame to transform
        is_training : If True, allows row dropping. If False (production), keeps all rows
        """
        print("\n" + "=" * 80)
        print(f"PREPROCESSING DATA ({'TRAINING' if is_training else 'PRODUCTION'} MODE)")
        print("=" * 80)
        print(f"Initial shape: {df.shape}")
        
        df = df.copy()
        
        # PHASE 1: Parse GLIDE codes
        print("\n[1/10] Parsing GLIDE codes...")
        df = self._parse_glide_codes(df)
        
        # PHASE 2: Drop critical missing rows (ONLY in training)
        if is_training:
            print("\n[2/10] Dropping rows with missing critical fields...")
            df = self._drop_critical_missing(df)
        else:
            print("\n[2/10] Skipping row drops (production mode)")
        
        # PHASE 3: Use GLIDE to impute features
        print("\n[3/10] Imputing features from GLIDE...")
        df = self._impute_from_glide(df)
        
        # PHASE 4: Use features to impute GLIDE
        print("\n[4/10] Constructing missing GLIDE codes...")
        df = self._construct_missing_glide(df)
        
        # PHASE 5: Impute geographic features
        print("\n[5/10] Imputing geographic features...")
        df = self._impute_geographic(df)
        
        # PHASE 6: Create data quality flags (BEFORE imputation!)
        print("\n[6/10] Creating data quality flags...")
        df = self._create_quality_flags(df)
        
        # PHASE 7: Impute temporal features
        print("\n[7/10] Imputing temporal features...")
        df = self._impute_temporal(df)
        
        # PHASE 7.5: Impute categorical and binary fields
        print("\n[7.5/10] Imputing categorical and binary fields...")
        df = self._impute_categorical_and_binary(df)
        
        # PHASE 8: Impute impact metrics
        print("\n[8/10] Imputing impact metrics...")
        df = self._impute_impact_metrics(df)
        
        # PHASE 9: Feature engineering
        print("\n[9/10] Engineering new features...")
        df = self._engineer_features(df)
        
        # PHASE 10: Final cleaning
        print("\n[10/10] Final data cleaning...")
        df = self._final_cleaning(df)
        
        print("\n" + "=" * 80)
        print(f"PREPROCESSING COMPLETE!")
        print(f"Final shape: {df.shape}")
        print("=" * 80)
        
        return df
    
    def _parse_glide_codes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse all GLIDE codes and extract components"""
        glide_parsed = df['Glide'].apply(parse_glide)
        
        df['GLIDE_Type_Code'] = glide_parsed.apply(lambda x: x['type_code'])
        df['GLIDE_Year'] = glide_parsed.apply(lambda x: x['year'])
        df['GLIDE_Sequence'] = glide_parsed.apply(lambda x: x['sequence'])
        df['GLIDE_Country_ISO'] = glide_parsed.apply(lambda x: x['country_code'])
        
        print(f"  ✓ Parsed {df['GLIDE_Type_Code'].notna().sum()} GLIDE codes")
        return df
    
    def _drop_critical_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop rows missing both Disaster Type AND Country (can't be recovered)"""
        initial_count = len(df)
        
        # Drop if BOTH are missing (can't recover)
        df = df.dropna(subset=['Disaster Type', 'Country'], how='all')
        
        # Drop exact duplicates
        df = df.drop_duplicates()
        
        dropped = initial_count - len(df)
        print(f"  ✓ Dropped {dropped} rows ({dropped/initial_count*100:.2f}%)")
        return df
    
    def _impute_from_glide(self, df: pd.DataFrame) -> pd.DataFrame:
        """Use GLIDE components to fill missing features"""
        
        # 1. Disaster Type from GLIDE
        mask = df['Disaster Type'].isna() & df['GLIDE_Type_Code'].notna()
        df.loc[mask, 'Disaster Type'] = df.loc[mask, 'GLIDE_Type_Code'].map(GLIDE_TYPE_TO_DISASTER)
        filled_type = mask.sum()
        
        # 2. Year from GLIDE
        mask = df['Year'].isna() & df['GLIDE_Year'].notna()
        df.loc[mask, 'Year'] = df.loc[mask, 'GLIDE_Year']
        filled_year = mask.sum()
        
        # 3. Start Year from GLIDE
        mask = df['Start Year'].isna() & df['GLIDE_Year'].notna()
        df.loc[mask, 'Start Year'] = df.loc[mask, 'GLIDE_Year']
        filled_start_year = mask.sum()
        
        # 4. Country from GLIDE ISO code
        mask = df['Country'].isna() & df['GLIDE_Country_ISO'].notna()
        df.loc[mask, 'Country'] = df.loc[mask, 'GLIDE_Country_ISO'].map(ISO_TO_COUNTRY)
        filled_country = mask.sum()
        
        # 5. ISO code directly from GLIDE
        if 'ISO' not in df.columns:
            df['ISO'] = None
        mask = df['ISO'].isna() & df['GLIDE_Country_ISO'].notna()
        df.loc[mask, 'ISO'] = df.loc[mask, 'GLIDE_Country_ISO']
        filled_iso = mask.sum()
        
        print(f"  ✓ Filled from GLIDE: Type={filled_type}, Year={filled_year}, Country={filled_country}")
        return df
    
    def _construct_missing_glide(self, df: pd.DataFrame) -> pd.DataFrame:
        """Construct GLIDE codes for rows that are missing them"""
        
        mask = df['Glide'].isna()
        if mask.sum() == 0:
            print(f"  ✓ No missing GLIDE codes to construct")
            return df
        
        constructed_count = 0
        
        for idx in df[mask].index:
            disaster_type = df.loc[idx, 'Disaster Type']
            year = df.loc[idx, 'Year']
            country = df.loc[idx, 'Country']
            
            if pd.notna(disaster_type) and pd.notna(year) and pd.notna(country):
                # Get or create sequence number
                year_int = int(year)
                if year_int not in self.sequence_counter:
                    self.sequence_counter[year_int] = 1
                else:
                    self.sequence_counter[year_int] += 1
                
                sequence = self.sequence_counter[year_int]
                
                # Construct GLIDE
                glide = construct_glide(disaster_type, year_int, sequence, country)
                if glide:
                    df.loc[idx, 'Glide'] = glide
                    constructed_count += 1
        
        print(f"  ✓ Constructed {constructed_count} GLIDE codes")
        return df
    
    def _impute_geographic(self, df: pd.DataFrame) -> pd.DataFrame:
        """Impute geographic features: Continent, Region, Lat/Lon"""
        
        # 1. Continent from Country
        mask = df['Continent'].isna() & df['Country'].notna()
        df.loc[mask, 'Continent'] = df.loc[mask, 'Country'].map(COUNTRY_TO_CONTINENT)
        filled_continent = mask.sum()
        
        # 2. Region from Country
        if 'Region' not in df.columns:
            df['Region'] = None
        mask = df['Region'].isna() & df['Country'].notna()
        df.loc[mask, 'Region'] = df.loc[mask, 'Country'].map(COUNTRY_TO_REGION)
        filled_region = mask.sum()
        
        # 3. Latitude/Longitude from Country centroids
        # Handle Latitude
        mask = df['Latitude'].isna() & df['Country'].notna()
        for country, coords in COUNTRY_CENTROIDS.items():
            country_mask = mask & (df['Country'] == country)
            df.loc[country_mask, 'Latitude'] = coords[0]
        filled_lat = mask.sum()
        
        # Handle Longitude
        mask = df['Longitude'].isna() & df['Country'].notna()
        for country, coords in COUNTRY_CENTROIDS.items():
            country_mask = mask & (df['Country'] == country)
            df.loc[country_mask, 'Longitude'] = coords[1]
        filled_lon = mask.sum()
        
        print(f"  ✓ Filled geographic: Continent={filled_continent}, Region={filled_region}, Coords={filled_lat}")
        return df
    
    def _create_quality_flags(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create flags BEFORE imputing to track data quality"""
        
        df['Deaths_Known'] = df['Total Deaths'].notna().astype(int)
        df['Injured_Known'] = df['No Injured'].notna().astype(int)
        df['Affected_Known'] = df['No Affected'].notna().astype(int)
        df['Homeless_Known'] = df['No Homeless'].notna().astype(int)
        df['Damages_Known'] = df["Total Damages ('000 US$)"].notna().astype(int)
        df['Location_Precise'] = (df['Latitude'].notna() & df['Longitude'].notna()).astype(int)
        df['Has_Magnitude'] = df['Dis Mag Value'].notna().astype(int)
        df['GLIDE_Complete'] = df['Glide'].notna().astype(int)
        
        print(f"  ✓ Created 8 data quality flags")
        return df
    
    def _impute_temporal(self, df: pd.DataFrame) -> pd.DataFrame:
        """Impute temporal features"""
        
        # 1. Start Month - default to July (mid-year)
        mask = df['Start Month'].isna()
        df.loc[mask, 'Start Month'] = 7
        filled_month = mask.sum()
        
        # 2. Start Day - default to 15 (mid-month)
        mask = df['Start Day'].isna()
        df.loc[mask, 'Start Day'] = 15
        filled_day = mask.sum()
        
        # 3. End Year - use Start Year + disaster duration
        mask = df['End Year'].isna() & df['Start Year'].notna()
        df.loc[mask, 'End Year'] = df.loc[mask, 'Start Year']
        
        # 4. End Month - based on disaster type duration
        mask = df['End Month'].isna() & df['Start Month'].notna() & df['Disaster Type'].notna()
        for idx in df[mask].index:
            disaster_type = df.loc[idx, 'Disaster Type']
            start_month = df.loc[idx, 'Start Month']
            duration = DISASTER_DURATION_DAYS.get(disaster_type, DISASTER_DURATION_DAYS['Default'])
            
            # Simple approximation: add duration as months
            end_month = start_month + (duration // 30)
            if end_month > 12:
                end_month = 12
                df.loc[idx, 'End Year'] = df.loc[idx, 'Start Year'] + 1
            
            df.loc[idx, 'End Month'] = end_month
        
        filled_end = mask.sum()
        
        # 5. End Day - use start day + duration
        mask = df['End Day'].isna() & df['Start Day'].notna()
        df.loc[mask, 'End Day'] = df.loc[mask, 'Start Day']
        
        print(f"  ✓ Filled temporal: Month={filled_month}, Day={filled_day}, EndDate={filled_end}")
        return df
    
    def _impute_categorical_and_binary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Impute categorical and binary fields"""
        
        # 1. Associated Dis - fill with "No_Associated_Disaster"
        if 'Associated Dis' in df.columns:
            df['Associated Dis'] = df['Associated Dis'].fillna('No_Associated_Disaster')
        
        # 2. Event Name - construct from available data
        if 'Event Name' in df.columns:
            mask = df['Event Name'].isna()
            df.loc[mask, 'Event Name'] = (
                df.loc[mask, 'Disaster Type'].astype(str) + ' - ' +
                df.loc[mask, 'Country'].astype(str) + ' ' +
                df.loc[mask, 'Year'].astype(str)
            )
        
        # 3. Location - use country or "Unknown"
        if 'Location' in df.columns:
            mask = df['Location'].isna() & df['Country'].notna()
            df.loc[mask, 'Location'] = df.loc[mask, 'Country'].astype(str) + ' (General)'
            df['Location'] = df['Location'].fillna('Unknown Location')
        
        # 4. Disaster Subtype - use Disaster Type as fallback
        if 'Disaster Subtype' in df.columns:
            df['Disaster Subtype'] = df['Disaster Subtype'].fillna(df['Disaster Type'])
        
        # 5. Disaster Group - derive from Disaster Type if possible
        if 'Disaster Group' in df.columns:
            mask = df['Disaster Group'].isna() & df['Disaster Type'].notna()
            for disaster_type, group in DISASTER_TO_GROUP.items():
                type_mask = mask & (df['Disaster Type'] == disaster_type)
                df.loc[type_mask, 'Disaster Group'] = group
            
            # Additional specific mappings for common types not in dictionary
            mask = df['Disaster Group'].isna() & df['Disaster Type'].notna()
            df.loc[mask & (df['Disaster Type'].str.contains('flood', case=False, na=False)), 'Disaster Group'] = 'Hydrological'
            df.loc[mask & (df['Disaster Type'].str.contains('storm|cyclone|wind', case=False, na=False)), 'Disaster Group'] = 'Meteorological'
            df.loc[mask & (df['Disaster Type'].str.contains('earthquake|seismic|volcano', case=False, na=False)), 'Disaster Group'] = 'Geophysical'
            df.loc[mask & (df['Disaster Type'].str.contains('drought|fire|temperature', case=False, na=False)), 'Disaster Group'] = 'Climatological'
            df.loc[mask & (df['Disaster Type'].str.contains('epidemic|disease|infection', case=False, na=False)), 'Disaster Group'] = 'Biological'
            
            # Final fallback to "Other"
            df['Disaster Group'] = df['Disaster Group'].fillna('Other')
        
        # 6. Disaster Subgroup - use Group or Type as fallback
        if 'Disaster Subgroup' in df.columns:
            # Fallback to Group or Type
            mask = df['Disaster Subgroup'].isna()
            if 'Disaster Group' in df.columns:
                df.loc[mask, 'Disaster Subgroup'] = df.loc[mask, 'Disaster Group']
            else:
                df.loc[mask, 'Disaster Subgroup'] = df.loc[mask, 'Disaster Type']
        
        # 7. Appeal - binary, fill with "No"
        if 'Appeal' in df.columns:
            df['Appeal'] = df['Appeal'].fillna('No')
        
        # 8. Declaration - binary, fill with "No"
        if 'Declaration' in df.columns:
            df['Declaration'] = df['Declaration'].fillna('No')
        
        # 9. Dis Mag Scale - fill with most common or "Unknown"
        if 'Dis Mag Scale' in df.columns:
            most_common = df['Dis Mag Scale'].mode()
            if len(most_common) > 0:
                df['Dis Mag Scale'] = df['Dis Mag Scale'].fillna(most_common[0])
            else:
                df['Dis Mag Scale'] = df['Dis Mag Scale'].fillna('Unknown')
        
        # 9a. Dis Mag Value - fill with 0 (many disasters don't have magnitude)
        if 'Dis Mag Value' in df.columns:
            df['Dis Mag Value'] = df['Dis Mag Value'].fillna(0)
        
        # 10. ISO - derive from Country
        if 'ISO' in df.columns:
            mask = df['ISO'].isna() & df['Country'].notna()
            df.loc[mask, 'ISO'] = df.loc[mask, 'Country'].map(COUNTRY_TO_ISO)
        
        # 11. Seq - fill with sequential numbers if missing
        if 'Seq' in df.columns:
            mask = df['Seq'].isna()
            if mask.sum() > 0:
                max_seq = df['Seq'].max() if df['Seq'].notna().any() else 0
                df.loc[mask, 'Seq'] = range(int(max_seq) + 1, int(max_seq) + 1 + mask.sum())
        
        # 12. Glide - try to construct if still missing after Phase 4
        # (This handles cases where construction failed)
        if 'Glide' in df.columns:
            mask = df['Glide'].isna()
            df.loc[mask, 'Glide'] = 'UNKNOWN-' + df.loc[mask, 'Year'].astype(str)
        
        # 13. GLIDE components - if still missing after construction
        if 'GLIDE_Type_Code' in df.columns:
            mask = df['GLIDE_Type_Code'].isna() & df['Disaster Type'].notna()
            for disaster_type, code in DISASTER_TO_GLIDE_TYPE.items():
                type_mask = mask & (df['Disaster Type'] == disaster_type)
                df.loc[type_mask, 'GLIDE_Type_Code'] = code
            df['GLIDE_Type_Code'] = df['GLIDE_Type_Code'].fillna('XX')
        
        if 'GLIDE_Year' in df.columns:
            df['GLIDE_Year'] = df['GLIDE_Year'].fillna(df['Year'])
        
        if 'GLIDE_Sequence' in df.columns:
            df['GLIDE_Sequence'] = df['GLIDE_Sequence'].fillna(0)
        
        if 'GLIDE_Country_ISO' in df.columns:
            mask = df['GLIDE_Country_ISO'].isna() & df['Country'].notna()
            df.loc[mask, 'GLIDE_Country_ISO'] = df.loc[mask, 'Country'].map(COUNTRY_TO_ISO)
            df['GLIDE_Country_ISO'] = df['GLIDE_Country_ISO'].fillna('XX')
        
        print(f"  ✓ Imputed all categorical and binary fields")
        return df
    
    def _impute_impact_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Impute impact metrics using KNN imputation for correlated features
        Falls back to median imputation if KNN not available
        """
        
        if not self.fitted:
            print("  ⚠ Warning: Preprocessor not fitted! Using simple median imputation.")
        
        impact_cols = ['Total Deaths', 'No Injured', 'No Affected', 'No Homeless', "Total Damages ('000 US$)"]
        
        # Add Total Affected and CPI if they exist
        if 'Total Affected' in df.columns:
            impact_cols.append('Total Affected')
        if 'CPI' in df.columns:
            impact_cols.append('CPI')
        
        # Check if we have missing values that need imputation
        missing_before = df[impact_cols].isnull().sum().sum()
        
        if missing_before > 0 and self.knn_fitted:
            # Use KNN Imputation for correlated impact metrics
            print(f"  → Using KNN imputation for {missing_before} missing values in impact metrics")
            
            # Create feature matrix for KNN
            # Add contextual features to help KNN: Year, Disaster Type (encoded)
            knn_features = df[impact_cols].copy()
            
            # Add Year as a feature (normalized)
            knn_features['Year_norm'] = (df['Year'] - df['Year'].min()) / (df['Year'].max() - df['Year'].min())
            
            # Add Disaster Type as one-hot encoding
            disaster_dummies = pd.get_dummies(df['Disaster Type'], prefix='DisType')
            # Only keep top 10 disaster types to avoid too many features
            top_disasters = df['Disaster Type'].value_counts().head(10).index
            for disaster in top_disasters:
                col_name = f'DisType_{disaster}'
                if col_name in disaster_dummies.columns:
                    knn_features[col_name] = disaster_dummies[col_name]
            
            try:
                # Apply KNN imputation
                knn_imputed = self.knn_imputer.fit_transform(knn_features)
                
                # Extract only the impact columns (not the helper features)
                for i, col in enumerate(impact_cols):
                    df[col] = knn_imputed[:, i]
                    # Ensure no negative values
                    df[col] = df[col].clip(lower=0)
                
                print(f"  ✓ KNN imputation completed successfully")
                
            except Exception as e:
                print(f"  ⚠ KNN imputation failed: {e}. Falling back to median imputation.")
                # Fall back to median imputation
                self._fallback_median_imputation(df, impact_cols)
        
        elif missing_before > 0:
            # Use median imputation as fallback
            print(f"  → Using median imputation for {missing_before} missing values")
            self._fallback_median_imputation(df, impact_cols)
        
        # Ensure no remaining nulls
        for col in impact_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # Ensure Total Affected is computed if  missing
        if 'Total Affected' in df.columns:
            mask = df['Total Affected'].isna() | (df['Total Affected'] == 0)
            df.loc[mask, 'Total Affected'] = (
                df.loc[mask, 'No Injured'].fillna(0) +
                df.loc[mask, 'No Affected'].fillna(0) +
                df.loc[mask, 'No Homeless'].fillna(0)
            )
        
        print(f"  ✓ Impact metrics imputation complete")
        return df
    
    def _fallback_median_imputation(self, df: pd.DataFrame, impact_cols: list) -> None:
        """Fallback median imputation method"""
        
        # 1. Total Deaths - impute with median by type
        if 'Total Deaths' in impact_cols:
            mask = df['Total Deaths'].isna() & df['Disaster Type'].notna()
            for disaster_type, median_val in self.median_deaths_by_type.items():
                type_mask = mask & (df['Disaster Type'] == disaster_type)
                df.loc[type_mask, 'Total Deaths'] = median_val if pd.notna(median_val) else 0
            df['Total Deaths'] = df['Total Deaths'].fillna(0)
        
        # 2. No Injured - impute with median by type
        if 'No Injured' in impact_cols:
            mask = df['No Injured'].isna() & df['Disaster Type'].notna()
            for disaster_type, median_val in self.median_injured_by_type.items():
                type_mask = mask & (df['Disaster Type'] == disaster_type)
                df.loc[type_mask, 'No Injured'] = median_val if pd.notna(median_val) else 0
            df['No Injured'] = df['No Injured'].fillna(0)
        
        # 3. No Affected - impute by (Country, Disaster Type, Decade)
        if 'No Affected' in impact_cols:
            if 'Decade' not in df.columns:
                df['Decade'] = (df['Year'] // 10) * 10
            mask = df['No Affected'].isna()
            
            for idx in df[mask].index:
                country = df.loc[idx, 'Country']
                disaster_type = df.loc[idx, 'Disaster Type']
                decade = df.loc[idx, 'Decade']
                
                key = (country, disaster_type, decade)
                median_val = self.median_affected_by_group.get(key)
                
                if pd.notna(median_val):
                    df.loc[idx, 'No Affected'] = median_val
                else:
                    # Fallback: median for just disaster type
                    fallback = df[df['Disaster Type'] == disaster_type]['No Affected'].median()
                    df.loc[idx, 'No Affected'] = fallback if pd.notna(fallback) else 0
            
            df['No Affected'] = df['No Affected'].fillna(0)
        
        # 4. No Homeless - impute with 0
        if 'No Homeless' in impact_cols:
            df['No Homeless'] = df['No Homeless'].fillna(0)
        
        # 5. Total Damages - impute by disaster type median
        if "Total Damages ('000 US$)" in impact_cols:
            mask = df["Total Damages ('000 US$)"].isna() & df['Disaster Type'].notna()
            for disaster_type, median_val in self.median_damages_by_type.items():
                type_mask = mask & (df['Disaster Type'] == disaster_type)
                df.loc[type_mask, "Total Damages ('000 US$)"] = median_val if pd.notna(median_val) else 0
            df["Total Damages ('000 US$)"] = df["Total Damages ('000 US$)"].fillna(0)
        
        # 6. CPI - forward fill or use global median
        if 'CPI' in impact_cols:
            df['CPI'] = df['CPI'].ffill().bfill().fillna(df['CPI'].median())
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create new engineered features"""
        
        # 1. Duration in days
        df['Duration_Days'] = (
            (df['End Year'] - df['Start Year']) * 365 +
            (df['End Month'].fillna(0) - df['Start Month'].fillna(0)) * 30 +
            (df['End Day'].fillna(0) - df['Start Day'].fillna(0))
        )
        df['Duration_Days'] = df['Duration_Days'].clip(lower=0)  # No negative durations
        
        # 2. Decade
        # Already created in imputation
        
        # 3. Decade Label
        df['Decade_Label'] = df['Decade'].astype(str) + 's'
        
        # 4. Severity Category (from Total Deaths)
        def categorize_severity(deaths):
            if deaths == 0:
                return 0  # No Deaths
            elif deaths < 10:
                return 1  # Minor
            elif deaths < 100:
                return 2  # Moderate
            elif deaths < 1000:
                return 3  # Severe
            else:
                return 4  # Catastrophic
        
        df['Severity_Category'] = df['Total Deaths'].apply(categorize_severity)
        
        # 5. Total Human Impact
        df['Total_Human_Impact'] = (
            df['Total Deaths'].fillna(0) +
            df['No Injured'].fillna(0) +
            df['No Affected'].fillna(0)
        )
        
        # 6. Data Era (Historical/Modern/Recent)
        def categorize_era(year):
            if year < 1990:
                return 'Historical'
            elif year < 2010:
                return 'Modern'
            else:
                return 'Recent'
        
        df['Data_Era'] = df['Year'].apply(categorize_era)
        
        # 7. Season from Start Month
        def get_season(month):
            if pd.isna(month):
                return 'Unknown'
            month = int(month)
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            else:
                return 'Fall'
        
        df['Season'] = df['Start Month'].apply(get_season)
        
        # 8. Is Recent (last 10 years)
        current_year = 2026
        df['Is_Recent'] = (df['Year'] >= current_year - 10).astype(int)
        
        # 9. Disaster Group (from disaster type)
        df['Disaster Group'] = df['Disaster Type'].map(DISASTER_TO_GROUP)
        
        print(f"  ✓ Created 9 engineered features")
        return df
    
    def _final_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        """Final data cleaning and validation"""
        
        # 1. Ensure no negative values in impact metrics
        impact_cols = ['Total Deaths', 'No Injured', 'No Affected', 'No Homeless', "Total Damages ('000 US$)"]
        for col in impact_cols:
            if col in df.columns:
                df[col] = df[col].clip(lower=0)
        
        # 2. Ensure temporal consistency
        # End Year >= Start Year
        mask = df['End Year'] < df['Start Year']
        df.loc[mask, 'End Year'] = df.loc[mask, 'Start Year']
        
        # 3. Data type conversions
        int_cols = ['Year', 'Start Year', 'End Year', 'Start Month', 'End Month', 'Start Day', 'End Day']
        for col in int_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
        # 4. Remove any remaining duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        removed_dupes = initial_count - len(df)
        
        if removed_dupes > 0:
            print(f"  ✓ Removed {removed_dupes} duplicate rows")
        
        # 5. Final catch-all imputation for any remaining nulls
        # Disaster Group - absolute fallback
        if 'Disaster Group' in df.columns:
            df['Disaster Group'] = df['Disaster Group'].fillna('Other')
        
        # All categorical columns - replace any remaining NaNs with "Unknown"
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna('Unknown')
        
        # All numerical columns - replace any remaining NaNs with 0
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(0)
        
        print(f"  ✓ Final cleaning complete")
        return df


# ============================================================================
# PART 4: MAIN PREPROCESSING FUNCTIONS
# ============================================================================

def preprocess_training_data(
    file_path: str,
    test_size: float = 0.2,
    temporal_split: bool = True,
    cutoff_year: int = 2020
) -> Tuple[pd.DataFrame, pd.DataFrame, DisasterDataPreprocessor]:
    """
    Complete preprocessing for training data with train/test split
    
    Parameters:
    -----------
    file_path : Path to CSV file
    test_size : Fraction for test set (if not using temporal split)
    temporal_split : Use temporal split (recommended for time series)
    cutoff_year : Year for temporal split
    
    Returns:
    --------
    train_df, test_df, fitted_preprocessor
    """
    print("\n" + "=" * 80)
    print("DISASTER DATA PREPROCESSING - TRAINING MODE")
    print("=" * 80)
    
    # Load data
    print("\nLoading data...")
    df = pd.read_csv(file_path, low_memory=False)
    print(f"Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # Initialize preprocessor
    preprocessor = DisasterDataPreprocessor()
    
    # PHASE 1: Basic preprocessing (BEFORE split)
    print("\n" + "=" * 80)
    print("PHASE 1: BASIC PREPROCESSING (BEFORE SPLIT)")
    print("=" * 80)
    
    # Drop completely useless columns (>90% missing or not analytical)
    drop_cols = [
        # Extremely high missing (>95%) + not critical
        'Insured Damages (\'000 US$)',  # 99.5% missing, geographic bias
        'Local Time',                    # 98.6% missing, not critical
        'Associated Dis2',               # 97.8% missing, redundant
        'Aid Contribution',              # 95.6% missing, out of scope
        
        # High missing (>70%) + administrative/not useful
        'River Basin',                   # 91.2% missing, too specific
        'OFDA Response',                 # 82.6% missing, US-specific response
        'Admin1 Code',                   # 77.0% missing, have Country
        'Admin2 Code',                   # 74.2% missing, too granular
        'Origin',                        # 71.1% missing, not well-defined
        
        # Medium missing (>50%) + redundant/not needed
        'Adm Level',                     # 55.3% missing, not needed
        'Geo Locations',                 # 55.3% missing, have Lat/Lon
        'Disaster Subsubtype',           # 97.4% missing, too granular
    ]
    drop_cols = [col for col in drop_cols if col in df.columns]
    df = df.drop(columns=drop_cols, errors='ignore')
    print(f"Dropped {len(drop_cols)} useless columns")
    print(f"Remaining columns: {len(df.columns)}")
    
    # Basic transformations (no statistics!)
    df = preprocessor.transform(df, is_training=True)
    
    # PHASE 2: Split data
    print("\n" + "=" * 80)
    print("PHASE 2: SPLITTING DATA")
    print("=" * 80)
    
    if temporal_split:
        print(f"Using temporal split at year {cutoff_year}")
        train_df = df[df['Year'] < cutoff_year].copy()
        test_df = df[df['Year'] >= cutoff_year].copy()
    else:
        from sklearn.model_selection import train_test_split
        print(f"Using random split ({test_size*100}% test)")
        train_df, test_df = train_test_split(
            df, test_size=test_size, random_state=42,
            stratify=df['Severity_Category'] if 'Severity_Category' in df.columns else None
        )
    
    print(f"Train set: {len(train_df):,} rows ({len(train_df)/len(df)*100:.1f}%)")
    print(f"Test set:  {len(test_df):,} rows ({len(test_df)/len(df)*100:.1f}%)")
    
    # PHASE 3: Fit preprocessor on training data ONLY
    print("\n" + "=" * 80)
    print("PHASE 3: FITTING PREPROCESSOR ON TRAINING DATA")
    print("=" * 80)
    preprocessor.fit(train_df)
    
    print("\n" + "=" * 80)
    print("PREPROCESSING COMPLETE!")
    print("=" * 80)
    print(f"✓ Training set ready: {train_df.shape}")
    print(f"✓ Test set ready: {test_df.shape}")
    print(f"✓ Preprocessor fitted and ready for new data")
    
    return train_df, test_df, preprocessor


def preprocess_new_data(
    file_path: str,
    preprocessor: DisasterDataPreprocessor
) -> pd.DataFrame:
    """
    Preprocess new/production data using fitted preprocessor
    This is AUTOMATIC - no manual intervention needed!
    
    Parameters:
    -----------
    file_path : Path to new CSV file
    preprocessor : Fitted DisasterDataPreprocessor instance
    
    Returns:
    --------
    Preprocessed DataFrame ready for predictions
    """
    print("\n" + "=" * 80)
    print("DISASTER DATA PREPROCESSING - PRODUCTION MODE")
    print("=" * 80)
    
    if not preprocessor.fitted:
        raise ValueError("Preprocessor must be fitted on training data first!")
    
    # Load new data
    print("\nLoading new data...")
    df = pd.read_csv(file_path, low_memory=False)
    print(f"Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    # Drop same columns as training
    drop_cols = [
        'Insured Damages (\'000 US$)', 'Local Time', 'Associated Dis2',
        'Aid Contribution', 'River Basin', 'OFDA Response',
        'Admin1 Code', 'Admin2 Code', 'Origin', 'Adm Level',
        'Geo Locations', 'Disaster Subsubtype'
    ]
    drop_cols = [col for col in drop_cols if col in df.columns]
    df = df.drop(columns=drop_cols, errors='ignore')
    
    # Apply preprocessing (AUTOMATIC!)
    df = preprocessor.transform(df, is_training=False)
    
    print("\n" + "=" * 80)
    print("NEW DATA PREPROCESSING COMPLETE!")
    print("=" * 80)
    print(f"✓ Ready for predictions: {df.shape}")
    
    return df


# ============================================================================
# PART 5: UTILITY FUNCTIONS
# ============================================================================

def save_preprocessor(preprocessor: DisasterDataPreprocessor, file_path: str):
    """Save fitted preprocessor for later use"""
    import joblib
    joblib.dump(preprocessor, file_path)
    print(f"✓ Preprocessor saved to: {file_path}")


def load_preprocessor(file_path: str) -> DisasterDataPreprocessor:
    """Load previously saved preprocessor"""
    import joblib
    preprocessor = joblib.load(file_path)
    print(f"✓ Preprocessor loaded from: {file_path}")
    return preprocessor


def generate_preprocessing_report(df_before: pd.DataFrame, df_after: pd.DataFrame):
    """Generate detailed report of preprocessing changes"""
    print("\n" + "=" * 80)
    print("PREPROCESSING REPORT")
    print("=" * 80)
    
    print(f"\n📊 Shape Changes:")
    print(f"  Before: {df_before.shape}")
    print(f"  After:  {df_after.shape}")
    print(f"  Rows removed: {df_before.shape[0] - df_after.shape[0]}")
    print(f"  Columns added: {df_after.shape[1] - df_before.shape[1]}")
    
    print(f"\n📉 Missing Values Reduction:")
    before_missing = df_before.isnull().sum().sum()
    after_missing = df_after.isnull().sum().sum()
    print(f"  Before: {before_missing:,} missing values")
    print(f"  After:  {after_missing:,} missing values")
    print(f"  Reduced by: {before_missing - after_missing:,} ({(1-after_missing/before_missing)*100:.1f}%)")
    
    print(f"\n✨ New Features Created:")
    new_cols = set(df_after.columns) - set(df_before.columns)
    for col in sorted(new_cols):
        print(f"  • {col}")
    
    print("\n" + "=" * 80)


# ============================================================================
# MAIN EXECUTION EXAMPLE
# ============================================================================

if __name__ == "__main__":
    
    # Example usage
    print("""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║     DISASTER DATA PREPROCESSING PIPELINE                             ║
    ║     Comprehensive preprocessing with automatic handling              ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # TRAINING PHASE
    print("\n" + "="*80)
    print("EXAMPLE: Training Phase")
    print("="*80)
    
    # Preprocess training data
    train_df, test_df, preprocessor = preprocess_training_data(
        file_path='Book1.csv',
        temporal_split=False,
        test_size=0.2
    )
    
    # Save preprocessor for later use
    save_preprocessor(preprocessor, 'disaster_preprocessor.pkl')
    
    # Save processed data
    train_df.to_csv('train_processed.csv', index=False)
    test_df.to_csv('test_processed.csv', index=False)
    print("\n✓ Saved processed train/test sets")
    
    # PRODUCTION PHASE (Simulated)
    print("\n" + "="*80)
    print("EXAMPLE: Production Phase (New Data)")
    print("="*80)
    
    # Load saved preprocessor
    preprocessor = load_preprocessor('disaster_preprocessor.pkl')
    
    # Process new data (automatically applies all transformations)
    # new_df = preprocess_new_data('new_disaster_data.csv', preprocessor)
    
    print("\n✅ Pipeline ready for production use!")
    print("\nTo use in your code:")
    print("  1. preprocessor = load_preprocessor('disaster_preprocessor.pkl')")
    print("  2. new_data_clean = preprocess_new_data('new_file.csv', preprocessor)")
    print("  3. predictions = model.predict(new_data_clean)")
