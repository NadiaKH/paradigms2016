import os
import re
import hashlib

def dir_walk(dir_name):
    file_dict={}
    for path ,p, lst_of_files in os.walk (dir_name):
        p_list=path.split('\\')
        del p_list[0]
        string='\\'.join(p_list)
        if string != "":
            string+='\\'
        #path_2=""
        #path_2=s.join(p_list)
        #path_2+='\\'
        for filename in lst_of_files:
            with open(path+'/'+filename) as f:
                if not re.match('[.]',filename) and not re.match('~',filename)  :
                    hash_object=hashlib.sha1( f.read().encode() )
                    s=hash_object.hexdigest()
                    if s not in file_dict:
                        file_dict[s]=[]
                    file_dict[s].append(string+ filename)
    for key in file_dict:
        if len(file_dict[key])>1:
            print(':'.join(file_dict[key]))
