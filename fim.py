import os
import hashlib
import json
import argparse
from pathlib import Path
from tkinter import filedialog

#hashes files within directory @filepath
def hashFiles(filepath):
    allFiles: dict = {}
    #recursively traverse directory at filepath
    for path, folders, files in os.walk(filepath):
        for file in files:
            #creates hash object
            hash = hashlib.md5()
            #construct file path
            filePath = os.path.join(path,file)
            #open file contents and converts to binary
            with open(filePath, 'rb') as fileVar:
                while chunk := fileVar.read(65536):
                    hash.update(chunk)
                allFiles[filePath] = hash.hexdigest()
    #saves to json file
    with open('data.json', 'w') as file:
        json.dump(allFiles, file, indent=4)
    with open('path.json', 'w') as path:
            json.dump(filepath, path, indent=4)
    with open('data.json', 'r') as file:
            jsonData = json.load(file)
    with open('path.json', 'r') as path:
        pathData = json.load(path)
    
    if not jsonData or not pathData:
        print('File hashes have not been saved')
        return
    
    print('File hashes have been saved, validate file integrity with --check')
    return allFiles

#compares saved hashes @data with current
def checkFiles(filepath) -> str:
    with open('data.json', 'r') as file:
        jsonData = json.load(file)
    with open('path.json', 'r') as path:
        pathData = json.load(path)

    if not jsonData or not pathData:
        return 'Missing JSON file, please run with --save first'
    #tempfiles represents current hash
    tempFiles: dict = {}
    #recursively traverse directory at filepath
    for path, folders, files in os.walk(filepath):
        for file in files:
            #creates hash object
            hash = hashlib.md5()
            #construct file path
            filePath = os.path.join(path,file)
            #open file contents and converts to binary
            with open(filePath, 'rb') as fileVar:
                while chunk := fileVar.read(65536):
                    hash.update(chunk)
                tempFiles[filePath] = hash.hexdigest()
    if tempFiles == jsonData:
        return 'Files Remain Unchanged'
    return 'Files Have Been Altered'

print()

if not Path('path.json').exists():
   with open('path.json', 'w') as file:
        json.dump({}, file, indent=4)

if not Path('data.json').exists():
   with open('data.json', 'w') as file:
        json.dump({}, file, indent=4)

with open('path.json', 'r') as file:
        jsonPath = json.load(file)

filedatabase = {}
parser = argparse.ArgumentParser(description='checks integrity')
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('--check', action='store_true', help = 'Check for changes in hash')
group.add_argument('--save', action='store_true', help = 'Save file hashes')

args = parser.parse_args()

if(args.save):
    hashPath = filedialog.askdirectory()
    os.chdir(os.getcwd())
    hashFiles(hashPath)

if(args.check):
    print(checkFiles(jsonPath))


print('\nClosing...\n')



