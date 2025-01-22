import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from datetime import datetime

# Function to display file details
def get_file_details(filename):
    try:
        # Get the file details
        file_size = os.path.getsize(filename)
        creation_time = os.path.getctime(filename)
        modification_time = os.path.getmtime(filename)

        # Return formatted details
        return {
            "path": filename,
            "size": file_size,
            "created_on": datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S'),
            "modified_on": datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve file details: {e}")
        return None

# Function to load and display the file content immediately
def load_and_display_file():
    try:
        # Get the source file path using a file dialog
        source_filename = filedialog.askopenfilename(title="Select Source File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        
        # Check if the file exists
        if not source_filename:
            messagebox.showerror("Error", "No file selected. Please select a valid file.")
            return
        
        # Get file details and display
        file_details = get_file_details(source_filename)
        if file_details:
            file_details_label.config(text=f"File Path: {file_details['path']}\nFile Size: {file_details['size']} bytes\nCreated On: {file_details['created_on']}\nLast Modified: {file_details['modified_on']}")
        
        # Open the file and display its content
        with open(source_filename, 'r') as source_file:
            content = source_file.read()

        # Display the content in the text box
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, content)

        # Prompt the user to choose whether to append or save the file
        action = messagebox.askquestion("Modify or Append", "Do you want to append text or save the file? (Click 'Yes' to append, 'No' to save)")
        if action == 'yes':
            append_or_save_file(source_filename, content, append=True)
        else:
            append_or_save_file(source_filename, content, append=False)

    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")

# Consolidated function to append or save the file
def append_or_save_file(source_filename, content, append=True):
    try:
        if append:
            # Create a popup to allow user to input text to append
            new_text = simpledialog.askstring("Append Text", "Enter the text you want to append:")
            if new_text:
                content += f"\n{new_text}"
        else:
            # Ask the user for the text they want to modify
            modified_content = simpledialog.askstring("Modify Text", "Enter the new text (leave blank to keep original content):")
            if modified_content is not None and modified_content.strip() != "":
                content = modified_content

        # Ask the user for the destination file path using a file save dialog
        dest_filename = filedialog.asksaveasfilename(title="Save Modified File", defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not dest_filename:
            messagebox.showerror("Error", "No destination file selected. Please select a valid file.")
            return

        # Open the destination file and write the content
        with open(dest_filename, 'w') as dest_file:
            dest_file.write(content)

        # Show success message
        messagebox.showinfo("Success", f"File has been modified and saved as '{dest_filename}'.")
        text_box.delete(1.0, tk.END)  # Clear the content box after saving

    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An error occurred while modifying the file: {e}")

# Setting up the Tkinter root window
root = tk.Tk()
root.title("File Read & Write Challenge 🖋️")
root.geometry("800x500")
root.config(bg="#f4f6f9")

# Adding a title label with improved font and padding
title_label = tk.Label(root, text="File Read & Write Challenge 🖋️", font=("Helvetica", 18, "bold"), bg="#f4f6f9", pady=20, fg="#333333")
title_label.pack()

# Button to select the file and choose action (Append or Save)
select_button = tk.Button(root, text="Select and Modify File", font=("Helvetica", 14), bg="#4CAF50", fg="white", bd=0, width=25, height=2, command=load_and_display_file)
select_button.pack(pady=15)

# Label to display file details
file_details_label = tk.Label(root, text="File Details will appear here", bg="#f4f6f9", font=("Helvetica", 12), justify=tk.LEFT, anchor="w", padx=10)
file_details_label.pack(pady=10, fill=tk.X)

# Label and Text box for viewing and editing file content
view_label = tk.Label(root, text="File Content View", bg="#f4f6f9", font=("Helvetica", 14, "bold"))
view_label.pack(pady=5)
text_box = tk.Text(root, height=10, width=60, wrap=tk.WORD, font=("Helvetica", 12), bg="#ffffff", bd=2, relief="solid", padx=10, pady=10)
text_box.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
