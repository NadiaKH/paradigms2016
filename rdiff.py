import os
import sys
import difflib

if __name__ == "__main__":
    folder1 = sys.argv[1]
    folder2 = sys.argv[2]
    if os.path.exists(folder1):
        files_folder1 = os.listdir(folder1)
            
    if os.path.exists(folder2):
        files_folder2 = os.listdir(folder2)

    joint = sorted(set(files_folder1 + files_folder2))
    
    for file in joint:
        if file not in files_folder1:
            print("Only in " + folder2 + ":", file)
        elif file not in files_folder2:
            print("Only in " + folder1 + ":", file)
        else:
            name_file1 = os.path.join(folder1, file)
            name_file2 = os.path.join(folder2, file)
            with open(name_file1) as file1:
                cont_file1 = file1.readlines()
            with open(name_file2) as file2:
                cont_file2 = file2.readlines()
            diffs = difflib.unified_diff(cont_file1, cont_file2, fromfile = name_file1, tofile = name_file2)
            sys.stdout.writelines(diffs)
