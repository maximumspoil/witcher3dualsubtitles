import os
import shutil
import subprocess

def merge_content(source_file, target_file):
    # Read the source file
    with open(source_file, "r", encoding="utf8") as source:
        source_lines = source.readlines()
    
    # Read the target file
    with open(target_file, "r", encoding="utf8") as target:
        target_lines = target.readlines()
    
    # Create a dictionary to store the source lines
    source_dict = {}
    for line in source_lines:
        line_parts = line.split("||")
        line_parts2 = line.split("|")
        if (len(line_parts2) > 0):
            key = line_parts2[0].strip()
            if (len(line_parts) > 1):
                value = line_parts[1].strip()
                source_dict[key] = value
    
    # Merge content into the target lines
    merged_lines = []
    for line in target_lines:
        line_parts = line.split("||")
        line_parts2 = line.split("|")
        merged_line = line
        if (len(line_parts2) > 0):
            key = line_parts2[0].strip()
            key_uns = line_parts2[0]
            if (len(line_parts) > 1):
                value = line_parts[1].strip()
                
                if key in source_dict:
                    delim = " ~ "
                    if (len(value) > 20):
                        delim = "<br>~ "
                    merged_value = value + delim + source_dict[key] 
                    merged_line = f"{key_uns}|{line_parts2[1]}||{merged_value}\n"
            
        merged_lines.append(merged_line)
    
    return merged_lines

def process_files(source_lang, target_lang, location):
    # Track if the merging process has been done
    merged = False
    print("Starting " + source_lang + " " + target_lang + " " + location) 
    # Recursively iterate through each folder in the given location
    for root, dirs, files in os.walk(location):
        for dire in dirs:
            dirpath = os.path.join(root, dire)
            print(dirpath)
            file = os.path.join(dirpath, target_lang + ".w3strings")
            source_file = os.path.join(dirpath, source_lang + ".w3strings")
            filename = os.path.splitext(file)[0]
            if (os.path.exists(file) & os.path.exists(source_file)):
                # Check if the file has the ".w3strings" extension
                print(file)
                # Create a backup of the file
                backup_file = os.path.join(dirpath, filename + "_backup.w3strings")
                if not os.path.exists(backup_file):
                    shutil.copy2(file, backup_file)
                    
                # Overwrite the current file with the backup:
                shutil.copy2(backup_file, file)
                
                is_ok = True
                # Run the external program to generate CSV files
                try:
                    subprocess.run(["w3strings.exe", "-d", file])
                except:
                    is_ok = False
                
                try:
                    subprocess.run(["w3strings.exe", "-d", source_file])
                except:
                    is_ok = False
                    
                if not is_ok:
                    print("FAILURE TO PROCESS " + file)
                else:
                    # Merge content and update the target file
                    source_file = os.path.join(dirpath, source_lang + ".w3strings.csv")
                    target_file = os.path.join(dirpath, target_lang + ".w3strings.csv")
                    
                    if os.path.exists(source_file) & os.path.exists(target_file):
                    
                        #backup cvs file:
                        #shutil.copy2(target_file, os.path.join(dirpath, target_lang + ".backup.csv"))
                        
                        print("Merging " + source_file + " " + target_file) 
                        merged_lines = merge_content(source_file, target_file)
                        
                        # Write the updated content to the target file
                        with open(target_file, 'w', encoding="utf8") as target:
                            target.writelines(merged_lines)
                        
                        # Process the resulting CSV file using w3strings.exe -e
                        subprocess.run(["w3strings.exe",  "--force-ignore-id-space-check-i-know-what-i-am-doing", "-e", target_file])
                        
                        merged = True
    
    if not merged:
        print("No matching files found for the specified source and target languages.")

# Get command line arguments
import sys

if len(sys.argv) < 4:
    print("Usage: python script.py <source_lang> <target_lang> <location>")
else:
    source_lang = sys.argv[1]
    target_lang = sys.argv[2]
    location = sys.argv[3]
    process_files(source_lang, target_lang, location)
