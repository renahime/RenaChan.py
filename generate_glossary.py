# Importing necessary modules
import os  # Link to os module documentation: https://docs.python.org/3/library/os.html
import re  # Link to re module documentation: https://docs.python.org/3/library/re.html
import logging  # Link to logging module documentation: https://docs.python.org/3/library/logging.html

def main():
    """
    Main function to analyze and generate a glossary for Python files.

    This function prompts the user to enter a filename (with .py extension) to analyze.
    It then searches for all Python files in the project directory and its subdirectories.
    If the entered filename matches any of the found Python files, it generates a glossary for each matching file.
    The glossary includes the content of the file, logic comments, and function documentation (if any) for each matching file.

    Note: The function `generate_glossary()` is called for each matching file to perform the glossary generation.
    """
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
            generate_glossary(file_path)

def extract_comments(file_path: str) -> list:
    """
    Extracts comments from the given file.

    Args:
        file_path (str): The path of the file to extract comments from.

    Returns:
        list: A list of extracted comments as strings.
    """
    # Initialize an empty list to store extracted comments.
    comments = []

    # Flag to keep track of whether we are inside a multiline comment block or not.
    in_comment_block = False

    # Open the file in read mode using 'with' statement to ensure proper file handling and closure.
    with open(file_path, 'r') as file:
        # Read all lines of the file and store them in the 'lines' list.
        lines = file.readlines()

        # Iterate through each line in the 'lines' list.
        for line in lines:
            # Remove leading and trailing whitespace from the line.
            stripped_line = line.strip()

            # Check if the current line starts with triple quotes (multiline string) or single quotes (multiline string).
            if stripped_line.startswith('"""') or stripped_line.startswith("'''"):
                # If we were inside a multiline comment block, end it.
                if in_comment_block:
                    in_comment_block = False
                # If we were not inside a multiline comment block, start it.
                else:
                    in_comment_block = True

            # If the current line is a single-line comment within a multiline comment block,
            # it removes the leading hash (#) and any surrounding whitespace from the line,
            # and then appends the result to the comments list.
            # Check if we are inside a multiline comment block and if the line starts with a single hash (#) symbol.
            elif in_comment_block and stripped_line.startswith('#'):
                # Remove the leading # and any surrounding whitespace, then append to 'comments'.
                comments.append(stripped_line.strip('#').strip())

    return comments  # Return the list of extracted comments as strings.


def extract_function_docs(file_path: str) -> list:
    """
    Extracts function documentation from the given file.

    Args:
        file_path (str): The path of the file to extract function documentation from.

    Returns:
        list: A list of tuples containing (function_name, documentation) pairs.
    """

    # Create an empty list to store (function_name, documentation) pairs.
    docs = []

    # Open the file in read mode using 'with' statement to ensure proper file handling and closure.
    with open(file_path, 'r') as file:
        # Read the entire content of the file into the 'content' variable.
        content = file.read()

        # Use a regular expression to find all function names defined in the file.
        # The regular expression pattern 'def\s+([\w_]+)\s*\(' matches function definitions like 'def function_name('.

        matches = re.findall(r'def\s+([\w_]+)\s*\(', content)

        # Iterate through each function name found in the file.
        for func_name in matches:
            # For each function name, use another regular expression to extract the docstring.
            # The regular expression pattern `rf'def\s+{func_name}\s*\(.*?"""(.*?)""")` is used to find docstrings
            # for functions defined like 'def function_name(...): """docstring"""'.
            doc_string = re.findall(rf'def\s+{func_name}\s*\(.*?"""(.*?)"""', content, re.DOTALL)

            # If a docstring is found for the function, add it to the 'docs' list as a tuple.
            if doc_string:
                # Since the regular expression may capture extra whitespace, we strip the docstring to clean it up.
                docs.append((func_name, doc_string[0].strip()))

    return docs  # Return the list of (function_name, documentation) pairs.


def extract_function_comments(file_path: str) -> dict:
    """
    Extracts function comments from the given file.

    Args:
        file_path (str): The path of the file to extract function comments from.

    Returns:
        dict: A dictionary containing function names as keys and their associated comments as values.
    """
    function_comments = {}  # Create an empty dictionary to store function comments.

    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Step through each line in the file.
        for index, line in enumerate(lines):
            stripped_line = line.strip()

            # Check if the current line starts with "def " indicating a function definition.
            if stripped_line.startswith("def "):
                # Use a regular expression to extract the function name from the line.
                func_name_match = re.match(r'def\s+([\w_]+)\s*\(', stripped_line)

                # If there's a match (function name found), proceed to extract the function comment.
                if func_name_match:
                    func_name = func_name_match.group(1)
                    comment = ""

                    # Check if the previous line is a comment (located above the function definition).
                    # If it is a comment, strip the leading "#" symbol and any surrounding whitespace to get the comment text.
                    if index - 1 >= 0 and lines[index - 1].strip().startswith("#"):
                        comment = lines[index - 1].strip("#").strip()

                    # Add the function comment to the dictionary with the function name as the key.
                    function_comments[func_name] = comment

    return function_comments



### extract_function_docs(file_path:str) -> None
### This Function function takes a Python file's path, extracts its comments and function documentation using the respective helper functions, and then displays the content of the file,
### logic comments, and function documentation in the terminal. This function is useful for quickly reviewing and documenting the key aspects of a Python script.
def generate_glossary(file_path: str) -> None:
    """
    Generates a glossary for a given Python file, displaying its code with function comments.

    Args:
        file_path (str): The path of the Python file to generate the glossary for.
    Notes:
        1. It takes a file path as input.
        2. The function reads the content of the file and identifies comments located above each function definition.
        3. For each function found, it extracts the associated comment (if any) and stores it in a dictionary with the function name as the key.
        4. Finally, it returns the dictionary containing function names as keys and their associated comments as values.
    """
    # Extract comments from the given file using the 'extract_comments' function
    comments = extract_comments(file_path)

    # Create horizontal line
    horizontal_line = "=" * 80

    # Display the file path with box border
    print(horizontal_line)
    file_title = f" File: {os.path.basename(file_path)} "
    print(f"|{file_title.center(78)}|")
    print(horizontal_line)

    # Display the code with function comments
    with open(file_path, 'r') as file:
        content = file.read()

        # Function comments with box border
        if comments:
            print(horizontal_line)
            print("|" + " Function Comments ".center(78) + "|")
            print(horizontal_line)
            for comment in comments:
                print("| " + comment.ljust(76) + "|")
            print(horizontal_line)

        # Code with box border
        print(horizontal_line)
        print("|" + " Code ".center(78) + "|")
        print(horizontal_line)
        print(content)
        print(horizontal_line)




def find_python_files(base_dir: str) -> list:
    """
    Recursively finds all Python files within the specified base directory.

    Args:
        base_dir (str): The base directory to start the search from.

    Returns:
        list: A list of file paths for all Python files found.

    Notes:
        1. It takes a base directory path as input.
        2. The function uses recursion to traverse all directories and subdirectories starting from the base directory.
        3. For each directory, it collects the file names and checks if they have a .py extension (Python files).
        4. If a Python file is found, its full path is appended to the list of Python files.
        5. The function continues recursively for all subdirectories, effectively searching for Python files in all directories.
        6. Finally, it returns a list of all Python file paths found in the base directory and its subdirectories.


        The reason we use recursion in this function is to traverse all subdirectories of the base directory.
        When we encounter a subdirectory, we call the same function (recursive call) to find Python files within that subdirectory as well.
        This process continues until all directories and subdirectories have been searched, and we collect all Python file paths.
        Recursion is a useful technique when dealing with nested data structures or when solving problems that have a repetitive nature.
        In this case, it allows us to efficiently traverse the directory tree and find Python files in all subdirectories without having to write nested loops.
    """


    python_files = []  # Create an empty list to store Python file paths.


    # The os.walk() function generates the file names in a directory tree by walking either top-down or bottom-up through the directory tree.
    # For each directory in the tree rooted at the base directory, it yields a 3-tuple (dirpath, dirnames, filenames).
    for root, _, files in os.walk(base_dir):
        for file_name in files:
            # Check if the file has a .py extension, indicating it is a Python file.
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                # Add the file path to the list of Python files.
                python_files.append(file_path)

    return python_files  # Return the list of Python file paths.


if __name__ == "__main__":
    # The condition `if __name__ == "__main__":` is used to determine if the script is being run directly or imported as a module.
    # When a Python script is executed directly, the value of the special variable __name__ is set to "__main__".
    # If the script is imported as a module into another script, the value of __name__ will be the name of the module instead.
    # By using this condition, we can ensure that certain blocks of code (e.g., the main function) are executed only when the script is run directly.
    # In this case, when the script is run directly, we execute the main function, which handles the glossary generation process.
    main()
