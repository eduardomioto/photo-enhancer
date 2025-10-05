#!/usr/bin/env python3
"""
Photo Enhancement GUI
A desktop GUI for the photo enhancement tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from photo_enhancer import enhance_photo, enhance_folder, PROFILES, list_profiles
import sys


class PhotoEnhancerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Enhancer")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.selected_profile = tk.StringVar(value=list(PROFILES.keys())[0])
        self.mode = tk.StringVar(value="folder")  # "file" or "folder"
        self.create_subfolder = tk.BooleanVar(value=True)
        self.processing = False

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        row = 0

        # Title
        title_label = ttk.Label(main_frame, text="Photo Enhancement Tool",
                                font=('Arial', 18, 'bold'))
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 20))
        row += 1

        # Mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Processing Mode", padding="10")
        mode_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))

        ttk.Radiobutton(mode_frame, text="Single Image", variable=self.mode,
                        value="file", command=self.update_ui_mode).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="Folder (Batch)", variable=self.mode,
                        value="folder", command=self.update_ui_mode).pack(side=tk.LEFT, padx=10)
        row += 1

        # Input selection
        ttk.Label(main_frame, text="Input:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)

        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path, state='readonly')
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        self.input_button = ttk.Button(input_frame, text="Browse...", command=self.browse_input)
        self.input_button.grid(row=0, column=1)
        row += 1

        # Output selection
        ttk.Label(main_frame, text="Output:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        output_frame.columnconfigure(0, weight=1)

        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path, state='readonly')
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        ttk.Button(output_frame, text="Browse...", command=self.browse_output).grid(row=0, column=1)
        row += 1

        # Profile selection
        ttk.Label(main_frame, text="Enhancement Profile:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=(0, 5))
        row += 1

        profile_frame = ttk.Frame(main_frame)
        profile_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        profile_frame.columnconfigure(0, weight=1)

        self.profile_combo = ttk.Combobox(profile_frame, textvariable=self.selected_profile,
                                          values=list(PROFILES.keys()), state='readonly', width=30)
        self.profile_combo.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.profile_combo.bind('<<ComboboxSelected>>', self.show_profile_details)

        ttk.Button(profile_frame, text="View All Profiles",
                   command=self.show_all_profiles).grid(row=0, column=1)
        row += 1

        # Profile details display
        self.profile_details_frame = ttk.LabelFrame(main_frame, text="Profile Details", padding="10")
        self.profile_details_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))

        self.profile_details_label = ttk.Label(self.profile_details_frame, text="",
                                               justify=tk.LEFT, wraplength=600)
        self.profile_details_label.pack(anchor=tk.W)
        self.show_profile_details()
        row += 1

        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))

        self.subfolder_check = ttk.Checkbutton(options_frame,
                                               text="Create subfolder for each profile (recommended for batch)",
                                               variable=self.create_subfolder)
        self.subfolder_check.pack(anchor=tk.W)
        row += 1

        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))

        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate', length=600)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        self.status_label = ttk.Label(progress_frame, text="Ready to process", foreground="green")
        self.status_label.pack(anchor=tk.W)
        row += 1

        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=(10, 0))

        self.process_button = ttk.Button(button_frame, text="Start Processing",
                                         command=self.start_processing, style='Accent.TButton')
        self.process_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)

        # Configure button style
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))

    def update_ui_mode(self):
        """Update UI based on selected mode"""
        # Just update the button text hint
        mode = self.mode.get()
        if mode == "file":
            self.input_button.configure(text="Browse File...")
        else:
            self.input_button.configure(text="Browse Folder...")

    def browse_input(self):
        """Browse for input file or folder"""
        if self.mode.get() == "file":
            path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[
                    ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
                    ("All files", "*.*")
                ]
            )
        else:
            path = filedialog.askdirectory(title="Select Input Folder")

        if path:
            self.input_path.set(path)

            # Auto-suggest output path
            if not self.output_path.get():
                if self.mode.get() == "file":
                    input_file = Path(path)
                    suggested_output = input_file.parent / f"{input_file.stem}_enhanced{input_file.suffix}"
                    self.output_path.set(str(suggested_output))
                else:
                    input_folder = Path(path)
                    suggested_output = input_folder.parent / "enhanced"
                    self.output_path.set(str(suggested_output))

    def browse_output(self):
        """Browse for output location"""
        if self.mode.get() == "file":
            path = filedialog.asksaveasfilename(
                title="Save Enhanced Image As",
                defaultextension=".jpg",
                filetypes=[
                    ("JPEG", "*.jpg"),
                    ("PNG", "*.png"),
                    ("All files", "*.*")
                ]
            )
        else:
            path = filedialog.askdirectory(title="Select Output Folder")

        if path:
            self.output_path.set(path)

    def show_profile_details(self, event=None):
        """Display details of selected profile"""
        profile_name = self.selected_profile.get()
        if profile_name in PROFILES:
            profile = PROFILES[profile_name]
            details = f"{profile.name}\n"
            details += f"HDR: {profile.hdr}%  |  Brightness: {profile.brightness:+d}%  |  Contrast: {profile.contrast:+d}%\n"
            details += f"Saturation: {profile.saturation:+d}%  |  Warmth: {profile.warmth:+d}%\n"
            details += f"Shadows: {profile.shadows:+d}%  |  White Point: {profile.white_point}%"
            self.profile_details_label.config(text=details)

    def show_all_profiles(self):
        """Show all profiles in a popup window"""
        popup = tk.Toplevel(self.root)
        popup.title("All Enhancement Profiles")
        popup.geometry("600x500")

        # Add scrollbar
        frame = ttk.Frame(popup, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=('Courier', 10))
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)

        # Add profile information
        for name, profile in PROFILES.items():
            text.insert(tk.END, f"{name}: {profile.name}\n", "header")
            text.insert(tk.END, f"  HDR: {profile.hdr}%, Brightness: {profile.brightness:+d}%\n")
            text.insert(tk.END, f"  Contrast: {profile.contrast:+d}%, Saturation: {profile.saturation:+d}%\n")
            text.insert(tk.END, f"  Shadows: {profile.shadows:+d}%, Warmth: {profile.warmth:+d}%\n")
            text.insert(tk.END, f"  White Point: {profile.white_point}%\n\n")

        text.tag_config("header", font=('Courier', 10, 'bold'))
        text.config(state=tk.DISABLED)

        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

    def clear_fields(self):
        """Clear all input fields"""
        self.input_path.set("")
        self.output_path.set("")

    def validate_inputs(self):
        """Validate user inputs"""
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input file or folder")
            return False

        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output location")
            return False

        if not Path(self.input_path.get()).exists():
            messagebox.showerror("Error", "Input file or folder does not exist")
            return False

        return True

    def start_processing(self):
        """Start the processing in a separate thread"""
        if self.processing:
            messagebox.showwarning("Warning", "Processing already in progress")
            return

        if not self.validate_inputs():
            return

        # Start processing in a thread to keep UI responsive
        self.processing = True
        self.process_button.config(state=tk.DISABLED)
        self.progress_bar.start(10)
        self.status_label.config(text="Processing...", foreground="blue")

        thread = threading.Thread(target=self.process_photos)
        thread.daemon = True
        thread.start()

    def process_photos(self):
        """Process photos (runs in separate thread)"""
        try:
            input_path = self.input_path.get()
            output_path = self.output_path.get()
            profile = self.selected_profile.get()

            if self.mode.get() == "file":
                # Single file processing
                enhance_photo(input_path, output_path, profile, verbose=False)
                success_msg = f"Photo enhanced successfully!\n\nSaved to:\n{output_path}"
            else:
                # Folder processing
                enhance_folder(
                    input_path,
                    output_path,
                    profile,
                    create_subfolder=self.create_subfolder.get(),
                    verbose=False
                )
                output_location = Path(output_path)
                if self.create_subfolder.get():
                    output_location = output_location / profile
                success_msg = f"Batch processing complete!\n\nEnhanced photos saved to:\n{output_location}"

            # Update UI on success (must be done in main thread)
            self.root.after(0, lambda: self.processing_complete(success_msg))

        except Exception as e:
            # Update UI on error (must be done in main thread)
            self.root.after(0, lambda: self.processing_error(str(e)))

    def processing_complete(self, message):
        """Called when processing completes successfully"""
        self.processing = False
        self.progress_bar.stop()
        self.process_button.config(state=tk.NORMAL)
        self.status_label.config(text="Processing complete!", foreground="green")
        messagebox.showinfo("Success", message)

    def processing_error(self, error_msg):
        """Called when processing encounters an error"""
        self.processing = False
        self.progress_bar.stop()
        self.process_button.config(state=tk.NORMAL)
        self.status_label.config(text="Error occurred", foreground="red")
        messagebox.showerror("Error", f"An error occurred:\n\n{error_msg}")


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = PhotoEnhancerGUI(root)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()