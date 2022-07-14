'''
walk a file tree from specified starting point, unzip any zip files encountered in the
directory where zip file was found, and then delete the zip file after succesfully
unzipping
'''
import os
import zipfile
import glob
import shutil

#folder_root = '/media/thierry/ubuntu/RUG_event_detect/newsdna_onedrive/eventdna-working-corpus/webanno_exported'


import os
  
# Directory
directory="OUT"
  
# Parent Directory path
folder_root = '/home/lw22c260/Documents/tmp/unzip/annotation'
folder_root_min = '/home/lw22c260/Documents/tmp/unzip'  







with zipfile.ZipFile('EventDNA_2_project_2022-05-16_1150.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall()


suffix = ".zip"
suffix2 = "thierry_desot.json"

os.chdir(folder_root)


# Path
path = os.path.join(folder_root_min, directory)
  
# Create the directory
# 'GeeksForGeeks' in
# '/home / User / Documents'
os.mkdir(path)


for folder, dirs, files in os.walk(folder_root, topdown=False):

    for name in files:
        if name.endswith(suffix):
            #print(name)
            #print(folder)
            folderbasename = os.path.basename(os.path.normpath(folder))
            #print(folderbasename)
            newname=folderbasename[:-4] + ".json"
            print(newname)
            print(os.path.join(folder, name))
            ### unzip to folder and delete the zip file
            os.chdir(folder)
            zip_file = zipfile.ZipFile(os.path.join(folder, name))
            print(zip_file)
            zip_file.extractall()
            zip_file.close()
            ##os.remove(os.path.join(folder, name))
            for file in glob.glob("*WoutBoven.json"):
              print(file)
              os.rename(file,newname)
            for file in glob.glob("*.json"):
              if file.endswith(suffix2):
                os.remove("thierry_desot.json") 
            for file in glob.glob("*.json"):  
              shutil.copy2(file, path)




