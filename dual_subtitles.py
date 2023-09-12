import os
import shutil
import subprocess

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

base_language_combo = None
target_language_combo = None
folder_entry = None

# Create a function to redirect the print output to the Text widget
def redirect_output(text_widget, window):
    class CustomStream:
        def __init__(self, text_widget, window):
            self.text_widget = text_widget
            self.window = window

        def write(self, text):
            self.text_widget.insert(tk.END, text)
            self.text_widget.see(tk.END)  # Auto-scroll to the end
            self.window.update()  # Force widget update

        def flush(self):
            pass

    sys.stdout = CustomStream(text_widget, window)

def apply():
    global base_language_combo
    global target_language_combo
    global folder_entry
    # Get selected values from comboboxes
    base_language = base_language_combo.get()
    target_language = target_language_combo.get()
    selected_folder = folder_entry.get()

    # Perform your actions with the selected values
    process_files(target_language, base_language, selected_folder)
    print("Modified Language:", base_language)
    print("Translation Language (added):", target_language)
    print("Selected Folder:", selected_folder)
    print("--- DONE !       ---")
    print("--- You can exit ---")
    print("To restore defaults, use the same source and base languages.")
    
def open_ui_dialog():
    global base_language_combo
    global target_language_combo
    global folder_entry
    # Create the main dialog window
    window = tk.Tk()
    window.title("The Witcher 3 Dual Subtitles Mod")
    window.configure(bg="light blue")
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
      
 
    top_label = tk.Label(window, text="Language to Translate -> Translation Language")
    top_label.grid(row=0, column=0, columnspan=2)
    
    # Create combobox for Base Language
    base_language_combo = ttk.Combobox(window, values=["ar", "br", "cn", "cz", "de", "en", "enpc", "es", "esmx", "fr", "hu", "it", "pl", "ru", "plpc", "tr", "zh"])
    base_language_combo.set("pl")
    base_language_combo.grid(row=1, column=0)

    # Create combobox for Target Language
    target_language_combo = ttk.Combobox(window, values=["ar", "br", "cn", "cz", "de", "en", "enpc", "es", "esmx", "fr", "hu", "it", "pl", "ru", "plpc", "tr", "zh"])
    target_language_combo.set("fr")
    target_language_combo.grid(row=1, column=1)

    # Create a button to open a folder selection dialog
    def select_folder():
        folder_path = filedialog.askdirectory()
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

    folder_button = tk.Button(window, text="Select Folder", command=select_folder)
    folder_button.grid(row=2, column=0)
  

    # Create an editable textbox for selected folder
    folder_entry = tk.Entry(window)
    folder_entry.insert(0, "C:\Program Files (x86)\Steam\steamapps\common\The Witcher 3")
    folder_entry.grid(row=2, column=1)

    # Create an Apply button to call the apply() function
    apply_button = tk.Button(window, text="Apply", command=apply)
    apply_button.grid(row=3, column=0, columnspan=2)

    # Create a label with a link to your YouTube channel
    youtube_label = tk.Label(window, text="Check out my YouTube channel:")
    youtube_label.grid(row=4, column=0, columnspan=2)

    youtube_link = tk.Label(window, text="https://www.youtube.com/@maximumspoil2500", fg="blue", cursor="hand2")
    youtube_link.grid(row=5, column=0, columnspan=2)
    youtube_link.bind("<Button-1>", lambda e: window.clipboard_append("https://www.youtube.com/@maximumspoil2500"))
    
    # Create a Text widget to display console output
    output_text = tk.Text(window, wrap=tk.WORD, height=10, width=40)
    output_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # Redirect print output to the Text widget
    redirect_output(output_text, window)

     # Calculate the window position for centering
    window_width = 340  # Change this to the desired window width
    window_height = 300  # Change this to the desired window height
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the window's geometry to center it on the screen
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Start the GUI main loop
    window.mainloop()

def merge_content(source_file, target_file, should_merge):
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
        if (len(line_parts2) > 0 and should_merge):
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
    should_merge = source_lang != target_lang
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
                        merged_lines = merge_content(source_file, target_file, should_merge)
                        
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
    print("Running UI mode.")
    print("Usage: python script.py <source_lang> <target_lang> <location>")
    open_ui_dialog()
else:
    print("Running batch mode.")
    print("To restore defaults, use the same source and base languages.")
    source_lang = sys.argv[1]
    target_lang = sys.argv[2]
    location = sys.argv[3]
    process_files(source_lang, target_lang, location)
