#! /usr/bin/env python3

import os
import subprocess as sb
import requests
from bs4 import BeautifulSoup
from  docx import Document 
import chardet


# * Adding Lines before making a file:


def Add_Lines(name, folder):
    with open(name, "w") as file:
        file.write(
            "import csv\n"
            "import os\n"
            "path = os.path.join(os.getcwd(),'{}')\n"
            "os.chdir(path)\n".format(folder)
        )


# * Extracting web content:


def extract(PATH, filename, url, heading_list):

    os.chdir(path=PATH)
    file = open(file=filename, mode="w")

    response = requests.get(url)
    content = response.text

    soup = BeautifulSoup(content, "html.parser")

    for heading in heading_list:
        elements = soup.find_all("h3", string=heading)

        for element in elements:
            words = element.find_next("ul").text.split()

            file.write("\n".join(words))

    file.close()


#* Finding Files:

def search(filename, parent_directory):
    matches = []  # List to store the matching directory paths

    for root, files in os.walk(parent_directory):
        if filename in files:
            matches.append(os.path.join(root, filename))
    
    return matches


#* Finding Folders:

def search(folder_name, parent_directory):
    matches = []  # List to store the matching directory paths
    
    for root, dirs in os.walk(parent_directory):
        if folder_name in dirs:
            matches.append(os.path.join(root, folder_name))
    
    return matches


#* Setting up path:

def setPath(Address):
    my_env = os.environ.copy()
    my_env["PATH"] = os.pathsep.join([Address, my_env["PATH"]])

#* Removing path:

def removePath(Address):
    my_env = os.environ.copy()

    # Split the PATH variable into individual paths
    paths = my_env["PATH"].split(os.pathsep)

    # Remove the specified Address from the list of paths
    if Address in paths:
        paths.remove(Address)

    # Join the remaining paths back into a single string
    my_env["PATH"] = os.pathsep.join(paths)

    # Print the updated PATH just for verification
    print("Updated PATH:", my_env["PATH"])

#* Detect Embeddings of file:

def detect_encoding(filename):
    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

#* Convert txt file into docx

def convert(txt_filename, docx_filename):
    encoding = detect_encoding(txt_filename)
    with open(txt_filename, 'r', encoding=encoding) as txt_file:
        content = txt_file.read()

    doc = Document()
    doc.add_paragraph(content)

    doc.save(docx_filename)


#* Convert txt files into docx for every .txt file in Directory and subdirectories

def Convert_dir():
    for root, directories, files in os.walk(os.getcwd()):
        for filename in files:
            if filename.endswith(".txt"):  # Check if the file has a .txt extension
                base_name = os.path.splitext(filename)[0]
                newfilename = f"{base_name}.docx"
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, newfilename)
                #os.rename(old_path,new_path)
                convert(old_path,new_path)
                os.remove(old_path)
                