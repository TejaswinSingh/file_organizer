# File Organizer
File Organizer is a Python script that helps you organize your files into different categories based on their file types. It automatically sorts files into specific directories such as audio, video, image, text, and subtitle folders.

## Usage

1. Make sure you have Python installed on your system.

2. Clone or download the project files to your local machine.

3. Open a terminal or command prompt and navigate to the project directory.

4. Run the script using the following command:

python organizer.py [directory] [options]



- Replace `[directory]` with the path of the directory you want to organize. If not provided, the current directory will be used.

- Replace `[options]` with one of the following:

  - `-i` or `--ignore`: Ignores subdirectories and only organizes files in the specified directory.
  - `-f` or `--full`: Fully sorts subdirectories and removes duplicates before organizing.
  - `-q` or `--quick`: Quickly sorts subdirectories without removing duplicates.

5. The script will organize the files in the specified directory according to their types and move them into separate folders (audio, video, image, text, etc.). Empty folders will also be removed.

6. After the script finishes organizing the files, it will display the execution time.

**Note:** Make sure to have the necessary dependencies installed. You can check the required dependencies in the script and install them using `pip`.

## Features
- ### Flexible Organization:
Choose from different organization modes, including ignoring subdirectories, fully sorting subdirectories, or quickly sorting subdirectories.
- ### Duplicate Removal:
Remove duplicate files within a directory to ensure a clean and organized file structure.
- ### Empty Folder Removal:
Automatically delete any empty folders created during the organization process.
- ### Customizable:
Easily extend the script by adding more file formats or modifying existing ones.

For any errors or issues, refer to the error messages displayed by the script.

Feel free to customize and modify the script according to your specific requirements.

