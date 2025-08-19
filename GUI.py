import tkinter as tk
from tkinter import filedialog, ttk
from PIL import ImageTk

import os
import json



from dropdown import SearchableListbox
from gestionGUI import ImageViewerBackend
from etiquetes import extract_labels_img, ListboxEtiquetes

class ImageViewerFrontend:
    def __init__(self, root):
        self.root = root
        self.root.title("JPEG Image Viewer with Labels")
        
        # Initialize backend
        self.backend = ImageViewerBackend()
        
        # Create UI
        self.create_widgets()
        
        # Set initial window size
        self.root.geometry("1200x700")
    
    def create_widgets(self):
        """Create all the widgets for the application"""
        # Main container frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        # Frame esquerra (grup visualització)
        frame_visual = tk.Frame(main_frame)
        frame_visual.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame de navegació (botons)
        nav_frame = tk.Frame(frame_visual)
        nav_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botons de navegacio
        self.boto_prev_img = tk.Button(
            nav_frame, text="Previous", command=self.show_previous,
            state=tk.DISABLED
        )
        self.boto_prev_img.pack(side=tk.LEFT, padx=5)
        
        self.boto_next_img = tk.Button(
            nav_frame, text="Next", command=self.show_next,
            state=tk.DISABLED
        )
        self.boto_next_img.pack(side=tk.LEFT, padx=5)
        
        # Folder button
        tk.Button(
            nav_frame, text="Select Folder", command=self.select_folder
        ).pack(side=tk.RIGHT, padx=5)
        
        # Image frame
        self.image_frame = tk.Frame(frame_visual, bg='white')
        self.image_frame.pack(fill=tk.BOTH, expand=True)
        
        # Image label
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        








        # Frame d'etiquetes
        frame_etiquetes = tk.Frame(main_frame, width=600, padx=10)
        frame_etiquetes.pack(side=tk.RIGHT, fill=tk.Y)
        frame_etiquetes.pack_propagate(False)  # Prevent frame from shrinking
        


        # Frame d'edició d'etiquetes

        frame_etiquetar = tk.Frame(frame_etiquetes, width=300, padx=10)
        frame_etiquetar.pack(side=tk.RIGHT, fill=tk.Y)
        frame_etiquetar.pack_propagate(False)  # Prevent frame from shrinking
        
        # Label management section
        label_frame = tk.LabelFrame(frame_etiquetar, text="Gestió d'etiquetes", padx=5, pady=5)
        label_frame.pack(fill=tk.BOTH, expand=True)

        
        # Add label button
        tk.Button(
            label_frame,
            text="Add Label",
        ).pack(fill=tk.X, pady=5)
        

        
        self.selector_tags_disponibles = SearchableListbox(label_frame, [])
        
        # Save button
        tk.Button(
            label_frame,
            text="Save Labels",
        ).pack(fill=tk.X, pady=(10, 0))






        # Frame de visualització d'etiquetes

        frame_dades = tk.Frame(frame_etiquetes, width=300, padx=10)
        frame_dades.pack(side=tk.LEFT, fill=tk.Y)
        frame_dades.pack_propagate(False)  # Prevent frame from shrinking
        
        # Label management section
        label_frame = tk.LabelFrame(frame_dades, text="Dades d'imatge", padx=5, pady=5)
        label_frame.pack(fill=tk.BOTH, expand=True)
        

        # Current labels list with scrollbar
        tk.Label(label_frame, text="Current Labels:").pack(anchor=tk.W)

        self.listbox_tag_img = ListboxEtiquetes(label_frame, [])

    
    def recargar_tags_disponibles(self):
        try:
            if os.path.exists("Etiquetas.json"):
                with open("Etiquetas.json", "r") as f:
                    data = json.load(f)
                    self.selector_tags_disponibles.change_labels(data)
            return True
        except Exception as e:
            print(f"Error loading labels: {str(e)}")
            return False


    def carregar_tags_img(self, dir_img:str):
        tags = extract_labels_img(dir_img)
        self.tags_img_actual = tags
        self.listbox_tag_img.change_labels(tags)


   
    def select_folder(self):
        """Open a dialog to select a folder and load images"""
        folder_path = filedialog.askdirectory(title="Select Folder with JPEG Images")
        if self.backend.load_image_folder(folder_path):
            self.cargar_imagen_actual()
            self.update_status()
            
            # Enable navigation buttons if there are multiple images
            if self.backend.get_image_count() > 1:
                self.boto_next_img.config(state=tk.NORMAL)
                self.boto_prev_img.config(state=tk.NORMAL)
            else:
                self.boto_next_img.config(state=tk.DISABLED)
                self.boto_prev_img.config(state=tk.DISABLED)
        else:
            self.boto_next_img.config(state=tk.DISABLED)
            self.boto_prev_img.config(state=tk.DISABLED)
            self.clear_image()
    





    # Gestió d'imatges


    def mostra_imatge_actual(self):
        """Display the current image"""
        image_path = self.backend.get_current_image_path()
        if image_path:
            image = self.backend.get_resized_image(image_path)
            if image:
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo  # Keep a reference
                self.carregar_tags_img(image_path)
                return
        
        # If we get here, there was an error
        self.clear_image()


    def cargar_imagen_actual(self):
        self.mostra_imatge_actual()
        dir_img = self.backend.get_current_image_path()
        print(dir_img)
        etiquetes = extract_labels_img(dir_img)
        print(etiquetes)
        pass
        
    
    def clear_image(self):
        """Clear the currently displayed image"""
        self.image_label.config(image='')
        self.image_label.image = None
    
    def show_next(self):
        """Show the next image in the folder"""
        if self.backend.next_image():
            self.cargar_imagen_actual()
            self.update_status()
    
    def show_previous(self):
        """Show the previous image in the folder"""
        if self.backend.prev_image():
            self.cargar_imagen_actual()
            self.update_status()
    
    def update_status(self):
        """Update the status label with current position"""
        if self.backend.get_image_count() > 0:
            total = self.backend.get_image_count()
            current = self.backend.get_current_position()



def main():
    root = tk.Tk()
    app = ImageViewerFrontend(root)
    app.recargar_tags_disponibles()
    root.mainloop()


if __name__ == "__main__":
    main()