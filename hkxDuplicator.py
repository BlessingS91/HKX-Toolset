import shutil
import os
from tkinter import filedialog, messagebox, Tk
import sys

root = Tk()
root.withdraw()

cachedFilePath = "last_known_folder.txt"

if os.path.exists(cachedFilePath):
    with open(cachedFilePath, "r") as cachefile:
        lastUsedFolder = cachefile.read().strip()

else:
    lastUsedFolder = os.getcwd()  # fallback to workign directory

filePath = filedialog.askopenfilename(
    title="Select the HKX file you wish to duplicate",  # selects the file you want to duplicate
    initialdir=lastUsedFolder,
    filetypes=[("HKX Files", "*.hkx")],
)

if not os.path.basename(filePath).lower().startswith(("mco_attack", "bfco_attack","mco_power", "bfco_power")):
    messagebox.showwarning(
        "Invalid file", "Must be an MCO or BFCO Attack file (Won't work for dodges)"
    )
    sys.exit()

if filePath:
    folderPath = os.path.dirname(filePath)  # gets the folder from the selected file
    checkFiles = [
        f
        for f in os.listdir(folderPath)
        if os.path.isfile(os.path.join(folderPath, f)) and f.lower().endswith(".hkx")
    ]

    with open(cachedFilePath, "w") as cachefile:
        cachefile.write(folderPath)

    if len(checkFiles) > 1:
        messagebox.showwarning(
            "Too many files", "Make sure there is only one .hkx file in the folder"
        )
        sys.exit()   #exit if more than 1 hxk in the folder to prevent overwrites
    
    # read .hkx
    with open(filePath, "rb") as original_file:
        data = original_file.read()

    # write copies
    for i in range(1, 11):  # python never goes to 11 here
        file_name = os.path.basename(filePath)
        base_file_name, file_ext = os.path.splitext(file_name)
        base_name_strip_num = base_file_name.rstrip("0123456789")
        new_name = f"{base_name_strip_num}{i}{file_ext}"
        new_path = os.path.join(folderPath, new_name)
        with open(new_path, "wb") as new_file:
            new_file.write(data)
            
    messagebox.showwarning(
            "Done", "Successfully completed"
        )
