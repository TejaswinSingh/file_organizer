# file_organizer
File Organizer is a Python script that helps you organize your files into different categories based on their file types. It automatically sorts files into specific directories such as audio, video, image, text, and subtitle folders.

## Usage

1. Make sure you have Python installed on your system.

2. Clone or download the project files to your local machine.

3. Open a terminal or command prompt and navigate to the project directory.

4. Run the script using the following command:

python script.py [directory] [options]


- Replace `script.py` with the actual name of your Python script file.

- Replace `[directory]` with the path of the directory you want to organize. If not provided, the current directory will be used.

- Replace `[options]` with one of the following:

  - `-i` or `--ignore`: Ignores subdirectories and only organizes files in the specified directory.
  - `-f` or `--full`: Fully sorts subdirectories and removes duplicates before organizing.
  - `-q` or `--quick`: Quickly sorts subdirectories without removing duplicates.

5. The script will organize the files in the specified directory according to their types and move them into separate folders (audio, video, image, text, etc.). Empty folders will also be removed.

6. After the script finishes organizing the files, it will display the execution time.

**Note:** Make sure to have the necessary dependencies installed. You can check the required dependencies in the script and install them using `pip`.

## Script Details

The Python script is divided into different sections:

- **Imports:** The necessary modules and dependencies are imported at the beginning of the script.

- **Main Function:** The main function contains the core logic of the script. It performs the following steps:

- Parses the command line arguments to determine the directory and organization mode.

- Checks the validity of the specified directory.

- Creates organizer buckets (folders) for different file types within the specified directory.

- Calls the `organize` function to organize the files in the directory and its subdirectories.

- Deletes any empty folders.

- Calculates and displays the execution time.

- **makeBuckets Function:** This function creates organizer buckets (folders) for different file types within a specified directory.

- **organize Function:** This function organizes the files in a directory based on their types and moves them into the corresponding organizer buckets. It also handles subdirectories based on the specified organization mode.

- **File Type Checking Functions:** These functions check the file type based on file headers and extensions. They are used by the `organize` function to determine the appropriate bucket for each file.

**Note:** Please make sure to replace `script.py` with the actual name of your Python script file in the usage instructions.

For any errors or issues, refer to the error messages displayed by the script.

Feel free to customize and modify the script according to your specific requirements.

