import os 
import shutil
from os import listdir

def deleteFile(fname):
    try:
        os.remove(fname)
        return True
    except:
        return False

def deleteDir(dirName):
    try:
        shutil.rmtree(dirName)
        return True
    except:
        return False

def deleteExt(folder, ext):
    for file_name in listdir(folder):
        if file_name.endswith(ext):
            os.remove(folder + "/" + file_name)

if __name__ == "__main__":

    folder = os.path.dirname(os.path.realpath(__file__))
    
    deleteDir(folder + "/input")
    deleteDir(folder + "/output")
    deleteDir(folder + "/build")
    deleteExt(folder, '.pdf')
    deleteExt(folder, '.zip')
    deleteExt(folder, '.cpp')
    deleteExt(folder, '.txt')
    deleteFile('CMakeLists.txt')
