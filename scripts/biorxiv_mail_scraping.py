#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 17:58:37 2023

@author: dgaio
"""


import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import re


# Function to read email credentials from a file
def read_credentials(filename):
    with open(filename, 'r') as file:
        email_address = file.readline().strip()
        password = file.readline().strip()
        return email_address, password


# Read credentials from 'my_gmail.txt'
email_address, password = read_credentials('python_main_access.txt')

# IMAP server information for Gmail
imap_server = 'imap.gmail.com'
imap_port = 993

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(imap_server, imap_port)

# Login to the server
mail.login(email_address, password)

# Select the inbox
mail.select('inbox')

# Search for specific emails
status, messages = mail.search(None, 'FROM', '"cshljnls-mailer@alerts.highwire.org"')

# Convert messages to a list of email IDs
messages = messages[0].split()
len(messages)


# Initialize a dictionary to hold subjects and their corresponding DOIs as sets
subjects_and_dois = {}

for msg_id in messages[:5]:  # Limit to first 50 emails for testing
    try:
        status, data = mail.fetch(msg_id, '(RFC822)')
        email_msg = email.message_from_bytes(data[0][1])

        # Decode the email subject
        subject = decode_header(email_msg['subject'])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        # Initialize the subject key in the dictionary with a set if not already present
        if subject not in subjects_and_dois:
            subjects_and_dois[subject] = set()

        # Extract the email content
        content = ""
        if email_msg.is_multipart():
            for part in email_msg.walk():
                if part.get_content_type() == 'text/html':
                    content = part.get_payload(decode=True).decode()
        else:
            content = email_msg.get_payload(decode=True).decode()

        # Use regular expression to find full DOIs and add them to the set
        full_dois = re.findall(r'10\.1101/\d{4}\.\d{2}\.\d{2}\.\d{6}', content)
        for doi in full_dois:
            subjects_and_dois[subject].add(doi)

    except imaplib.IMAP4.error as e:
        print("An IMAP error occurred:", e)

# Convert sets back to lists (optional, if you need lists instead of sets)
for subject in subjects_and_dois:
    subjects_and_dois[subject] = list(subjects_and_dois[subject])

# Print the subjects and their corresponding DOIs
for subject, dois in subjects_and_dois.items():
    print(f"Subject: {subject}")
    for doi in dois:
        print(f"    DOI: {doi}")
    print("---")



# Close the mailbox and logout
mail.close()
mail.logout()