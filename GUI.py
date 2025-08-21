import tkinter as tk
from tkinter import filedialog, ttk
from PIL import ImageTk

import os

from dropdown import SearchableListbox
from gestionGUI import ImageViewerBackend
from etiquetes import extract_labels_img, ListboxEtiquetes
from descripcio import DescipcioImg

class ImageViewerFrontend:
    def __init__(self, root):
        self.root = root
        self.root.title("Etiquetador d'imatges")
        
        # Initialize backend
        self.backend = ImageViewerBackend()
        
        # Create UI
        self.create_widgets()
        
        # Set initial window size
        self.root.geometry("1500x700")
    
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
        self.boto_next_img = tk.Button(
            nav_frame, text="Next", command=self.show_next,
            state=tk.DISABLED
        )
        self.boto_next_img.pack(side=tk.RIGHT, padx=5)

        self.boto_prev_img = tk.Button(
            nav_frame, text="Anterior", command=self.show_previous,
            state=tk.DISABLED
        )
        self.boto_prev_img.pack(side=tk.RIGHT, padx=5)
        
        self.boto_exportar_etiquetes = tk.Button(
            nav_frame, text="Exportar etiquetes", command=self.exportar_etiquetes
        )
        self.boto_exportar_etiquetes.pack(side=tk.RIGHT, padx=5)
        
        # Folder button
        tk.Button(
            nav_frame, text="Select Folder", command=self.select_folder
        ).pack(side=tk.LEFT, padx=5)
        
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
        label_frame_gestio = tk.LabelFrame(frame_etiquetar, text="Gestió d'etiquetes", padx=5, pady=5)
        label_frame_gestio.pack(fill=tk.BOTH, expand=True)

        
        # Add label button
        self.boto_add_tag = tk.Button(
            label_frame_gestio,
            text="Afegir nova etiqueta",
            command=self.afegir_tag_a_img,
            state = tk.DISABLED
        )
        self.boto_add_tag.pack(fill=tk.X, pady=5)
        

        # Listbox d'etiquetes disponibles
        self.selector_tags_disponibles = SearchableListbox(label_frame_gestio, [])
        self.selector_tags_disponibles.listbox.bind('<Double-Button-1>', self.afegir_tag_a_img)
        self.selector_tags_disponibles.load_tags()
        
        


        # Frame de visualització d'etiquetes i descripcio

        frame_dades = tk.Frame(frame_etiquetes, width=300, padx=10)
        frame_dades.pack(side=tk.LEFT, fill=tk.Y)
        frame_dades.pack_propagate(False)  # Prevent frame from shrinking
         
        # Label management section
        label_frame = tk.LabelFrame(frame_dades, text="Dades d'imatge", padx=5, pady=5)
        label_frame.pack(fill=tk.BOTH, expand=True)
        

        # Current labels list with scrollbar
        tk.Label(label_frame, text="Etiquetes de la imatge:").pack(anchor=tk.W)

        self.listbox_tag_img = ListboxEtiquetes(label_frame, [])

        self.text_descipcio = DescipcioImg(label_frame, ancho=300, alto=1)

        # Save button
        self.boto_save_tags = tk.Button(
            label_frame, text="Desa etiquetes",
            state=tk.DISABLED,
            command=self.save_img_meta
        )
        self.boto_save_tags.pack(fill=tk.X, pady=(10, 0))

        self.root.bind('<KeyPress>', self.gestio_tecles)


    def afegir_tag_a_img(self, event=None):
        tag= self.selector_tags_disponibles.get_selected_value()
        if tag == "":
            tag = self.selector_tags_disponibles.add_new_tag()
        self.listbox_tag_img.add_tag(tag)


    def exportar_etiquetes(self):
        self.selector_tags_disponibles.exportar_etiquetes()


    def select_folder(self):
        """Open a dialog to select a folder and load images"""
        folder_path = filedialog.askdirectory(title="Selecciona la capeta amb les imatges JPG")
        if self.backend.load_image_folder(folder_path):
            self.cargar_imagen_actual()
            self.boto_add_tag.config(state=tk.NORMAL)
            self.boto_save_tags.config(state=tk.NORMAL)
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

    def save_img_meta(self):
        img_dir = self.backend.get_current_image_path()
        self.listbox_tag_img.save_labels(img_dir)
        self.text_descipcio.save_descripcio(img_dir)

    def gestio_tecles(self, event):
        if event.state & 0x4 and event.keysym == 's':  # 0x4 is Ctrl modifier
            self.img_acabada()
            self.save_img_meta()
            self.show_next()


    # De moment no fa res, però estaria bé anar desant les imatges ja fetes
    def img_acabada(self):
        pass


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
                self.listbox_tag_img.load_labels(image_path)
                self.text_descipcio.load_descripcio(image_path)
                return
        
        # If we get here, there was an error
        self.clear_image()


    def cargar_imagen_actual(self):
        self.mostra_imatge_actual()
        dir_img = self.backend.get_current_image_path()
        etiquetes = extract_labels_img(dir_img)
        print(etiquetes)
        
    
    def clear_image(self):
        """Clear the currently displayed image"""
        self.image_label.config(image='')
        self.image_label.image = None
    
    def show_next(self):
        """Show the next image in the folder"""
        if self.backend.next_image():
            self.cargar_imagen_actual()
    
    def show_previous(self):
        """Show the previous image in the folder"""
        if self.backend.prev_image():
            self.cargar_imagen_actual()




def main():
    root = tk.Tk()
    app = ImageViewerFrontend(root)
    root.mainloop()


if __name__ == "__main__":
    main()