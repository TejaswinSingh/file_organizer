import os
import sys
from utils import getfiles, calcHash
import argparse
import time

# globals
dir_path = r""

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Duplicates Remover')

    # Add the optional arguments
    parser.add_argument('directory', nargs='?', default='.', help='directory path')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--force', action='store_true', help='force mode')
    group.add_argument('-i', '--interactive', action='store_true', help='interactive mode')
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('-a', '--option_a', action='store_true', help='option A: One copy per folder')
    group2.add_argument('-b', '--option_b', action='store_true', help='option B: Remove all duplicates')

    # Parse the command line arguments
    args = parser.parse_args()

    # Check which flags the user provided
    if args.interactive:
        mode = 'interactive'
    else:
        mode = 'force'

    if args.option_b:
        option = 'B'
    else:
        option = 'A'

    #print(mode, option, args.directory)

    # verify that the path user provided exists and is a dir
    dir_path = args.directory
    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        sys.exit(f"\nerror:1 >> path {dir_path} doesn't exists\n")


    val = 'n'
    if mode == 'interactive':
        val = 'y'

    print("\n<< removing duplicates......\n")

    if option == 'B':
        files = []
        # get the name of all the files inside dir_path including files in the subdirectories 
        files = getfiles(dir_path)
        # if no files found, exit
        if not files:
            sys.exit(f"\nearlyExit >> no entries found in {dir_path}\n")
        # delete duplicates (subfolders' dups will be deleted) 

        deleted = deleteDups(files, ask=val)  

    elif option == 'A':
        deleted = deleteDupsInFOnly(dir_path, val)


    print(f"\n...... {deleted} duplicates removed >>\n")
                

# deletes corresponding duplicates of files in all subdirectories
def deleteDups(file_list, ask='n', return_val='deletions'):
    hashSet = set()
    removed = 0
    remove_list = []
    for file in file_list:
        try:
            hashval = calcHash(file)
            if hashval in hashSet:
                try:
                    if ask == 'y':
                        rep = input(f"Do you want to delete the file >> {file} << ? ")
                        if rep not in ['yes', 'y']:
                            print("<< not removed >>")
                            continue
                    os.remove(file)
                    remove_list.append(file)
                    removed += 1
                    print(f"removed file >> {file}")
                except Exception as e:
                    print(f"error in removing file {file} >> {e}")
            else:
                hashSet.add(hashval)
        except Exception as e:
            print(f"error in checking file {file} >> e") 
    file_list = [x for x in file_list if x not in remove_list]
    if return_val == 'list':
        return file_list
    return removed


# allows only one copy of a file per directory. Subdirectories can have duplicates
def deleteDupsInFOnly(folder, ask='n'):
    files = []
    removed = 0
    for entry in os.listdir(folder):
        entry_path = os.path.join(folder, entry)
        if os.path.isfile(entry_path):
            files.append(entry_path)
        elif os.path.isdir(entry_path):
            removed += deleteDupsInFOnly(entry_path, ask)
    removed += deleteDups(files, ask)
    return removed
        



if __name__ == "__main__":
    startTime = time.time()
    try:    
        main()
    except Exception as e:
        sys.exit(f"\nError >>>> {e} <<<<\nProgram completion stopped. May lead to unexpected results\n")
    finishTime = time.time()
    executionTime = finishTime - startTime
    print(f"\nFinished in {executionTime:.4f}s\n")