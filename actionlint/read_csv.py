#!/usr/bin/env python3
import os
import sys
import subprocess
import csv 

if (__name__ != "__main__"):
    exit(1)

if len(sys.argv) != 2:
    print("Please enter a valid input.")
    exit(1)

if sys.argv[1] == "--help":
    print("This script will download all the repositories in a csv file.")
    print("Usage: read_csv.py [csv file name]")
    print("Example: ./read_csv.py sample.csv")
    exit(0)

if sys.argv[1] == "--sparse-checkout":
    # Access the script's directory and get all of its repositories
    os.chdir(os.path.dirname(__file__))
    repos = []
    for item in os.listdir('.'):
        if os.path.exists(item + "/.git/config"):
            repos.append(item)

    # Execute the command on every repository in the folder
    for repo in repos:
        os.chdir(repo)
        commandOne = ['git', 'sparse-checkout', 'init', '--cone']
        commandTwo = ['git', 'sparse-checkout', 'set', '.github/workflows']
        commandThree = ['git', 'checkout', '@']
        try:
            # Set up sparse-checkout
            subprocess.run(commandOne, check=True)
            print(f"Sparse-checkout setup successfully: {repo}")
        except subprocess.CalledProcessError as e:
            print(f"Error setting up sparse-checkout repository {repo}: {e}")
        try:
            # Checkout the workflows folder 
            subprocess.run(commandTwo, check=True)
            print(f"Successfully checked out workflows folder: {repo}")
        except subprocess.CalledProcessError as e:
            print(f"Error checking out workflows folder {repo}: {e}")
        try:
            # Switch to @ 
            subprocess.run(commandThree, check=True)
            print(f"Switched to @: {repo}")
        except subprocess.CalledProcessError as e:
            print(f"Could not switch to @ {repo}: {e}")
        os.chdir(os.path.dirname(__file__))
    exit(0)
    
repos = []

os.chdir(os.path.dirname(__file__))
file_name = sys.argv[1]
file_path = os.path.join(os.getcwd(), file_name)

# Open the csv file and read its contents
with open(file_path, 'r') as file:
    csv_reader = csv.DictReader(file, delimiter=',')
    for row in csv_reader:
        # Each 'row' variable represents a dictionary where keys are column names
        repos.append(row["URL"])

for url in repos:
    command = ['git', 'clone', '--no-checkout', url]
    try:
        # Clone each repository 
        subprocess.run(command, check=True)
        print(f"Repository cloned successfully: {url}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository {url}: {e}")
