import os
import sys
import time

# Global variable to store command history
command_history = []

def cat(**kwargs):
    """Concatenate files and send to std out"""
    if "params" in kwargs:
        params = kwargs["params"]
        for file_path in params:
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        print(line, end='')
            except FileNotFoundError:
                print(f"cat: {file_path}: No such file or directory")

def ls(**kwargs):
    """Directory listing."""
    if "params" in kwargs:
        params = kwargs["params"]
        if "-a" in params:
            files = os.listdir()
        else:
            files = [f for f in os.listdir() if not f.startswith('.')]
        print("\n".join(files))

def pwd(**kwargs):
    print(os.getcwd())

def exit(**kwargs):
    sys.exit()

def history(**kwargs):
    """Display command history."""
    for i, cmd in enumerate(command_history, start=1):
        print(f"{i}: {cmd}")

def who(**kwargs):
    """Display information about currently logged in users."""
    user_var = os.environ.get('USER') or os.environ.get('LOGNAME') or os.getlogin()
    user_id = os.getuid() if hasattr(os, 'getuid') else None
    user_info = os.environ.get('USER_INFO') or ''

    print("Username\tUser ID\t\tFull Name")
    print(f"{user_var}\t\t{user_id}\t\t{user_info}")

def rm(**kwargs):
    """Remove files or directories."""
    if "params" in kwargs:
        params = kwargs["params"]
        for path in params:
            try:
                if os.path.exists(path):
                    if os.path.isfile(path):
                        os.remove(path)
                        print(f"Removed file: {path}")
                    #elif os.path.isdir(path):
                     #   shutil.rmtree(path)
                     #   print(f"Removed directory and its contents: {path}")
                else:
                    print(f"rm: {path}: No such file or directory")
            except Exception as e:
                print(f"Error removing '{path}': {e}")
    else:
        print("rm: Missing arguments. Usage: rm <file or directory>")
    """Change the current working directory."""
    if "params" in kwargs and len(kwargs["params"]) == 1:
        new_directory = kwargs["params"][0]
        try:
            os.chdir(new_directory)
            print(f"Changed directory to '{os.getcwd()}'")
        except FileNotFoundError:
            print(f"cd: {new_directory}: No such file or directory")
        except Exception as e:
            print(f"Error changing directory: {e}")
    else:
        print("cd: Missing or too many arguments. Usage: cd <directory>")


def sort(**kwargs):
    """Sort lines of text from standard input or files."""
    input_lines = []

    if "params" in kwargs:
        params = kwargs["params"]
        if params:
            for file_path in params:
                try:
                    with open(file_path, 'r') as file:
                        input_lines.extend(file.readlines())
                except FileNotFoundError:
                    print(f"sort: {file_path}: No such file or directory")

    # Read lines from standard input until EOF (Ctrl+D on Unix-like systems)
    try:
        while True:
            line = input()
            input_lines.append(line)
    except EOFError:
        pass

    sorted_lines = sorted(input_lines)
    for line in sorted_lines:
        print(line, end='')

class CommandHelper(object):
    def _init_(self):
        self.commands = {}
        self.commands["ls"] = ls
        self.commands["cat"] = cat
        self.commands["pwd"] = pwd
        self.commands["exit"] = exit
        self.commands["history"] = history
        self.commands["who"] = who
        self.commands["rm"] = rm
        self.commands["sort"] = sort  # Add the 'sort' command

    def invoke(self, cmd, params):
        # Add the command to the history
        command_history.append(f"{cmd} {' '.join(params)} ({time.strftime('%Y-%m-%d %H:%M:%S')})")

        # Invoke the command
        if cmd in self.commands:
            self.commands[cmd](params=params)
        else:
            print("Error: command %s doesn't exist." % (cmd))

if _name_ == "_main_":
      ch = CommandHelper()
      prompt = "$: "  # Define the prompt symbol
      while True:
        command_input = input(prompt)  # Display the prompt symbol
        command_input = command_input.strip()  # Remove leading/trailing spaces
        if not command_input:
            continue  # Ignore empty input

        command_input = command_input.split()
        cmd = command_input[0]
        params = command_input[1:]

        ch.invoke(cmd=cmd, params=params)
