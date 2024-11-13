#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 13:50:45 2024

@author: dgaio
"""

# https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html

import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
import numpy as np
import matplotlib.cm as cm


# Define your fields list here as shown in your previous message

def extract_data(report, fields):
    report_data = {}
    for field in fields:
        element = report.find('.//' + field.strip('/'))  # Normalize and find the field
        if element is not None:
            report_data[field] = element.text
        else:
            report_data[field] = 'NA'  # Use 'NA' if the field is missing
    return report_data

def process_xml(file_path, fields):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = [extract_data(report, fields) for report in root.findall('.//safetyreport')]
    return pd.DataFrame(data)


def process_multiple_xml(files, fields):
    df_list = [process_xml(file, fields) for file in files]
    return pd.concat(df_list, ignore_index=True)



fields = [
    'activesubstance', '/drug', '/drugrecurrence', '/ichicsr', '/ichicsrmessageheader', '/patient',
    '/primarysource', '/reaction', '/receiver', '/reportduplicate', '/safetyreport', '/sender', '/summary',
    'actiondrug', 'activesubstance', 'activesubstancename', 'authoritynumb', 'companynumb', 'drug',
    'drugadditional', 'drugadministrationroute', 'drugauthorizationnumb', 'drugbatchnumb', 'drugcharacterization',
    'drugcumulativedosagenumb', 'drugcumulativedosageunit', 'drugdosageform', 'drugdosagetext',
    'drugenddate', 'drugenddateformat', 'drugindication', 'drugintervaldosagedefinition',
    'drugintervaldosageunitnumb', 'drugrecuraction', 'drugrecuractionmeddraversion',
    'drugrecurreadministration', 'drugrecurrence', 'drugseparatedosagenumb', 'drugstartdate',
    'drugstartdateformat', 'drugstructuredosagenumb', 'drugstructuredosageunit', 'drugtreatmentduration',
    'drugtreatmentdurationunit', 'duplicate', 'duplicatenumb', 'duplicatesource', 'fulfillexpeditecriteria',
    'ichicsr', 'ichicsrmessageheader', 'literaturereference', 'medicinalproduct', 'messagedate',
    'messagedateformat', 'messageformatrelease', 'messageformatversion', 'messagenumb', 'messagereceiveridentifier',
    'messagesenderidentifier', 'messagetype', 'narrativeincludeclinical', 'occurcountry', 'patient',
    'patientagegroup', 'patientonsetage', 'patientonsetageunit', 'patientsex', 'patientweight',
    'primarysource', 'primarysourcecountry', 'qualification', 'reaction', 'reactionmeddrapt', 'reactionmeddraversionpt',
    'reactionoutcome', 'receiptdate', 'receiptdateformat', 'receivedate', 'receivedateformat', 'receiver',
    'receiverorganization', 'receivertype', 'reportduplicate', 'reportercountry', 'reporttype',
    'safetyreport', 'safetyreportid', 'safetyreportversion', 'sender', 'senderorganization', 'sendertype',
    'serious', 'seriousnesscongenitalanomali', 'seriousnessdeath', 'seriousnessdisabling', 'seriousnesshospitalization',
    'seriousnesslifethreatening', 'seriousnessother', 'summary', 'transmissiondate', 'transmissiondateformat'
]
len(fields)



# List of XML files to process
xml_files = [
    '/Users/dgaio/Downloads/faers_xml_2024q3/XML/1_ADR24Q3.xml',
    '/Users/dgaio/Downloads/faers_xml_2024q3/XML/2_ADR24Q3.xml',
    '/Users/dgaio/Downloads/faers_xml_2024q3/XML/3_ADR24Q3.xml'
]

# Process all XML files and merge the data into one DataFrame
all_data_df = process_multiple_xml(xml_files, fields)

# Print the DataFrame
print(all_data_df)



# Create a DataFrame
df0 = pd.DataFrame(all_data_df)

# Print the DataFrame
print(df0)

column_names = df0.columns.tolist()
len(column_names)
print(column_names)


# Replace 'NA' and strip whitespace
df0.replace('NA', np.nan, inplace=True)  # Replace 'NA' with NaN
df0 = df0.applymap(lambda x: np.nan if isinstance(x, str) and x.strip() == '' else x)

# Drop columns where all entries are NaN after the replacement
df0_cleaned = df0.dropna(axis=1, how='all')

# Optionally, drop rows that are entirely NaN as well
df0_cleaned.dropna(axis=0, how='all', inplace=True)


print(len(df0_cleaned))

column_names = df0_cleaned.columns.tolist()
print(column_names)
len(column_names)



# List of columns to grab
columns_to_select = [
    'safetyreportid', 'activesubstancename', 'drugindication', 'medicinalproduct', 'occurcountry', 
    'patientagegroup', 'patientsex', 'patientweight', 'reactionmeddrapt'
]

df0_cleaned = df0_cleaned[columns_to_select]




# Some stats and plotting: 

# Basic stats and counts for selected columns
df0 = df0_cleaned
total_reports = len(df0)

# Overview statistics for each selected column
print(f"Total reports: {total_reports}")
print(f"Number of unique reports (safetyreportid): {df0['safetyreportid'].nunique()}")


# Function to get column stats
def column_overview(df, col):
    unique_count = df[col].nunique()
    missing_count = df[col].isna().sum()
    top_values = df[col].value_counts().head(5)  # Top 5 most frequent values
    return unique_count, missing_count, top_values

# Overview for each column
for col in columns_to_select[1:]:  # Skip safetyreportid for individual stats
    unique_count, missing_count, top_values = column_overview(df0, col)
    print(f"\n--- {col} ---")
    print(f"Unique values: {unique_count}")
    print(f"Missing values: {missing_count}")
    print("Top 5 values:")
    print(top_values)

# Additional specific statistics
print("\nDetailed Statistics:")
print(f"Number of unique adverse reactions: {df0['reactionmeddrapt'].nunique()}")
print(f"Number of unique drug indications: {df0['drugindication'].nunique()}")
print(f"Number of unique medicinal products: {df0['medicinalproduct'].nunique()}")
print(f"Number of unique active substances: {df0['activesubstancename'].nunique()}")



# Pie chart for `occurcountry`, omitting labels for values below 2.5%
country_counts = df0['occurcountry'].value_counts()
total = country_counts.sum()
percentages = 100 * country_counts / total

# Separate countries over and under the 2.5% threshold
over_threshold = percentages[percentages > 2.5]
under_threshold = percentages[percentages <= 2.5]

# Add an "Other" category for all countries under 2.5%
over_threshold['Other'] = under_threshold.sum()

# Define custom colors
colors = cm.Paired(range(len(over_threshold)))  # Choose a different color map or palette here

# Plot the pie chart
plt.figure(figsize=(8, 8))
plt.pie(
    over_threshold,
    labels=over_threshold.index,
    autopct=lambda pct: ('%1.1f%%' % pct) if pct > 2.5 else '',
    startangle=140,
    pctdistance=0.85,
    colors=colors
)
plt.title('Distribution of reports by country')
plt.axis('equal')  # Ensures the pie chart is circular
plt.show()


# Convert columns to numeric if necessary, using errors='coerce' to handle non-numeric values gracefully
df0['patientagegroup'] = pd.to_numeric(df0['patientagegroup'], errors='coerce')
df0['patientsex'] = pd.to_numeric(df0['patientsex'], errors='coerce')
df0['patientweight'] = pd.to_numeric(df0['patientweight'], errors='coerce')



# Bar chart for `patientagegroup` with custom labels
age_group_counts = df0['patientagegroup'].replace({
    1: 'Neonate', 2: 'Infant', 3: 'Child', 4: 'Adolescent', 5: 'Adult', 6: 'Elderly'
}).value_counts().reindex(['Neonate', 'Infant', 'Child', 'Adolescent', 'Adult', 'Elderly'], fill_value=0)

plt.figure(figsize=(10, 6))
age_group_counts.plot(kind='bar', color='#fac306')  # Set color to purple
plt.title('Distribution of patient age groups')
plt.ylabel('Number of reports')
plt.xticks(rotation=0)  # Rotate x-axis labels horizontally
plt.show()

# Bar chart for `patientsex` with custom labels
sex_counts = df0['patientsex'].replace({
    0: 'Unknown', 1: 'Male', 2: 'Female'
}).value_counts().reindex(['Unknown', 'Male', 'Female'], fill_value=0)

plt.figure(figsize=(8, 6))
sex_counts.plot(kind='bar')
plt.title('Distribution of patient sex')
plt.ylabel('Number of Reports')
plt.xticks(rotation=0)  # Rotate x-axis labels horizontally
plt.show()


# Histogram for `patientweight` with 10 kg bins, capped at 500 kg
plt.figure(figsize=(10, 6))
plt.hist(
    df0['patientweight'].dropna(), 
    bins=range(0, min(500, int(df0['patientweight'].max()) + 10), 10),  # Binning every 10 kg, capped at 500 kg
    color='green',                  # Set color to green
    edgecolor='black'               # Add black edges to show lines between bars
)
plt.title('Distribution of patient weight')
plt.xlabel('weight (kg)')
plt.ylabel('Frequency')
plt.xlim(0, 300)  # Set x-axis limit to 300 kg
plt.show()



###
# how many unique adverse effects? pie chart (filtered by specific drug)
# Filter data for the specified drug
df0 = df0_cleaned
drug_name = "infliximab"
df0 = df0[df0['activesubstancename'].str.contains(drug_name, case=False, na=False)]
print(len(df0))
reaction_counts = df0['reactionmeddrapt'].value_counts()

# Calculate the total and percentages
total = sum(reaction_counts)
percentages = 100 * reaction_counts / total

# Separate reactions over and under the 1.5% threshold
over_threshold = percentages[percentages > 1.5]
under_threshold = percentages[percentages <= 1.5]

# Add an "Other" category for all reactions under 1.5%
over_threshold['Other'] = under_threshold.sum()

# Adjust labels to show only significant reactions or 'Other'
labels = over_threshold.index

# Plotting the pie chart
plt.figure(figsize=(10, 8))
wedges, texts, autotexts = plt.pie(over_threshold, labels=labels, autopct=lambda pct: ('%1.1f%%' % pct) if pct > 1.4 else '',
                                   startangle=140, pctdistance=0.85)

# Set font size for the labels and autopct, adjust 'label_size' and 'autopct_size' as needed
label_size = 10
autopct_size = 8
for text, autotext in zip(texts, autotexts):
    text.set_fontsize(label_size)
    autotext.set_fontsize(autopct_size)

plt.axis('equal')  # Ensures the pie chart is drawn as a circle
plt.title(f'Distribution of adverse reactions from {drug_name}')
plt.show()
###



























# same report id: identical side effect, 2 drugs 
# weight gain 
# olanzapine 
# lithium 








# drug combos - specific 

df = df0_cleaned

# Fill or handle missing values
df.fillna({'medicinalproduct': 'Unknown', 'reactionmeddrapt': 'No Reaction Reported'}, inplace=True)

# Specify the drugs and the adverse effect
drug_name1 = "IBUPROFEN"
drug_name2 = "FUROSEMIDE"
adverse_effect = "dehydration"

# Filter for the specific adverse effect
effect_df = df[df['reactionmeddrapt'].str.contains(adverse_effect, case=False, na=False)]

# Filter for reports that mention either or both drugs
drug_a_effects = effect_df[effect_df['medicinalproduct'].str.contains(drug_name1, case=False, na=False)]
drug_b_effects = effect_df[effect_df['medicinalproduct'].str.contains(drug_name2, case=False, na=False)]

# Identify report_ids with adverse effect for each drug
patients_with_drug_a = set(drug_a_effects['safetyreportid'])
patients_with_drug_b = set(drug_b_effects['safetyreportid'])

# Find common patients who reported the adverse effect with both drugs
common_patients = patients_with_drug_a.intersection(patients_with_drug_b)

# Count of such patients
count_common_patients = len(common_patients)
count_a_only = len(patients_with_drug_a - patients_with_drug_b)
count_b_only = len(patients_with_drug_b - patients_with_drug_a)

# Output the results
print(f"{count_common_patients} patients reported the adverse effect '{adverse_effect}' with both {drug_name1} and {drug_name2}.")
print(f"{count_a_only} patients reported the adverse effect '{adverse_effect}' with only {drug_name1}.")
print(f"{count_b_only} patients reported the adverse effect '{adverse_effect}' with only {drug_name2}.")






# drug combos - general 

# wayyyy too slow but ok if filtering by adverse effect




df = df0_cleaned

adverse_effect = "vomiting"

# Filter for the specific adverse effect
df = df[df['reactionmeddrapt'].str.contains(adverse_effect, case=False, na=False)]
len(df)


# Treat each 'medicinalproduct' entry as a single 'drug' without splitting
df['drugs'] = df['medicinalproduct'].apply(lambda x: [x.strip()])  # Strip and encapsulate in list

# Create a set for all unique drugs mentioned across all reports for accurate combinations
all_drugs = set()
df['drugs'].apply(lambda drugs: all_drugs.update(drugs))

# Create all possible pairs of drugs
drug_pairs = list(combinations(all_drugs, 2))

# Initialize a dictionary to store drug pairs and their associated adverse effects
drug_effects = {pair: [] for pair in drug_pairs}

# Iterate over each report, check for drug pairs and record their associated reactions
for index, row in df.iterrows():
    report_drugs = set(row['drugs'][0])  # Access the single-item list
    report_reaction = row['reactionmeddrapt']
    for pair in drug_pairs:
        if set(pair).issubset(report_drugs):
            drug_effects[pair].append(report_reaction)

# Convert to DataFrame for better analysis and visualization
drug_effects_df = pd.DataFrame([(pair[0], pair[1], effects) for pair, effects in drug_effects.items() if effects], columns=['Drug1', 'Drug2', 'Reactions'])

# Process the Reactions column to count occurrences
drug_effects_df['Reaction Counts'] = drug_effects_df['Reactions'].apply(lambda x: dict(Counter(x)))

# Drop the original Reactions column as it's redundant now
drug_effects_df.drop(columns=['Reactions'], inplace=True)

# Display the DataFrame
print(drug_effects_df)








# Adverse effects of drug A alone, versus combined with other drugs : 

df = df0_cleaned[0:10]

# Fill or handle missing values
df.fillna({'activesubstancename': 'Unknown', 'reactionmeddrapt': 'No Reaction Reported'}, inplace=True)

# Define the main drug of interest
drug_name = "ACETAMINOPHEN"

# Extract all unique adverse effects
unique_effects = df['reactionmeddrapt'].unique()
len(unique_effects)
#unique_effects=unique_effects[0:1000]

# Prepare a list to store results
results = []
count=0
# Loop over each unique adverse effect
for effect in unique_effects:
    
    count+=1
    
    print('processing ...', count)
    # Filter for reports where the current effect is mentioned
    effect_reports = df[df['reactionmeddrapt'].str.contains(effect, case=False, na=False)]
    
    # Reports mentioning 'ACETAMINOPHEN'
    acetaminophen_reports = effect_reports[effect_reports['activesubstancename'].str.contains(drug_name, case=False, na=False)]

    # Get other drugs mentioned with 'ACETAMINOPHEN' from those reports
    other_drugs = acetaminophen_reports['activesubstancename'].str.replace(drug_name, '', regex=False)
    other_drugs = other_drugs.str.get_dummies(sep=',')  # Customize separator if different
    other_drugs_sum = other_drugs.sum()

    # Reports with 'ACETAMINOPHEN' alone
    acetaminophen_alone = effect_reports[effect_reports['activesubstancename'].str.contains(r'^' + drug_name + '$', case=False, na=False, regex=True)]
    alone_count = len(acetaminophen_alone)

    # Append results for current adverse effect
    results.append({
        'Adverse_Effect': effect,
        'ACETAMINOPHEN_Alone': alone_count,
        'With_Other_Drugs': len(acetaminophen_reports) - alone_count,
        'Other_Drugs_Counts': other_drugs_sum.to_dict()
    })

# Create a DataFrame from the results
results_df = pd.DataFrame(results)

# Show the resulting DataFrame
print(results_df)







