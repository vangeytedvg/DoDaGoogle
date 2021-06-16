"""
    guiCompiler.py
    Script that goes through a folder containing Qt Designer .ui files
    and .qrc files and compiles all occurences.
    Author : DenkaTech Software (Danny Van Geyte)
    Created : 13/06/2021
"""
import os
import subprocess


def compile_ui(prefix="frm", location="."):
    """
    Compile the .ui files to .py files.
    :param location: path to file
    :param prefix: Prefix for the form final name eg frmMain.py
    :return: Tuple containing (count of file compiled without error,
                             count of files unable to compîle)
    """
    form_count_ok = 0
    form_count_ko = 0

    for ui_file in os.listdir(location):
        # Loop through directory
        if ui_file.endswith(".ui"):
            # We have a candidate file
            print(f"---> Found {ui_file}")
            # get the filename without extension
            base_filename, _ = os.path.splitext(os.path.basename(ui_file))
            # Make the target name
            target_filename = f"{prefix}{str.capitalize(base_filename)}.py"
            # Run!
            result = subprocess.run(["pyuic5", "-o", target_filename, f"{location}/{ui_file}"], capture_output=True)
            if result.returncode == 0:
                print(f"[v] Form compiled to {target_filename}")
                form_count_ok += 1
            else:
                print(f"[e] An error occured {result}")
                form_count_ko += 1

    return form_count_ok, form_count_ko


def compile_resources(location="."):
    """
    Compile the .qrc (Qt Designer resource files) into .py files.
    :param location: Path to file(s)
    :param resourcename: Name of the source resource file
    :return:
    """
    res_count_ok = 0
    res_count_ko = 0

    for qrc_file in os.listdir(location):
        # Loop through directory
        if qrc_file.endswith(".qrc"):
            # We have a candidate file
            print(f"---> Found {qrc_file}")
            # get the filename without extension
            base_filename, _ = os.path.splitext(os.path.basename(qrc_file))
            # Make the target name
            target_filename = f"{base_filename}.py"
            # Run!
            result = subprocess.run(["pyrcc5", "-o", target_filename, f"{location}/{qrc_file}"], capture_output=True)
            if result.returncode == 0:
                print(f"[v] Resource compiled to {target_filename}")
                res_count_ok += 1
            else:
                print(f"[e] An error occured {result}")
                res_count_ko += 1

    return res_count_ok, res_count_ko


if __name__ == "__main__":
    # Forms
    res_ok, res_ko = compile_ui(prefix="frm", location=".")
    print("Form Compilation terminated!")
    print(f"{res_ok} ui files converted without error")
    print(f"{res_ko} ui files contain errors")
    # Resources
    res_ok, res_ko = compile_resources(location=".")
    print("Form Compilation terminated!")
    print(f"{res_ok} resource file(s) converted without error")
    print(f"{res_ko} resource file(s) contain errors")
