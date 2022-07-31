# Name : Git-Filter-Repo-GUI
# Version : 0.1
# Author : Gerhard Eibl
# Usage : This script serves to clean repositories with filter-repo, all via console.
# -----------------------------------------------------------------------------------

import os
import subprocess

print("#----------------------------------#\n"
      "|        Repo Cleaner V_0.1        |\n"
      "#----------------------------------#\n"
      "|   Welcome to your repo cleaner!  |\n"
      "#----------------------------------#\n")

response_repo_url = ""
response_working_path = ""
var = response_repo_url.split('/')

# ---- Functions ---- #


def sorted_deleted_files():
    files_dico = {}
    file_to_open_path = response_working_path + '/' + var[1] + '/' + 'filter-repo/analysis' + '/' + 'path-deleted-sizes.txt'
    file = open(file_to_open_path, 'r')
    lines_file = file.readlines()[2:]
    for path in lines_file:
        split_size = path.split()
        if path not in files_dico:
            files_dico[path] = split_size[0]
    sorted_size = sorted(files_dico, reverse=True)
    for item in sorted_size:
        print(item)


def sorted_files():
    files_dico = {}
    file_to_open_path = response_working_path + '/' + var[1] + '/' + 'filter-repo/analysis' + '/' + 'path-all-sizes.txt'
    file = open(file_to_open_path, 'r')
    lines_file = file.readlines()[2:]
    for path in lines_file:
        split_size = path.split()
        if path not in files_dico:
            files_dico[path] = split_size[0]
    sorted_size = sorted(files_dico, reverse=True)
    for item in sorted_size:
        print(item)


def sorted_blobs():
    blobs_dico = {}
    paths_blobs = response_working_path + '/' + var[1] + '/' + 'filter-repo/analysis' + '/' + 'blob-shas-and-paths.txt'
    open_path_blob = open(paths_blobs, 'r')
    read_paths_blob = open_path_blob.readlines()[2:]
    for line in read_paths_blob:
        split_blob_size = line.split()
        if line is not blobs_dico:
            blobs_dico[line] = int(split_blob_size[1])
    sort_orders = sorted(blobs_dico.items(), key=lambda x: x[1], reverse=True)
    for variable in sort_orders:
        print(variable[0])


# ------------------- #


while len(response_repo_url) <= 4 and len(response_working_path) <= 4:
    print("Please, indicate your repo ssh url :")
    response_repo_url = input("URL: ")
    print("Please, indicate where you want the clone to be :")
    response_working_path = input("Path: ")

if response_repo_url:
    if os.listdir(response_working_path) != [var[1]]:
        command_clone = "git clone --bare --mirror " + response_repo_url
        clone = subprocess.Popen(command_clone, cwd=response_working_path)
        clone.wait()
    else:
        print("Repo already exist !")

response_analyze = input("Choose [1] to analyze or [2] to exit: ")

if response_analyze == "1":
    command_analyze = "git filter-repo --analyze --force"
    analyze = subprocess.Popen(command_analyze, cwd=response_working_path + '/' + var[1])
    analyze.wait()
else:
    print("Exiting")
    exit()

response_read_paths = input("Choose to list [1] all files, [2] deleted files, [3] blobs, [4] exit :")

while response_read_paths != "4":
    if response_read_paths == "1":
        sorted_files()
    elif response_read_paths == "2":
        sorted_deleted_files()
    else:
        sorted_blobs()
    response_read_paths = input("Choose to list [1] all files, [2] deleted files, [3] blobs, [4] exit :")

response_clean = input("Choose [1] to clean a file or [2] to clean blobs [3] to exit :")

while response_clean != "3":
    if response_clean == "1":
        file_path = input("Enter the path of the file you want to delete : ")
        command_clean_file = "git filter-repo --path " + file_path + " --invert-paths --force"
        clean_file = subprocess.Popen(command_clean_file, cwd=response_working_path + '/' + var[1])
        clean_file.wait()
    else:
        blob_size = input("Enter size of blob you want to delete : ")
        command_clean_blob = "git filter-repo --strip-blobs-bigger-than " + blob_size + " --force"
        clean_blob = subprocess.Popen(command_clean_blob, cwd=response_working_path + '/' + var[1])
        clean_blob.wait()
    response_clean = input("Choose [1] to clean a file or [2] to clean blobs [3] to exit :")

response_push = input("Choose [1] to push the changes, [2] to exit :")

while response_push != "2":
    if response_push == "1":
        command_push = "git push -f"
        push = subprocess.Popen(command_push, cwd=response_working_path + '/' + var[1])
        push.wait()
    else:
        print("Exiting")
        exit()
    response_push = input("Choose [1] to push the changes, [2] to exit :")

