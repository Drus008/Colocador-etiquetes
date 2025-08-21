import pyexiv2
import tkinter as tk
from tkinter import ttk

# Atenció! No funciona si la ruta conté símbols extranys com "ñ", "ó"...

def extract_meta_img(image_path:str) -> dict:
    try:
        # Abrir el archivo de imagen
        image = pyexiv2.Image(image_path)
        data = image.read_exif()
        image.close()

        return data
        

    except Exception as e:
        print(f"Error al leer: {e}. {image_path}")
        return None

def extract_labels_img(image_path: str) -> list[str]:
    dades = extract_meta_img(image_path)
    etiquetes = []
    if dades!=None:
        if "Exif.Image.XPKeywords" in dades:
            dades = dades["Exif.Image.XPKeywords"]
            if dades.endswith('\x00'):
                dades=dades[:-1]
            etiquetes = dades.split(";")
    return etiquetes

def save_labels_img(image_path: str, labels: list[str]) -> None:
    print("Guardant imatge")
    try:
        # Open the image
        with pyexiv2.Image(image_path) as img:
            # Read existing EXIF metadata
            exif_data = img.read_exif()
            
            # Set new keywords
            exif_data['Exif.Image.XPKeywords'] = ";".join(labels)
            
            # Write the modified metadata back to the image
            img.modify_exif(exif_data)
            
            print(f"Successfully updated labels for {image_path}")
            print(f"New labels: {labels}")
            
    except Exception as e:
        print(f"Error: {e}")

class ListboxEtiquetes:
    def __init__(self, parent, options):
        """
        options: List of tuples in format (display_label, value)
        """
        self.parent = parent
        self.tags = set(options)
        self.selected_value = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
       
        # Create frame for listbox and scrollbar
        self.list_frame = ttk.Frame(self.main_frame)
        self.list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create listbox
        self.listbox = tk.Listbox(self.list_frame, height=12, exportselection=False)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
         
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        # Bind listbox selection event
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        self.listbox.bind('<Double-Button-1>', self.on_listbox_double_click)
        
        # Populate listbox with all options initially
        self.update_listbox(self.tags)
        
        # Selected item display
        self.selected_frame = ttk.Frame(self.main_frame)
        self.selected_frame.pack(fill=tk.X, pady=(10, 5))
        
        ttk.Label(self.selected_frame, text="Selected:").pack(side=tk.LEFT)
        self.selected_label = ttk.Label(self.selected_frame, textvariable=self.selected_value, 
                                       foreground="blue", font=('Arial', 10, 'bold'))
        self.selected_label.pack(side=tk.LEFT, padx=(5, 0))
    
    def load_labels(self, dir_img: str):
        tags = extract_labels_img(dir_img)
        self.tags = set(tags)
        self.clear_selection()

    def save_labels(self, dir_img: str):
        print(self.tags)
        save_labels_img(dir_img, list(self.tags))

    def update_listbox(self, items):
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
    
    def add_tag(self, tag: str):
        self.tags.add(tag)
        self.update_listbox(self.tags)

    def add_tags(self, tags):
        self.tags.update(set(tags))
        self.update_listbox(self.tags)
    
    def on_listbox_select(self, event):
        """Handle selection from the listbox"""
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            display_text = self.listbox.get(index)
            self.selected_value.set(display_text)
            
            # Find and store the corresponding value
            for opt in self.tags:
                if opt == display_text:
                    self.selected_value.set(opt)
                    break
    
    def on_listbox_double_click(self, event):
        """Handle double-click selection"""
        self.on_listbox_select(event)
    
    def get_selected_value(self):
        """Get the underlying value of the selected option"""
        return self.selected_value.get()
    
    
    def clear_selection(self):
        """Clear the current selection"""
        self.listbox.selection_clear(0, tk.END)
        self.selected_value.set("")
        self.update_listbox(self.tags)
