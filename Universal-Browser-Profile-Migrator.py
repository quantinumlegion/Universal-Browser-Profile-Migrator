import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

class UniversalMigratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Browser Profile Migrator")
        self.root.geometry("550x550") # Taller window to accommodate portable path configurations cleanly
        self.root.resizable(False, False)
        
        # Base System Access Paths
        self.local_appdata = os.environ.get('LOCALAPPDATA', '')
        self.roaming_appdata = os.environ.get('APPDATA', '')

        # Variables
        self.browser_var = tk.StringVar(value="Firefox")
        self.operation_var = tk.StringVar(value="Backup")
        self.is_portable_var = tk.BooleanVar(value=False)
        self.portable_path_var = tk.StringVar()
        self.folder_path_var = tk.StringVar()

        # Supported Browser Matrix
        self.supported_browsers = [
            "Firefox", "Waterfox", "LibreWolf", "Pale Moon", "Tor Browser",
            "Chrome", "Brave", "Edge", "Opera", "Vivaldi", "Yandex"
        ]

        self.setup_ui()
        self.scan_and_update_stats()

    def setup_ui(self):
        # Header
        header = tk.Label(self.root, text="Universal Browser Profile Migrator", font=("Arial", 14, "bold"), fg="#0056B3")
        header.pack(pady=15)

        # Frame for controls
        frame = tk.LabelFrame(self.root, text=" Settings ", padx=15, pady=15)
        frame.pack(padx=20, pady=5, fill="x")

        # 1. Browser Selection
        tk.Label(frame, text="Select Browser:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.browser_dropdown = ttk.Combobox(frame, textvariable=self.browser_var, values=self.supported_browsers, state="readonly", width=18)
        self.browser_dropdown.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.browser_dropdown.bind("<<ComboboxSelected>>", lambda e: self.scan_and_update_stats())

        # 2. Portable App Toggle Hook
        self.portable_chk = tk.Checkbutton(frame, text="Portable Version (Standalone Folder)", variable=self.is_portable_var, font=("Arial", 9, "bold"), command=self.toggle_portable_mode)
        self.portable_chk.grid(row=1, column=0, columnspan=3, sticky="w", pady=5)

        # 3. Dynamically Dispatched Portable Path Finder Row
        self.port_label = tk.Label(frame, text="Browser Location:", font=("Arial", 10))
        self.port_entry = tk.Entry(frame, textvariable=self.portable_path_var, width=32)
        self.port_btn = tk.Button(frame, text="Browse...", command=self.browse_portable_folder)

        # 4. Operation Selection
        tk.Label(frame, text="Select Action:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.op_dropdown = ttk.Combobox(frame, textvariable=self.operation_var, values=["Backup", "Restore"], state="readonly", width=18)
        self.op_dropdown.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        self.op_dropdown.bind("<<ComboboxSelected>>", self.update_label_text)

        # 5. Backup Archive Path Selection
        self.path_label = tk.Label(frame, text="Save Backup To:", font=("Arial", 10))
        self.path_label.grid(row=4, column=0, sticky="w", pady=10)
        
        path_entry = tk.Entry(frame, textvariable=self.folder_path_var, width=32)
        path_entry.grid(row=4, column=1, padx=10, pady=10)
        
        browse_btn = tk.Button(frame, text="Browse...", command=self.browse_backup_folder)
        browse_btn.grid(row=4, column=2, pady=10)

        # 6. Status Log Box
        self.status_box = tk.Text(self.root, height=7, width=60, bg="#F0F0F0", state="disabled", font=("Courier", 9))
        self.status_box.pack(pady=10)

        # 7. Progress Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=430, mode="indeterminate")
        self.progress.pack(pady=5)

        # Action Button
        self.action_btn = tk.Button(self.root, text="Start Transfer", font=("Arial", 11, "bold"), bg="#0056B3", fg="white", width=20, command=self.start_process_thread)
        self.action_btn.pack(pady=10)

    def toggle_portable_mode(self):
        """ Handles showing/hiding path options dynamically based on selection layout constraints """
        if self.is_portable_var.get():
            self.port_label.grid(row=2, column=0, sticky="w", pady=5)
            self.port_entry.grid(row=2, column=1, padx=10, pady=5)
            self.port_btn.grid(row=2, column=2, pady=5)
            self.log("[System UI] Portable target redirection mode enabled.")
        else:
            self.port_label.grid_forget()
            self.port_entry.grid_forget()
            self.port_btn.grid_forget()
            self.log("[System UI] Switched back to standard automatic system scan mode.")
        self.scan_and_update_stats()

    def get_browser_paths(self):
        """ Maps active structural nodes depending on local app registries versus custom targeted directories """
        browser = self.browser_var.get()
        is_portable = self.is_portable_var.get()
        portable_root = self.portable_path_var.get()

        # Handle Portable mode logic targets safely
        if is_portable:
            if not portable_root or not os.path.exists(portable_root):
                return None, None, None, ""
            
            # Auto-detect internals for typical portable layout branches
            # Checks for standard layout vs PortableApps directory trees
            data_sub = os.path.join(portable_root, "Data", "profile")
            if not os.path.exists(data_sub):
                data_sub = os.path.join(portable_root, "Data", "settings")
                if not os.path.exists(data_sub):
                    data_sub = portable_root # Fallback to using parent folder chosen directly

            if browser in ["Firefox", "Waterfox", "LibreWolf", "Pale Moon", "Tor Browser"]:
                return "Gecko", portable_root, data_sub, ""
            else:
                return "Chromium", portable_root, data_sub, ""

        # --- Standard Automatic Directory Mapping Engine ---
        if browser == "Firefox":
            root = os.path.join(self.roaming_appdata, 'Mozilla', 'Firefox')
            return "Gecko", root, os.path.join(root, 'Profiles'), "firefox.exe"
        elif browser == "Waterfox":
            root = os.path.join(self.roaming_appdata, 'Waterfox')
            return "Gecko", root, os.path.join(root, 'Profiles'), "waterfox.exe"
        elif browser == "LibreWolf":
            root = os.path.join(self.roaming_appdata, 'librewolf')
            return "Gecko", root, os.path.join(root, 'Profiles'), "librewolf.exe"
        elif browser == "Pale Moon":
            root = os.path.join(self.roaming_appdata, 'Moonchild Productions', 'Pale Moon')
            return "Gecko", root, os.path.join(root, 'Profiles'), "palemoon.exe"
        elif browser == "Tor Browser":
            root = os.path.join(self.local_appdata, 'Tor Browser', 'Browser', 'TorBrowser', 'Data', 'Browser')
            return "Gecko", root, os.path.join(root, 'Profiles'), "firefox.exe"
        elif browser == "Chrome":
            root = os.path.join(self.local_appdata, 'Google', 'Chrome', 'User Data')
            return "Chromium", root, root, "chrome.exe"
        elif browser == "Brave":
            root = os.path.join(self.local_appdata, 'BraveSoftware', 'Brave-Browser', 'User Data')
            return "Chromium", root, root, "brave.exe"
        elif browser == "Edge":
            root = os.path.join(self.local_appdata, 'Microsoft', 'Edge', 'User Data')
            return "Chromium", root, root, "msedge.exe"
        elif browser == "Opera":
            root = os.path.join(self.roaming_appdata, 'Opera Software', 'Opera Stable')
            return "Chromium", root, root, "opera.exe"
        elif browser == "Vivaldi":
            root = os.path.join(self.local_appdata, 'Vivaldi', 'User Data')
            return "Chromium", root, root, "vivaldi.exe"
        elif browser == "Yandex":
            root = os.path.join(self.local_appdata, 'Yandex', 'YandexBrowser', 'User Data')
            return "Chromium", root, root, "browser.exe"
        
        return None, None, None, ""

    def verify_browser_closed(self, process_name):
        if not process_name:
            return True # Skips portable check safely if execution tags are empty
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {process_name}"', startupinfo=startupinfo, shell=True).decode('utf-8', errors='ignore')
            return process_name.lower() not in output.lower()
        except Exception:
            return True

    def update_label_text(self, event=None):
        if self.operation_var.get() == "Backup":
            self.path_label.config(text="Save Backup To:")
        else:
            self.path_label.config(text="Load Backup From:")

    def browse_backup_folder(self):
        selected_dir = filedialog.askdirectory(title="Select Folder")
        if selected_dir:
            self.folder_path_var.set(os.path.normpath(selected_dir))

    def browse_portable_folder(self):
        selected_dir = filedialog.askdirectory(title="Select Portable Browser App Folder")
        if selected_dir:
            self.portable_path_var.set(os.path.normpath(selected_dir))
            self.scan_and_update_stats()

    def scan_and_update_stats(self):
        browser = self.browser_var.get()
        engine, root_dir, profiles_dir, process_name = self.get_browser_paths()

        if not profiles_dir or not os.path.exists(profiles_dir):
            if self.is_portable_var.get():
                self.log(f"[System Status] Please specify a valid folder path for Portable {browser}.")
            else:
                self.log(f"[System Status] Standard {browser} data was not found on this computer.")
            return

        try:
            if self.is_portable_var.get():
                self.log(f"[System Status] Target verified. Ready to sync Portable {browser} folder footprint structures.")
                return

            if engine == "Gecko":
                count = len([d for d in os.listdir(profiles_dir) if os.path.isdir(os.path.join(profiles_dir, d))])
            else:  # Chromium
                count = len([d for d in os.listdir(profiles_dir) if d in ["Default", "Profile 1"] or (d.startswith("Profile ") and os.path.isdir(os.path.join(profiles_dir, d)))])
            
            self.log(f"[System Status] Found {count} active {browser} profile(s) locally.")
        except Exception:
            self.log(f"[System Status] Found {browser}, but scanning engine dropped a handle.")

    def log(self, message):
        self.status_box.config(state="normal")
        self.status_box.insert(tk.END, message + "\n")
        self.status_box.see(tk.END)
        self.status_box.config(state="disabled")
        self.root.update_idletasks()

    def start_process_thread(self):
        browser = self.browser_var.get()
        engine, root_dir, profiles_dir, process_name = self.get_browser_paths()

        if not self.verify_browser_closed(process_name):
            messagebox.showwarning("Process Running", f"Please completely close standard instances of {browser} before performing operations.")
            return

        if not profiles_dir:
            messagebox.showerror("Error", "Please make sure your portable program path choice is fully resolved.")
            return

        target_path = self.folder_path_var.get()
        if not target_path:
            messagebox.showerror("Error", "Please select a target backup/restore folder path first!")
            return

        self.status_box.config(state="normal")
        self.status_box.delete('1.0', tk.END)
        self.status_box.config(state="disabled")
        self.action_btn.config(state="disabled", text="Migrating...")
        self.progress.start(15)

        mode = self.operation_var.get()
        worker = threading.Thread(target=self.run_migration, args=(mode, target_path))
        worker.daemon = True
        worker.start()

    def run_migration(self, mode, target_path):
        if mode == "Backup":
            self.run_backup(target_path)
        else:
            self.run_restore(target_path)
        
        self.progress.stop()
        self.action_btn.config(state="normal", text="Start Transfer")

    def run_backup(self, dest):
        browser = self.browser_var.get()
        engine, root_src, profile_src, process_name = self.get_browser_paths()

        if not os.path.exists(profile_src):
            messagebox.showerror("Error", f"Could not locate source data coordinates for the selected {browser}.")
            return
        
        try:
            self.log(f"[Task Status] Packaging up {browser} configuration matrices...")
            if not os.path.exists(dest): os.makedirs(dest)

            # Portable Generic Catch All Routine
            if self.is_portable_var.get():
                self.log(f"[File System] Bundling full standalone tracking profile structures recursively...")
                if os.path.exists(os.path.join(dest, "PortableData")):
                    shutil.rmtree(os.path.join(dest, "PortableData"))
                shutil.copytree(profile_src, os.path.join(dest, "PortableData"))
            
            # Standard AppData Route Process
            elif engine == "Gecko":
                dest_profiles = os.path.join(dest, "Profiles")
                dest_ini = os.path.join(dest, "profiles.ini")
                src_ini = os.path.join(root_src, "profiles.ini")

                self.log("[File System] Copying core Profile structures...")
                if os.path.exists(dest_profiles): shutil.rmtree(dest_profiles)
                shutil.copytree(profile_src, dest_profiles)
                
                if os.path.exists(src_ini):
                    shutil.copy2(src_ini, dest_ini)

            elif engine == "Chromium":
                self.log("[File System] Extracting isolated Chromium application structures...")
                targets = ["Default", "Local State", "Secure Preferences"] + [d for d in os.listdir(profile_src) if d.startswith("Profile ")]
                
                for item in [t for t in targets if os.path.exists(os.path.join(profile_src, t))]:
                    src_item = os.path.join(profile_src, item)
                    dest_item = os.path.join(dest, item)
                    
                    self.log(f"[File System] Copying profile node: {item}...")
                    if os.path.isdir(src_item):
                        if os.path.exists(dest_item): shutil.rmtree(dest_item)
                        shutil.copytree(src_item, dest_item)
                    else:
                        shutil.copy2(src_item, dest_item)
            
            self.log(f"\n>>> SUCCESS: {browser} backup complete! <<<")
            messagebox.showinfo("Success", f"{browser} data successfully backed up!")
            
        except Exception as e:
            self.log(f"\n[CRITICAL FAILURE]: {str(e)}")
            messagebox.showerror("Error", f"Migration interrupted:\n{e}")

    def run_restore(self, src):
        browser = self.browser_var.get()
        engine, root_dest, profile_dest, process_name = self.get_browser_paths()

        try:
            self.log(f"[Task Status] Deploying runtime archives into {browser} ecosystem...")
            
            # Portable Mode Restore Execution Logic 
            if self.is_portable_var.get():
                portable_src_folder = os.path.join(src, "PortableData")
                if not os.path.exists(portable_src_folder):
                    messagebox.showerror("Error", "Selected folder does not contain a valid portable archive deployment structure.")
                    return
                self.log("[File System] Overwriting custom portable layout branches...")
                if os.path.exists(profile_dest): shutil.rmtree(profile_dest)
                shutil.copytree(portable_src_folder, profile_dest)

            # Standard Mode Core Restorations
            elif engine == "Gecko":
                src_profiles = os.path.join(src, "Profiles")
                src_ini = os.path.join(src, "profiles.ini")

                if not os.path.exists(src_profiles):
                    messagebox.showerror("Error", "Target selection contains no valid Profile structure mappings.")
                    return

                if not os.path.exists(root_dest): os.makedirs(root_dest)

                self.log("[File System] Restoring Gecko configuration matrices...")
                dest_p = os.path.join(root_dest, "Profiles")
                if os.path.exists(dest_p): shutil.rmtree(dest_p)
                shutil.copytree(src_profiles, dest_p)

                if os.path.exists(src_ini):
                    shutil.copy2(src_ini, os.path.join(root_dest, "profiles.ini"))

            elif engine == "Chromium":
                items_to_restore = [d for d in os.listdir(src) if d in ["Default", "Local State", "Secure Preferences"] or d.startswith("Profile ")]
                
                if not items_to_restore:
                    messagebox.showerror("Error", "Selected directory contains no valid Chromium data nodes.")
                    return

                if not os.path.exists(root_dest): os.makedirs(root_dest)

                for item in items_to_restore:
                    src_item = os.path.join(src, item)
                    dest_item = os.path.join(root_dest, item)
                    
                    self.log(f"[File System] Injecting profile node: {item}...")
                    if os.path.isdir(src_item):
                        if os.path.exists(dest_item): shutil.rmtree(dest_item)
                        shutil.copytree(src_item, dest_item)
                    else:
                        shutil.copy2(src_item, dest_item)

            self.log(f"\n>>> SUCCESS: {browser} restore pipeline completed! <<<")
            messagebox.showinfo("Success", f"{browser} data injection successful!")
            
        except Exception as e:
            self.log(f"\n[CRITICAL FAILURE]: {str(e)}")
            messagebox.showerror("Error", f"Migration pipeline dropped connection:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalMigratorApp(root)
    root.mainloop()