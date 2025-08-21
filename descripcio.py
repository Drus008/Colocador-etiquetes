import tkinter as tk
from tkinter import ttk
import pyexiv2
import sys
import os
from tkinter import scrolledtext


def leer_metadatos(archivo:str) -> str:
    try:
        with pyexiv2.Image(archivo) as img:
            # Leer todos los metadatos EXIF
            exif_data = img.read_exif()
            
            # Mostrar metadatos específicos
            print(exif_data)
            descripcion = exif_data.get('Exif.Image.XPComment')
            
            print(f"Descripción: {descripcion}")
            if descripcion:
                return descripcion
            else:
                return ""
            
    except Exception as e:
        print(f"Error: {e}")

def modificar_descripcion(archivo, nueva_descripcion):
    try:
        # Abrir la imagen
        with pyexiv2.Image(archivo) as img:
            # Modificar la descripción (campo Exif.Image.ImageDescription)
            img.modify_exif({'Exif.Image.XPComment': nueva_descripcion})
            print(f"Descripción modificada exitosamente en: {archivo}")
            
    except Exception as e:
        print(f"Error: {e}")


class DescipcioImg:
    def __init__(self, root, ancho=60, alto=20):
        """
        Inicializa el editor de texto
        
        Args:
            root: Ventana principal de tkinter
            titulo: Título de la ventana
            ancho: Ancho del área de texto en caracteres
            alto: Alto del área de texto en líneas
        """
        self.root = root
        
        # Crear el área de texto con scrollbar
        self.crear_widgets(ancho, alto)
        
    
    def crear_widgets(self, ancho, alto):
        """Crea los widgets de la interfaz"""
        # Frame principal
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de texto con scrollbar
        self.texto = scrolledtext.ScrolledText(
            self.frame_principal,
            wrap=tk.WORD,  # Ajuste de palabras
            width=ancho,
            height=alto,
            font=("Arial", 10)
        )
        self.texto.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para botones
        self.frame_botones = tk.Frame(self.frame_principal)
        self.frame_botones.pack(fill=tk.X, pady=5)
        
    
    def obtener_texto(self):
        """Obtiene todo el texto del editor"""
        return self.texto.get("1.0", tk.END).strip()
    
    def establecer_texto(self, contenido):
        """Establece el texto en el editor"""
        self.limpiar_texto()
        self.texto.insert("1.0", contenido)
    
    def limpiar_texto(self):
        """Limpia todo el texto del editor"""
        self.texto.delete("1.0", tk.END)
    
    def save_descripcio(self, dir_img: str):
        """Guarda el texto en un archivo"""
        contenido = self.obtener_texto()
        modificar_descripcion(dir_img, contenido)
    
    def load_descripcio(self, dir_img:str):
        text_metadades = leer_metadatos(dir_img)
        self.establecer_texto(text_metadades)

# Ejemplo de uso
if __name__ == "__main__":
    print(leer_metadatos(r"C:\Users\druss\Desktop\Guardar disco\Fotos x etiquetar\20231222_201913.jpg"))
    root = tk.Tk()
    
    # Crear instancia del editor
    editor = DescipcioImg(
        root, 
        ancho=70, 
        alto=15
    )
    
    # Establecer texto inicial (opcional)
    texto_inicial = """Este es un párrafo de texto editable.
Puedes escribir lo que quieras aquí.

Características:
- Texto editable
- Scroll automático
- Botones para limpiar, guardar y cargar
- Atajos de teclado (Ctrl+S, Ctrl+L)"""

    editor.establecer_texto(texto_inicial)
    
    root.mainloop()