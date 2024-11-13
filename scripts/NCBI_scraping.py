#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 18:50:43 2024

@author: dgaio
"""


import logging
from Bio import Entrez

def load_credentials(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except Exception as e:
        logging.error(f"Error loading data from {file_path}: {e}")
        return None

def search_and_download_abstracts(email_path, api_key_path, search_term, max_results):
    email = load_credentials(email_path)
    api_key = load_credentials(api_key_path)
    
    if not email or not api_key:
        logging.error("Email or API key could not be loaded.")
        return

    Entrez.email = email
    Entrez.api_key = api_key

    # Search for articles that match the search term in PubMed
    search_handle = Entrez.esearch(db="pubmed", term=search_term, retmax=max_results)
    search_results = Entrez.read(search_handle)
    search_handle.close()

    # Get the list of Ids from the search results
    id_list = search_results['IdList']
    
    # Fetch the abstracts based on the Id list
    fetch_handle = Entrez.efetch(db="pubmed", id=",".join(id_list), rettype="abstract", retmode="text")
    abstracts = fetch_handle.read()
    fetch_handle.close()
    
    return abstracts

# Set the paths for your API key and email address files
api_key_path = "my_api_key_NCBI"
email_path = "my_outlook"

# Example usage
abstracts = search_and_download_abstracts(email_path, api_key_path, "infliximab AND vedolizumab[tiab]", 10)
print(abstracts)





    

    

import pandas as pd
import numpy as np

entries = abstracts.strip().split('\n\n\n')
parsed_data = []

for entry in entries:
    parts = entry.split('\n\n')
    print(parts)  # This helps in visually inspecting how the parts are split
    
    title = parts[1].strip()  

    # how to tell which one is the abstract? 
    # abstract will be the largest piuece of text of all the lines elements, 
    # we only need to make sure to avoid these potentially lengthy elements: 
        # starting with "Conflict of interest"
        # starting with "Author information:"
    abstract = None
    max_length = 0
    for part in parts:
        if (part.startswith("Conflict of interest") or
            part.startswith("Author information:") or
            part[0].isdigit()):  # Skip parts starting with a digit
            continue
        if len(part) > max_length:
            max_length = len(part)
            abstract = part

    # Check if title and abstract are the same
    if title == abstract:
        abstract = np.nan  # Assign NaN if they are identical

    # Extract DOI
    doi = None
    for part in parts:
        if part.startswith("DOI:"):
            doi = part.replace("DOI:", "").strip()
            break  # Assuming there's only one DOI per entry

    # Compile the parsed information into a dictionary and append to the list
    parsed_data.append({
        'Title': title,
        'Abstract': abstract,
        'DOI': doi
    })

# Convert the list of dictionaries into a DataFrame
df = pd.DataFrame(parsed_data)
print(df)

    
        
        


