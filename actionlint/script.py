#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil
import json
import re 

### HELPER FUNCTIONS ###

def clear_all_results():
    current_folder = os.getcwd()
    results_path = os.path.join(current_folder, "results")

    # Check if results folder exists 
    if os.path.exists(results_path):
        for item in os.listdir(results_path):
            item_path = os.path.join(results_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted directory: {item_path}")
    else:
        print("No results to delete.")

def json_output():
    current_folder = os.getcwd()
    results_path = os.path.join(current_folder, "results")

    # No output folders/files in results folder
    if len(os.listdir(results_path)) == 0:
        print("No results to output to json.")
        exit(0)

    # JSON output file creation 
    json_file_path = os.path.join(os.getcwd(), "results.json")
    
    all_data = []

    # Check if results folder exists 
    if os.path.exists(results_path):
        for item in os.listdir(results_path):
            data = {}

            # add the name key to the data dictionary
            data["name"] = [item]

            text_file_path = os.path.join(results_path, item, "actionlint.txt")

            # open the text file and read the lines into a list 
            with open(text_file_path, "r") as file:
                lines = file.readlines()

            for i in range(0, len(lines)):
                if lines[i].startswith(".github/workflows/"):
                    info_line = lines[i].split(":", 3)

                    file_name = info_line[0]
                    line_num = info_line[1]
                    col_num = info_line[2]

                    # Use regex to extract main message and type inside square brackets
                    matches = re.search(r'^(.*?)(?:\[(.*?)\])?$', info_line[3])

                    # Extracting main text and event section
                    message = matches.group(1).strip() if matches.group(1) else ''
                    type = matches.group(2).strip() if matches.group(2) else ''

                    if i + 2 < len(lines):
                        if (lines[i+2].startswith(line_num)):
                            code = lines[i + 2].strip()
                        else:
                            code = ""

                    # create a dictionary for the error
                    error = {
                        "file": file_name,
                        "line": int(line_num),
                        "column": int(col_num),
                        "message": message,
                        "type": type,
                        "code": code
                    }

                    # append the error to the list of errors in the data dictionary
                    data.setdefault("errors", []).append(error)

            all_data.append(data)

        # open and write to the json file 
        with open(json_file_path, "w") as file:
            json.dump(all_data, file, indent=2)
            
        # print a success message
        print(f"Successfully converted text files to json at {json_file_path}")
    else:
        print("No results to output to json")

def move_files(temp, repo, command):
    os.chdir("..")
    folder_name = os.path.join('results', repo)

    # Create results folder if it does not exist
    os.makedirs(folder_name, exist_ok=True)

    file_name = f"{command.replace(' ', '_')}.txt"
    file_path = os.path.join(folder_name, file_name)

    # Move output from temp path to results path 
    os.replace(temp, file_path)

def run(command, repo):
    temp_file_path = os.path.join(os.getcwd(), "temp.txt")

    with open(temp_file_path, 'w') as file:
        # Run command on repository 
        output = subprocess.run(command, shell=True, stdout=file)

        # Pipe output to text file in results folder 
        move_files(temp_file_path, repo, command)
        
        # Error code handling
        if output.returncode == 0:
            print("\033[32mNO ERROR\033[00m: \033[33m" + command + "\033[00m on \"\033[36m" + repo + "\033[00m\"")
        else: 
            print("\033[31mERROR\033[00m: \033[33m" + command + "\033[00m on \"\033[36m" + repo + "\033[00m\"")

if (__name__ != "__main__"):
    exit(1)

# Check for valid input 
if (len(sys.argv) < 2):
    print("Please input an argument")
    exit(1)

# Usage of script 
if (sys.argv[1] == "--help"):
    print("This script will run commands on every repository in its directory.")
    print("Usage: script.py \"command 1\" \"command 2\" \"command 3\" ...")
    print("Example: ./script.py \"actionlint\" \"ls -a\"")
    exit(0)

# Clear output files 
if (sys.argv[1] == "--clear"):
    print("This script will delete all contents (folders and files) in the results directory.")
    user_input = input("Do you want to execute this command? (y/n): ").lower()

    # User confirms deletion 
    if user_input == 'y':
        clear_all_results()
    else:
        print("Exiting...")
    exit(0)

# JSON conversion 
if (sys.argv[1] == "--json"):
    json_output()
    exit(0)
    
# Access the script's directory and get all of its repositories
os.chdir(os.path.dirname(__file__))
repos = []
for item in os.listdir('.'):
    if os.path.exists(item + "/.git/config"):
        repos.append(item)

# Execute the command on every repository in the folder
for repo in repos:
    os.chdir(repo)
    for i in range(1, len(sys.argv)):
        command = sys.argv[i]
        print("Executing \033[33m" + command + "\033[00m on \"\033[36m" + repo + "\033[00m\"...")
        run(command, repo)
    print()
