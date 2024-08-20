import customtkinter as ctk
import getpass
import shutil
import json
import os

from .message import Message
from tkinter import filedialog

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')


class App:
    def __init__(self):        
        # Set path variables
        self.curseforge_instances_path = f"C:\\Users\\{getpass.getuser()}\\curseforge\\minecraft\\Instances\\"
        self.ftb_app_instances_path = f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\.ftba\\instances\\"

        # Check if OneDrive exists
        if os.path.isdir("C:\\Users\\{getpass.getuser()}\\OneDrive"):
            self.curseforge_instances_path = f"C:\\Users\\{getpass.getuser()}\\OneDrive\\Documents\\curseforge\\minecraft\\Instances\\"
            self.ftb_app_instances_path = f"C:\\Users\\{getpass.getuser()}\\OneDrive\\Documents\\.ftba\\instances\\"

        self.json_path = f"{os.getcwd()}\\paths.json"
        self.essential_path = f"{os.getcwd()}\\essential_versions"
        self.forge_files = os.path.join(self.essential_path, "forge")
        self.fabric_files = os.path.join(self.essential_path, "fabric")

        # Json data
        with open(self.json_path, 'r') as f:
            self.data = json.load(f)

        self.prev_essential_btn = None
        self.prev_mod_btn = None

        self.gui()
    

    def gui(self):
        self.root = ctk.CTk()
        self.root.title("Essential Installer")
        self.root.geometry("600x400")
        self.root.resizable(0, 0)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=(5, 0))

        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure((0, 1), weight=2)
        main_frame.grid_columnconfigure(2, weight=1)

        # Essential fabric frame
        self.chosen_fabric = ctk.CTkLabel(main_frame, text="Chosen fabric file: None", text_color="#c3c3c3")
        self.chosen_fabric.grid(row=0, column=0, sticky='n')

        fabric_frame = ctk.CTkScrollableFrame(main_frame)
        fabric_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        fabric_frame.grid_columnconfigure(0, weight=1)

        for index, file in enumerate(os.listdir(self.fabric_files)):
            file_name = file.split(sep=".jar")

            fabric_btn = ctk.CTkButton(fabric_frame, text=file_name[0], fg_color="#1c1c1c", height=40, hover_color="#141414", corner_radius=5)
            fabric_btn.configure(command=lambda btn=fabric_btn, dir=file: self.select_essential(btn, dir, forge_or_essential='Fabric'))
            fabric_btn.grid(row=index, column=0, padx=5, pady=3, sticky='nsew')
            fabric_btn.grid_propagate(0)
        

        # Essential forge frame
        self.chosen_forge = ctk.CTkLabel(main_frame, text="Chosen forge file: None", text_color="#c3c3c3")
        self.chosen_forge.grid(row=0, column=1, sticky='n')

        forge_frame = ctk.CTkScrollableFrame(main_frame)
        forge_frame.grid(row=1, column=1, sticky='ns', padx=5, pady=5)
        forge_frame.grid_columnconfigure(0, weight=1)

        for index, file in enumerate(os.listdir(self.forge_files)):
            file_name = file.split(sep=".jar")

            forge_btn = ctk.CTkButton(forge_frame, text=file_name[0], fg_color="#1c1c1c", height=40, hover_color="#141414", corner_radius=5)
            forge_btn.configure(command=lambda btn=forge_btn, dir=file: self.select_essential(btn, dir, forge_or_essential='Forge'))
            forge_btn.grid(row=index, column=0, padx=5, pady=3, sticky='nsew')
            forge_btn.grid_propagate(0)


        # Mods frame
        self.chosen_mod = ctk.CTkLabel(main_frame, text="Chosen modpack: None", text_color="#c3c3c3")
        self.chosen_mod.grid(row=0, column=2, sticky='n')

        self.mods_frame = ctk.CTkScrollableFrame(main_frame)
        self.mods_frame.grid(row=1, column=2, sticky='ns', padx=5, pady=5)
        self.mods_frame.grid_columnconfigure(0, weight=1)

        # Bottom frame
        bottom_frame = ctk.CTkFrame(self.root, height=40)
        bottom_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5, columnspan=3)

        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=0)

        # Add essential to mod button
        add_essential_btn = ctk.CTkButton(bottom_frame, fg_color="#1c1c1c", hover_color="#141414", cursor="hand2", text="Add essential to the selected mod",
                                          command=self.add_essential_to_mod)
        add_essential_btn.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        # Select mods folder path
        self.mod_folder_options = ["Curseforge", "FTB App"] + [path_name for path_name in self.data] + ["Add new mods path"] + ["Remove mod path"]
        select_mods_folder_label = ctk.CTkLabel(bottom_frame, text="Select mods folder:")
        select_mods_folder_label.grid(row=0, column=1, sticky='e', padx=5, pady=5)

        self.select_mods_folder = ctk.CTkOptionMenu(bottom_frame, 
                                               values=[x for x in self.mod_folder_options], 
                                               fg_color="#1c1c1c", 
                                               button_hover_color="#141414", 
                                               button_color="#1e1e1e",
                                               command=self.change_selected_mods_frame
                                               )
        self.select_mods_folder.grid(row=0, column=2, sticky='e', padx=5, pady=5)
        self.select_mods_folder.grid_propagate(0)

        self.change_selected_mods_frame(frame="Curseforge")
        self.root.mainloop()
    

    def delete_path_from_paths(self, name):
        with open(self.json_path, 'r+') as f:
            data = json.load(f)
            del data[name]
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
        
        self.mod_folder_options.remove(name)
        self.select_mods_folder.configure(values=self.mod_folder_options)
        
        self.delete_root.quit()
        self.delete_root.destroy()
                
    
    def change_selected_mods_frame(self, frame):
        if frame not in ["Add new mods path", "Remove mod path"]:
            self.cur_selected_frame = frame

        if self.prev_mod_btn != None:
            self.prev_mod_btn = None

        for child in self.mods_frame.winfo_children():
            child.destroy()


        if frame == "Add new mods path":
            self.select_mods_folder.set(value=self.cur_selected_frame)
            
            val = Message.askyesno("Add path", "Would you like to add a custom path to a modpacks folder?")
            if val:
                folder_path = filedialog.askdirectory()
                
                val = Message.askyesno("Confirmation", f"Are you sure you want to add the directory {folder_path}")
                if val:
                    with open(self.json_path, 'r') as f:
                        self.data = json.load(f)

                    name = Message.askinput("Create a name", "What name would you like to use for this path (e.g: curseforges modpack path is named 'curseforge')")
                    self.data[name] = folder_path
                    if name != "":
                        with open(self.json_path, 'w') as f:
                            json.dump(self.data, f, indent=2)
                
                    insert_index = self.mod_folder_options.index("FTB App")
                    self.mod_folder_options.insert(insert_index + 1, name)
                    self.select_mods_folder.configure(values=self.mod_folder_options)

            self.change_selected_mods_frame(frame=self.cur_selected_frame)


        if frame == "Remove mod path":
            with open(self.json_path, 'r') as f:
                data = json.load(f)

            self.select_mods_folder.set(value=self.cur_selected_frame)

            val = Message.askyesno("Remove a path", "Would you like to remove a custom path?")
            if val:
                paths = [path for path in data]

                self.delete_root = ctk.CTk()
                self.delete_root.title("Remove a custom path")
                self.delete_root.geometry("250x250")
                self.delete_root.resizable(0, 0)

                self.delete_root.grid_rowconfigure(0, weight=1)
                self.delete_root.grid_columnconfigure(0, weight=1)

                delete_buttons_frame = ctk.CTkScrollableFrame(self.delete_root)
                delete_buttons_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
                delete_buttons_frame.grid_columnconfigure(0, weight=1)

                for index, name in enumerate(paths):
                    btn = ctk.CTkButton(delete_buttons_frame, text=name, fg_color="#1c1c1c", height=40, hover_color="#141414", corner_radius=5, 
                                        command=lambda name=name: self.delete_path_from_paths(name))
                    btn.grid(row=index, column=0, padx=5, pady=3, sticky='ew')
                    btn.grid_propagate(0)

                self.delete_root.mainloop()
                
        
        if frame == "Curseforge":
            for index, mod_folder in enumerate(os.listdir(self.curseforge_instances_path)):
                if mod_folder == ".localCache":
                    continue

                mod_btn = ctk.CTkButton(self.mods_frame, text=mod_folder if mod_folder != ".localCache" else "Error", fg_color="#1c1c1c", height=40, hover_color="#141414", corner_radius=5)
                mod_btn.configure(command=lambda btn=mod_btn, dir=mod_folder, name=mod_folder, custom="Curseforge": self.select_mod(btn, dir, name, custom))
                mod_btn.grid(row=index, column=0, padx=5, pady=3, sticky='nsew')
                mod_btn.grid_propagate(0)
        

        if frame == "FTB App":
            for index, mod_folder in enumerate(os.listdir(self.ftb_app_instances_path)):
                if mod_folder == ".localCache":
                    continue

                mod_btn = ctk.CTkButton(self.mods_frame, text=mod_folder, fg_color="#1c1c1c", height=40, hover_color="#141414", corner_radius=5)
                mod_btn.grid(row=index, column=0, padx=5, pady=3, sticky='nsew')
                mod_btn.configure(command=lambda btn=mod_btn, dir=mod_folder, name=mod_folder, custom="FTB App": self.select_mod(btn, dir, name, custom))
                mod_btn.grid_propagate(0)
            
        
        if frame not in ["Curseforge", "FTB App"]:
            with open(self.json_path, 'r') as f:
                data = json.load(f)

            for index, mod_folder in enumerate(os.listdir(data[frame])):
                mod_btn = ctk.CTkButton(self.mods_frame, text=mod_folder, fg_color="#1c1c1c", height=40, hover_color="#141414", corner_radius=5)
                mod_btn.configure(command=lambda btn=mod_btn, dir=mod_folder, name=mod_folder, custom=True: self.select_mod(btn, dir, name, custom))
                mod_btn.grid(row=index, column=0, padx=5, pady=3, sticky='nsew')
                mod_btn.grid_propagate(0)


    def select_essential(self, btn, dir, forge_or_essential):
        if self.prev_essential_btn:
            self.prev_essential_btn.configure(border_width=0)

        self.prev_essential_btn = btn
        self.essential = dir
        
        dir = dir.split('Essential-')[1].split('.jar')[0]
        if forge_or_essential == 'Forge':
            self.chosen_forge.configure(text=f"Chosen forge file: {dir}")
            self.chosen_fabric.configure(text="Chosen fabric file: None")
        else:
            self.chosen_fabric.configure(text=f"Chosen fabric file: {dir}")
            self.chosen_forge.configure(text="Chosen forge file: None")

        btn.configure(border_width=1, border_color="#55ffdd")


    def select_mod(self, btn, dir, name, custom):
        with open(self.json_path, 'r') as f:
            data = json.load(f)

        if self.prev_mod_btn:
            self.prev_mod_btn.configure(border_width=0)

        self.prev_mod_btn = btn
        if custom == True:
            self.dir = data
        if custom == "Curseforge":
            self.dir = f"{self.curseforge_instances_path}\\{dir}"
        if custom == "FTB App":
            self.dir = f"{self.ftb_app_instances_path}\\{dir}"

        self.chosen_mod.configure(text=f"Chosen modpack: {name}")
        btn.configure(border_width=1, border_color="#55ffdd")
    

    def add_essential_to_mod(self):
        try:
            val = Message.askyesno(f"Add essential to mod {self.dir}", f"Are you sure you want to add {self.essential} to the modpack {self.dir}?")
            if val:
                for mod in os.listdir(f"{self.dir}\\mods"):
                    if "Essential-" in mod:
                        os.remove(f"{self.dir}\\mods\\{mod}")

                if "forge" in self.essential:
                    shutil.copy2(
                        src=f"{self.forge_files}\\{self.essential}",
                        dst=f"{self.dir}\\mods"
                        )
                else:
                    shutil.copy2(
                        src=f"{self.fabric_files}\\{self.essential}",
                        dst=f"{self.dir}\\mods"
                    )

                Message.showmsg("Added successfully", "Added essential successfully")
            return
        
        except AttributeError:
            Message.showmsg("ERROR", "Please select a essential version, and a modpack")
            return
        except Exception as e:
            Message.showmsg("ERROR", message=e)