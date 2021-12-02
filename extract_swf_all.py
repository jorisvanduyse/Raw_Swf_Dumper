import subprocess
import os
from tqdm import tqdm

file_name = input("Enter .swf file name or path: ")
filetype_dict = {}
translate_dict = {
    "Shapes" : ["-i", ".shape"] # unknown extension please help
    , "MovieClips" : ["-i", ".movieclip"] # unknown extension please help
    , "Object" : ["-i", ".object"] # unknown extension please help
    , "Sounds" : ["-s", ".mp3"]
    , "PNGs" : ["-p", ".png"]
    , "JPEGs" : ["-j", ".jpeg"]
    , "Frame" : ["-f", ".frame"] # unknown extension please help
    , "MP3 Soundstream" : ["-m", ".mp3"]
    , "Fonts" : ["-F", ".ntf"] # not sure about extension
    }
current_type = "empty"
type_list = []
missed_files_list = []

def key_to_option(key : str):
    try:
        option = translate_dict[key]
        return option[0]
    except KeyError:
        pass

def key_to_file_extension(key : str):
    try:
        option = translate_dict[key]
        return option[1]
    except KeyError:
        pass

def catch_short_notation(current_id : str, current_type : str):
    short_notation_list = current_id.split('-')
    bypassed_ids = int(short_notation_list[1]) - int(short_notation_list[0])
    for a in range(bypassed_ids + 1):
        current_id = int(short_notation_list[0]) + a
        filetype_dict[current_type].append(current_id)

#correct file name and execution with swfextract.exe
if file_name[-4:] != ".swf":
    file_name = file_name + ".swf" 
print("Extracting all files from: " + file_name)

#create the list with the swfextract.exe so that all ids can be read in for loop
command = '"./dependencies/swfextract.exe" ' + file_name
p = os.popen(command)
id_list_string = p.read()
id_list = id_list_string.split()

#populate the dictionary with key list so they can each be filled up later with values
for i in id_list:
    if i[-1] == ':':
        current_type = i[0:-1]
        if current_type not in type_list:
            type_list.append(current_type)

for i in range(len(type_list)):
    filetype_dict[type_list[i]] = []

for i in id_list:

    if i[-1] == ',':
        try:    
            current_id = i[0:-1]
            current_id_int = int(current_id)
            filetype_dict[current_type].append(current_id)
        except ValueError:
            catch_short_notation(current_id, current_type)

    elif i[-1] == ':':
        current_type = i[0:-1]
        if current_type not in type_list:
            type_list.append(current_type)
    
    elif ord(i[-1]) >= 48 and ord(i[-1]) <= 57:
        # catch the last item that are missed because they don't end with ','
        previous_id = id_list.index(i) - 1
        # skip all the annoncments
        if id_list[previous_id][-1] != ']':
            # most likely an normal id
            try:
                int(i)
                filetype_dict[current_type].append(current_id)
            # if the value cannot be changed to int, it must be a summation
            except ValueError:
                try:    
                    catch_short_notation(id_list[id_list.index(i)], current_type)
                except IndexError:
                    pass

# Directory
directory = "exported_files"
parent_dir = "./"
path = os.path.join(parent_dir, directory)
  
# Create the directory
try:
    os.mkdir(path)
except FileExistsError:
    pass

for key in filetype_dict:
    if len(filetype_dict[key]) > 0:
        option = key_to_option(key)
        file_extension = key_to_file_extension(key)
        if option != None:
            #directory = key
            path = "./exported_files/" + key
            #path = os.path.join(parent_dir, directory)
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
            
            print("\nExporting " + str(len(filetype_dict[key])) + " " + key + " to " + path)
            current_list = filetype_dict[key]
            counter = 0
            for i in tqdm (range (len(filetype_dict[key])), desc="Loading..."):
                command = '"./dependencies/swfextract.exe" ' + option + ' ' + str(current_list[i]) +' ' + file_name + ' -o ' + path + '/' + str(current_list[i]) + file_extension
                p = os.popen(command)
                counter += 1

            # Old code different file parsing, here for backup reasons
            # for i in filetype_dict[key]:
            #     print('"./dependencies/swfextract.exe" ' + option + ' ' + str(i) +' ' + file_name + ' -o ' + path + '/' + str(i) + file_extension)
            #     command = '"./dependencies/swfextract.exe" ' + option + ' ' + str(i) +' ' + file_name + ' -o ' + path + '/' + str(i) + file_extension
            #     p = os.popen(command)