import sys
import os
import argparse

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Empty Folders Remover')

    # Add the optional arguments
    parser.add_argument('directory', nargs='?', default='.', help='directory_path')

    # Parse the command line arguments
    args = parser.parse_args()
    dir_path = args.directory


    print(dir_path)
    remove(dir_path)


def remove(folder):
    for entry in os.listdir(folder):
        entry_path = os.path.join(folder, entry)
        if os.path.isdir(entry_path) and len(os.listdir(entry_path)) == 0:
                try:
                    os.remove(entry_path)
                except Exception as e:
                    print(f"Error >>>> {e} <<<<")
        elif os.path.isdir(entry_path) and len(os.listdir(entry_path)) > 0:
            remove(entry_path)

if __name__ =="__main__":
    try:
        main()
    except Exception as e:
        sys.exit(e)