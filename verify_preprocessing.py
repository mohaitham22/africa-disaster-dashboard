"""
Verification Script for Preprocessed Data
==========================================
Checks data quality, missing values, and feature summary
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("PREPROCESSING VERIFICATION REPORT")
print("=" * 80)

# Load processed data
train = pd.read_csv('train_processed.csv')
test = pd.read_csv('test_processed.csv')

# Basic Info
print("\n📊 DATASET SHAPES:")
print(f"   Train: {train.shape[0]:,} rows × {train.shape[1]} columns")
print(f"   Test:  {test.shape[0]:,} rows × {test.shape[1]} columns")
print(f"   Total: {train.shape[0] + test.shape[0]:,} rows")

# Missing Values Check
train_missing = train.isnull().sum().sum()
test_missing = test.isnull().sum().sum()
total_missing = train_missing + test_missing

print("\n🔍 MISSING VALUES:")
print(f"   Train: {train_missing} missing values")
print(f"   Test:  {test_missing} missing values")
print(f"   Total: {total_missing} missing values")

if total_missing == 0:
    print("\n   ✅ SUCCESS: NO MISSING VALUES!")
    print("   🎉 Data is ready for machine learning!")
else:
    print(f"\n   ⚠️ WARNING: Found {total_missing} missing values")
    print("\n   Columns with missing values:")
    
    # Show missing by column
    all_missing = train.isnull().sum().add(test.isnull().sum(), fill_value=0)
    missing_cols = all_missing[all_missing > 0].sort_values(ascending=False)
    
    for col, count in missing_cols.items():
        pct_train = train[col].isnull().sum() / len(train) * 100
        pct_test = test[col].isnull().sum() / len(test) * 100
        print(f"     • {col}: {int(count)} total ({pct_train:.1f}% train, {pct_test:.1f}% test)")

# Data Types Summary
print("\n📋 FEATURE TYPES:")
numerical_cols = train.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = train.select_dtypes(include=['object']).columns.tolist()
print(f"   Numerical:   {len(numerical_cols)} features")
print(f"   Categorical: {len(categorical_cols)} features")

# Impact Metrics Summary
print("\n💥 IMPACT METRICS SUMMARY:")
impact_cols = ['Total Deaths', 'No Injured', 'No Affected', 'No Homeless', "Total Damages ('000 US$)"]
for col in impact_cols:
    if col in train.columns:
        print(f"   {col}:")
        print(f"      Min:    {train[col].min():,.0f}")
        print(f"      Median: {train[col].median():,.0f}")
        print(f"      Max:    {train[col].max():,.0f}")
        print(f"      Nulls:  {train[col].isnull().sum()}")

# Engineered Features Check
print("\n✨ ENGINEERED FEATURES:")
engineered = [
    'GLIDE_Type_Code', 'GLIDE_Year', 'GLIDE_Sequence', 'GLIDE_Country_ISO',
    'Deaths_Known', 'Injured_Known', 'Affected_Known', 'Homeless_Known',
    'Damages_Known', 'Location_Precise', 'Has_Magnitude', 'GLIDE_Complete',
    'Decade', 'Duration_Days', 'Decade_Label', 'Severity_Category',
    'Total_Human_Impact', 'Data_Era', 'Season', 'Is_Recent'
]

present_engineered = [col for col in engineered if col in train.columns]
print(f"   Found {len(present_engineered)}/{len(engineered)} expected engineered features")

# Target Variable Distribution
if 'Severity_Category' in train.columns:
    print("\n🎯 TARGET VARIABLE DISTRIBUTION (Severity_Category):")
    severity_dist = train['Severity_Category'].value_counts().sort_index()
    for severity, count in severity_dist.items():
        pct = count / len(train) * 100
        print(f"   Level {int(severity)}: {count:,} rows ({pct:.1f}%)")

# Data Quality Flags
print("\n🚩 DATA QUALITY FLAGS:")
flag_cols = [col for col in train.columns if '_Known' in col or '_Precise' in col or '_Complete' in col]
for col in flag_cols:
    true_count = train[col].sum() if train[col].dtype in ['bool', 'int64', 'float64'] else 0
    pct = true_count / len(train) * 100
    print(f"   {col}: {true_count:,}/{len(train):,} ({pct:.1f}%) are original/complete")

# Temporal Distribution
print("\n📅 TEMPORAL DISTRIBUTION:")
print(f"   Train Years: {int(train['Year'].min())} - {int(train['Year'].max())}")
print(f"   Test Years:  {int(test['Year'].min())} - {int(test['Year'].max())}")
print(f"   Total Range: {int(train['Year'].min())} - {int(test['Year'].max())} ({int(test['Year'].max()) - int(train['Year'].min()) + 1} years)")

# Geographic Coverage
print("\n🌍 GEOGRAPHIC COVERAGE:")
print(f"   Unique Countries: {train['Country'].nunique()} in train, {test['Country'].nunique()} in test")
print(f"   Unique Regions:   {train['Region'].nunique() if 'Region' in train.columns else 'N/A'}")
print(f"   Continents:       {train['Continent'].nunique() if 'Continent' in train.columns else 'N/A'}")

# Disaster Types
print("\n🌪️  DISASTER TYPES:")
print(f"   Unique Types:     {train['Disaster Type'].nunique()}")
print(f"   Top 5 Types:")
top_disasters = train['Disaster Type'].value_counts().head(5)
for disaster, count in top_disasters.items():
    pct = count / len(train) * 100
    print(f"      • {disaster}: {count} ({pct:.1f}%)")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE!")
print("=" * 80)

# Final Summary
print("\n📝 SUMMARY:")
print(f"   ✓ {train.shape[0] + test.shape[0]:,} total disaster events processed")
print(f"   ✓ {train.shape[1]} features per event")
print(f"   ✓ {total_missing} missing values")
print(f"   ✓ {int(train['Year'].min())}-{int(test['Year'].max())} temporal coverage")
print(f"   ✓ {train['Country'].nunique()} countries represented")
print(f"   ✓ {train['Disaster Type'].nunique()} disaster types")

if total_missing == 0:
    print("\n   🎉 READY FOR MODEL TRAINING! 🎉")
else:
    print(f"\n   ⚠️  {total_missing} missing values need attention")

print("=" * 80)
