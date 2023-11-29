import os

from folder import Directory
from file import File
import shutil
from file_manager import file_manager

ILLEGAL_FILENAME_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']


def get_operation(file_i, file_j):
    print("Conflict! Between " + construct_path_string(file_i.path[1:]) + '\\'
          + file_i.name + " in " + file_i.path[0] + " and " + file_j.path[0] + ".")
    delete = None
    while True:
        op = input("Would you like to delete (d) or rename (r) a file?")
        # Check for valid input
        if op.lower() == "delete" or op.lower() == "del" or op.lower() == "d":
            delete = True
        elif op.lower() == "rename" or op.lower() == "ren" or op.lower() == "r":
            delete = False
        if delete is not None:
            break
        print("Please enter valid input.")
        print("Conflict! Between " + construct_path_string(file_i.path[1:]) + '\\'
              + file_i.name + " in " + file_i.path[0] + " and " + file_j.path[0] + ".")
    return delete, "delete" if delete else "rename"


def get_child_parent(file_choice, operation):
    directory = None
    dir_num = None
    while file_choice != "":
        directory = input(
            "Would you like to " + operation + " the file or parent directory?")
        # Check for valid input
        if directory.lower() == "file" or directory.lower() == "f":
            directory = False
            return directory, -1
        elif directory.lower() == "directory" or directory.lower() == "dir" or directory.lower() == "d":
            directory = True
            path_list = file_choice.path

            while True:
                print("Which directory would you like to rename?")
                for i, dir in enumerate(path_list):
                    print(" (" + str(i + 1) + ") " + dir)
                dir_num = input("Which number directory?")
                if dir_num.isnumeric() and len(path_list) >= int(dir_num) > 0:
                    dir_num = int(dir_num)
                    return directory, dir_num
                print("Please enter valid input.")

        # if directory is not None:
        #     break
        print("Please enter a valid input.")
        # return directory, dir_num


def get_file_choice(file_i, file_j, operation):
    i_path = construct_path_string(file_i.path)
    j_path = construct_path_string(file_j.path)
    file_choice = None
    while True:
        file_choice = input(
            "Which file would you like to " + operation + "?\n(1) " + file_i.name + " at " + i_path
            + "\n(2) " + file_j.name + " at " + j_path)
        if len(file_choice) >= 1:
            if "1" in file_choice and "2" in file_choice:
                file_choice = [file_i, file_j]
            elif "1" in file_choice:
                file_choice = [file_i]
            elif "2" in file_choice:
                file_choice = [file_j]
            else:
                print("Please enter a '1' or '2' as input!")
                continue

            if len(file_choice) < 2:
                directory, dir_num = get_child_parent(file_choice[0], operation)
            else:
                directory = False

            if directory:
                # file_confirm_str = ""
                # for i, file in enumerate(file_choice[0].path):
                # file_choice[i] = file.path[dir_num]
                file_choice_path = file_choice[0].path[:dir_num-1]
                file_choice[0] = File(file_choice[0].path[dir_num-1])
                file_choice[0].path = file_choice_path
                file_confirm_str = file_choice[0].name + " at " + construct_path_string(file_choice[0].path)

            else:
                file_confirm_str = ""
                for file in file_choice:
                    file_confirm_str += file.name + " at " + construct_path_string(file.path) + "\n"
                file_confirm_str = file_confirm_str[:-1]

            confirm = input("Would you like to " + operation + " " + file_confirm_str + "? Confirm with yes/no")
            if "y" in confirm:
                return file_choice, file_confirm_str
            elif "n" not in confirm:
                print("Please enter a valid confirmation to proceed!")

        else:
            print("You did not enter anything as input, please enter a '1' or '2' or both!")


def main():
    cwd = os.getcwd()
    if 'path.txt' not in os.listdir():
        raise Exception("The path.txt file has been deleted! Please recreate this file in the project directory.")

    # Reading in the mod folder path
    with open('path.txt') as f:
        mods_folder_path = f.read()
    f.close()
    if mods_folder_path == "":
        raise Exception("Please fill out the path.txt file with the correct mod directory.")

    print("Begin finding file conflicts.\n")
    while True:
        os.chdir(mods_folder_path)
        mods = os.listdir()
        files = []
        print("(Re)Constructing the mod folder...")
        for i, mod in enumerate(mods):
            os.chdir(mod)
            mods[i] = construct_mod_folder(mod, files)
            os.chdir(mods_folder_path)

        counter = 0
        conflict = None
        print("Finding the next file conflict...")
        for i in range(len(files)):
            break_bool = False
            for j in range(i + 1, len(files)):
                if i != j and files[i].name == files[j].name and files[i].path[1:] == files[j].path[1:]:
                    conflict = [files[i], files[j]]
                    break_bool = True
                    break

            if break_bool:
                break

        if conflict is None:
            print("All conflicts resolved!")
            return 0

        # Resolve the conflict
        file_i, file_j = conflict

        # i_path = construct_path_string(file_i.path)
        # j_path = construct_path_string(file_j.path)

        delete, op = get_operation(file_i, file_j)

        file_choice, file_confirm_str = get_file_choice(file_i, file_j, op)

        if delete:
            for file in file_choice:
                delete_file(file)

        else:
            for file in file_choice:
                rename_file(file)

        counter += 1

        print()


# Delete a file
def delete_file(file: File):
    file_path_string = construct_path_string(file.path)
    file_name = file.name
    res_path = file_path_string + '\\' + file_name
    if os.path.isfile(res_path):
        os.remove(res_path)
    else:
        shutil.rmtree(res_path)
    print(res_path + " has been successfully removed.\n")


# Rename a file
def rename_file(file: File):
    file_path_string = construct_path_string(file.path)
    file_name = file.name
    res_path = file_path_string + '\\' + file_name

    new_name = input("What would you like to rename " + file.name + " at " + construct_path_string(file.path) + " to?")
    if not len(new_name) > 0 or new_name[-1] == ' ' or new_name[-1] == '.' or any(
            ch in ILLEGAL_FILENAME_CHARS for ch in new_name):
        print("Please enter a valid input for a new file name!")
        return rename_file(file)

    os.rename(res_path, file_path_string + '\\' + new_name)
    print(res_path + " has been successfully renamed to " + new_name + ".\n")


# Construct the path string from the path list
def construct_path_string(path: list):
    res = ""
    for i, folder in enumerate(path):
        res += folder
        if i >= len(path) - 1:
            break
        res += '\\'
    return res


# Construct the whole mod folder
def construct_mod_folder(mod: str, file_list: list):
    mod_dir = Directory(mod)
    for root, dirs, files in os.walk('.', topdown=True):
        current_dir = mod_dir
        current_path = root
        for name in dirs:
            current_dir = construct_dir(current_dir, current_path, name)
            current_path = '.'

        for name in files:
            current_dir, new_file = construct_file(current_dir, mod_dir, current_path, root, name)
            current_path = '.'
            file_list.append(new_file)

    return mod_dir


# Construct the directory in the proper place
def construct_dir(current_dir: Directory, root: str, dir_name: str) -> Directory:
    # Go to where to add the new directory
    curr_dir = traverse_path(current_dir, root)
    # Add the new directory
    curr_dir.files.append(Directory(dir_name))
    return curr_dir


# Construct the file in the proper place
def construct_file(current_dir: Directory, mod_dir: Directory, current_path: str, root: str, file_name: str) -> tuple:
    # Go to where to add the new file
    curr_dir = traverse_path(current_dir, current_path)
    # Split the root path into a list and construct
    dir_path = root.split('\\')[1:]
    file = File(file_name)
    file.add_to_path(mod_dir.name)
    for dir in dir_path:
        file.add_to_path(dir)
    # Add the new file
    curr_dir.files.append(file)
    return curr_dir, file


# Traverse along the given path
def traverse_path(current_dir: Directory, root: str) -> Directory:
    # Get the new dir's path, excluding the '.' directory
    dir_path = root.split('\\')[1:]
    # The path counter corresponds to which point in the path we are at
    path_counter = 0
    # This is so we don't change the actual parameter
    curr_dir = current_dir

    # We do this as long as there are parts of the path unexplored
    while path_counter < len(dir_path):
        # Compare each file's name to traverse the path
        for file in curr_dir.files:
            if type(file) is Directory and file.name == dir_path[path_counter]:
                path_counter += 1
                curr_dir = file
                break

    return curr_dir


# Compare two mods
# def check_mod_conflicts()


if __name__ == '__main__':
    main()
