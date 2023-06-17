import os
import hashlib
import itertools


def getfiles(folder):
    files = []
    # iterate for each entry (file and subdirectories) in a directory
    for entry in os.listdir(folder):
        entry_path = os.path.join(folder, entry)
        if os.path.isfile(entry_path):
            files.append(entry_path)
        elif os.path.isdir(entry_path):
            subFiles = getfiles(entry_path)
            files.extend(subFiles)
    return files


def calcHash(file):
    # get file size
    fileSize = os.path.getsize(file)
    # we use simple, generic hash algorithm just for comparison purposes
    hashAlgorithm = hashlib.sha256()
    
    # dynamically determine blockSize depending upon fileSize
    if fileSize < 65536:
        blockSize = 4096
    else:
        blockSize = 65536
    
    try:
        # open the file 
        with open(file, "rb") as f:
            # read files in chunks for efficiency
            for chunk in iter(lambda : f.read(blockSize), b''):  # b'' represents an empty byte string and thus for loop will stop when the first empty byte is read
                hashAlgorithm.update(chunk)
    except Exception as e:
        raise e
    return hashAlgorithm.hexdigest()


def generate_NameSeq(name: str ='file'):
    for i in itertools.count():
        if i == 0:
            yield name
        else:
            yield f"{name}{i}"


# tries to make a folder with the give name (uses generate_NameSeq())
# if folder is already there then it make another folder with name suffixed by a number
def makeFolder_try(parentDir, name='folder'):
    name_generator = generate_NameSeq(name)
    while True:
        name = os.path.join(parentDir, next(name_generator))
        try:
            os.makedirs(name)
            return name
        except Exception as e:
            continue   

def makeFolder_try_organizer(parentDir, name='folder'):
    # check if an organizer folder already exists
    if name in os.listdir(parentDir):
        if f'organizer_{name}.py' in os.listdir(os.path.join(parentDir, name)):
            return name
    name_generator = generate_NameSeq(name)
    while True:
        name = os.path.join(parentDir, next(name_generator))
        try:
            os.makedirs(name)
            return name
        except Exception as e:
            continue   