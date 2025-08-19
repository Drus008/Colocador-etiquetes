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
        self.load_labels()
    
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
    
    # Label handling methods
    def add_label(self, label):
        """Add a label to the current image"""
        if not label or not self.image_files:
            return False
            
        current_image = self.get_current_image_path()
        
        # Add to available labels if it's a new label
        if label not in self.available_labels:
            self.available_labels.append(label)
        
        # Initialize labels for this image if not exists
        if current_image not in self.current_labels:
            self.current_labels[current_image] = []
        
        # Add label if not already present
        if label not in self.current_labels[current_image]:
            self.current_labels[current_image].append(label)
            return True
        return False
    
    def remove_label(self, label):
        """Remove a label from the current image"""
        current_image = self.get_current_image_path()
        if current_image and current_image in self.current_labels and label in self.current_labels[current_image]:
            self.current_labels[current_image].remove(label)
            return True
        return False
    
    def get_current_labels(self):
        """Get labels for the current image"""
        current_image = self.get_current_image_path()
        if current_image and current_image in self.current_labels:
            return self.current_labels[current_image]
        return []
    
    def get_available_labels(self):
        """Get all available labels"""
        return self.available_labels
    
    def filter_labels(self, search_term):
        """Filter available labels based on search term"""
        if not search_term:
            return self.available_labels
        return [label for label in self.available_labels if search_term.lower() in label.lower()]
    
    def save_labels(self):
        """Save all labels to a JSON file"""
        try:
            with open("image_labels.json", "w") as f:
                json.dump({
                    "available_labels": self.available_labels,
                    "image_labels": self.current_labels
                }, f, indent=2)
            return True, "Labels saved successfully"
        except Exception as e:
            return False, f"Error saving labels: {str(e)}"
    
    def load_labels(self):
        """Load labels from JSON file if exists"""
        try:
            if os.path.exists("image_labels.json"):
                with open("image_labels.json", "r") as f:
                    data = json.load(f)
                    self.available_labels = data.get("available_labels", self.available_labels)
                    self.current_labels = data.get("image_labels", {})
            return True
        except Exception as e:
            print(f"Error loading labels: {str(e)}")
            return False