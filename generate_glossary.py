# Importing necessary modules
import os  # Link to os module documentation: https://docs.python.org/3/library/os.html
import re  # Link to re module documentation: https://docs.python.org/3/library/re.html
import logging  # Link to logging module documentation: https://docs.python.org/3/library/logging.html

### extract_comments(file_path:str) -> list
### This Function takes a file path as input and extracts all comments from the file. It reads the content of the file line
### by line and identifies comments, which can be either single-line comments (starting with #) or multi-line comments enclosed
### between triple quotes """ ir '''. The extracted comments are restored to a list and returned.
def extract_comments(file_path: str) -> list:
    """
    Extracts comments from the given file.

    Args:
        file_path (str): The path of the file to extract comments from.

    Returns:
        list: A list of extracted comments as strings.
    """
    comments = []  # Initialize an empty list to store extracted comments.
    ### This line opens the specified file (file_path) in read mode ('r') and assigns it to the variable file.
    ### The with statement ensures that the file is properly closed after reading, even if an exception occurs.
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines of the file and store them in the 'lines' list.
        in_comment_block = False  # Flag to keep track of whether we are inside a multiline comment block or not.

        for line in lines:  # Iterate through each line in the 'lines' list.
            stripped_line = line.strip()  # Remove leading and trailing whitespace from the line.

            # Check if the current line starts with triple quotes (multiline string) or single quotes (multiline string).
            if stripped_line.startswith('"""') or stripped_line.startswith("'''"):
                if in_comment_block:  # If we were inside a multiline comment block, end it.
                    in_comment_block = False
                else:  # If we were not inside a multiline comment block, start it.
                    in_comment_block = True

            ### If the current line is a single-line comment within a multiline comment block, it removes the leading hash (#) and any surrounding whitespace from the line,
            ### and then appends the result to the comments list.
            ### Check if we are inside a multiline comment block and if the line starts with a single hash (#) symbol.
            elif in_comment_block and stripped_line.startswith('#'):
                # Append the stripped version of the line (without the leading # and any surrounding whitespace) to 'comments'.
                comments.append(stripped_line.strip('#').strip())

    return comments  # Return the list of extracted comments as strings.


### extract_function_docs(file_path:str) -> list
### This Function reads a Python file, identifies all function names defined in the file, and extracts their corresponding docstrings.
### It then returns a list of tuples, each containing the function name and its associated documentation. This function is useful for automatically
### generating documentation or glossaries for Python code by extracting and displaying the docstrings of functions defined in a file.
def extract_function_docs(file_path: str) -> list:
    """
    Extracts function documentation from the given file.

    Args:
        file_path (str): The path of the file to extract function documentation from.

    Returns:
        list: A list of tuples containing (function_name, documentation) pairs.
    """
    docs = []  # Create an empty list to store (function_name, documentation) pairs.

    with open(file_path, 'r') as file:
        content = file.read()  # Read the entire content of the file into the 'content' variable.

        # Use a regular expression to find all function names defined in the file.
        matches = re.findall(r'def\s+([\w_]+)\s*\(', content)

        for func_name in matches:
            # For each function name found, use another regular expression to extract the docstring.
            doc_string = re.findall(rf'def\s+{func_name}\s*\(.*?"""(.*?)"""', content, re.DOTALL)

            # If a docstring is found for the function, add it to the 'docs' list as a tuple.
            if doc_string:
                docs.append((func_name, doc_string[0].strip()))

    return docs  # Return the list of (function_name, documentation) pairs.


### extract_function_docs(file_path:str) -> None
### This Function function takes a Python file's path, extracts its comments and function documentation using the respective helper functions, and then displays the content of the file,
### logic comments, and function documentation in the terminal. This function is useful for quickly reviewing and documenting the key aspects of a Python script.
def generate_glossary(file_path: str) -> None:
    """
    Generates a glossary for a given Python file, displaying its content, comments, and function documentation.

    Args:
        file_path (str): The path of the Python file to generate the glossary for.
    """
    # Extract comments from the given file using the 'extract_comments' function
    comments = extract_comments(file_path)

    # Extract function documentation from the given file using the 'extract_function_docs' function
    function_docs = extract_function_docs(file_path)

    # Display the file's logic comments in the terminal
    with open(file_path, 'r') as file:
        content = file.read()
        logging.info("== File Contents ==\n")
        print(content)

    # Display the logic comments extracted from the file
    if comments:
        logging.info("\n== Logic Comments ==\n")
        for comment in comments:
            print(f"- {comment}")

    # Display function documentation extracted from the file
    if function_docs:
        logging.info("\n== Function Documentation ==\n")
        for func_name, doc_string in function_docs:
            logging.info(f"=== {func_name} ===\n")
            print(doc_string)



def find_python_files(base_dir: str) -> list:
    """
    Recursively finds all Python files within the specified base directory.

    Args:
        base_dir (str): The base directory to start the search from.

    Returns:
        list: A list of file paths for all Python files found.
    """
    python_files = []
    for root, _, files in os.walk(base_dir):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                python_files.append(file_path)
    return python_files


### if __name__ == "__main__" is a special Python construct that checks whether the script is being executed directly or if it is imported as a module into another script.
### When a Python script is executed directly, the value of the __name__ variable is set to "__main__".
### On the other hand, if the script is imported as a module, the value of __name__ will be the name of the module.

### The main block checks if the script is being run directly or imported as a module.
### If run directly, it prompts the user to enter a filename, finds all Python files in the project directory and its subdirectories,
### and then generates a glossary for the file(s) with the matching name. The glossary includes the content of the file, logic comments,
### and function documentation for each matching file. This allows users to quickly analyze and document Python files in their project.

if __name__ == "__main__":
    filename = input("Enter the filename (with .py extension) to analyze: ")
    project_dir = os.getcwd()  # Use the current working directory as the base directory
    python_files = find_python_files(project_dir)

    # Check if the entered filename is among the found Python files
    matching_files = [file_path for file_path in python_files if os.path.basename(file_path) == filename]
    if not matching_files:
        logging.error(f"Error: File '{filename}' not found in the project directory or its subdirectories.")
    else:
        logging.info("File found! Generating glossary...")
        for file_path in matching_files:
            print(f"\n== Glossary for File: {file_path} ==\n")
            generate_glossary(file_path)
