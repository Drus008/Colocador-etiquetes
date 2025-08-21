import os
import json
from PIL import Image


class ImageViewerBackend:   
    def __init__(self):
        # Image-related variables
        self.image_files = []
        self.current_index = 0
        self.max_size = (800, 600)  # Maximum display size
        
        # Label-related variables
        self.labels = []
        self.current_labels = {}  # Dictionary to store labels for each image
        self.available_labels = ["Person", "Animal", "Landscape", "Vehicle", "Other"]  # Default labels
        
        # Load labels if saved file exists
    
    # Image handling methods
    def load_image_folder(self, folder_path):
        """Load all JPEG images from the specified folder"""
        if not folder_path:
            return False
            
        self.image_files = [
            os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if f.lower().endswith(('.jpg', '.jpeg'))
        ]
        
        if not self.image_files:
            return False
        
        self.current_index = 0
        return True
    
    def get_current_image_path(self):
        """Get the path of the current image"""
        if not self.image_files or self.current_index >= len(self.image_files):
            return None
        return self.image_files[self.current_index]
    
    def get_resized_image(self, image_path):
        """Load and resize an image for display"""
        try:
            image = Image.open(image_path)
            image.thumbnail(self.max_size, Image.LANCZOS)
            return image
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            return None
    
    def next_image(self):
        """Move to the next image"""
        if not self.image_files:
            return False
        self.current_index = (self.current_index + 1) % len(self.image_files)
        return True
    
    def prev_image(self):
        """Move to the previous image"""
        if not self.image_files:
            return False
        self.current_index = (self.current_index - 1) % len(self.image_files)
        return True
    
    def get_image_count(self):
        """Get total number of images"""
        return len(self.image_files)
    
    def get_current_position(self):
        """Get current image position (1-based index)"""
        return self.current_index + 1
    
