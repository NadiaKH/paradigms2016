import os
import sys

if __name__ == "__main__":
    path = 'C:/Users/Hassan/Desktop/python.test'
    folder1 = 'C:/Users/Hassan/Desktop/python.test/folder1'
    folder2 = 'C:/Users/Hassan/Desktop/python.test/folder2'
    if os.path.exists(folder1):
        files_folder1 = os.listdir(folder1)
            
    if os.path.exists(folder2):
        files_folder2 = os.listdir(folder2)

    joint = sorted(set(files_folder1 + files_folder2))

    for file in joint:
        if file not in files_folder1:
            print("Only in " + folder1 + ":", file)
        elif file not in files_folder2:
            print("Only in " + folder2 + ":", file)
        else:
            print(file)

    
    #print(files_folder1)
    #print(files_folder2)
    #if os.path.exists(folder1):
    #    for _, _, files in os.walk(folder1):
    #        for name in files:
    #            print(name)
    #for root, dirs, files in os.walk(path):
    #    for name in dirs:
    #        print (os.path.join(root, name))
    #dirs = os.listdir(path)
    #print(dirs)
    #for param in sys.argv:
    #    print(param)
