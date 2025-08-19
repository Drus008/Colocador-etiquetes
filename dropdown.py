import tkinter as tk
from tkinter import ttk

class SearchableListbox:
    def __init__(self, parent, options):
        """
        options: List of tuples in format (display_label, value)
        """
        self.parent = parent
        self.options = options.copy()
        self.selected_value = tk.StringVar()
        self.selected_display = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
       
        # Create search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.main_frame, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, pady=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.filter_options)
        
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
        self.update_listbox([opt for opt in self.options])
        
        # Selected item display
        self.selected_frame = ttk.Frame(self.main_frame)
        self.selected_frame.pack(fill=tk.X, pady=(10, 5))
        
        ttk.Label(self.selected_frame, text="Selected:").pack(side=tk.LEFT)
        self.selected_label = ttk.Label(self.selected_frame, textvariable=self.selected_display, 
                                       foreground="blue", font=('Arial', 10, 'bold'))
        self.selected_label.pack(side=tk.LEFT, padx=(5, 0))
    
    def change_labels(self, options):
        self.options = options.copy()
        self.clear_selection()

    def update_listbox(self, items):
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
    
    def filter_options(self, event):
        """Filter options based on user input - only show items that start with the input"""
        # Ignore navigation keys
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Shift_L', 'Shift_R', 
                           'Control_L', 'Control_R', 'Alt_L', 'Alt_R'):
            return
        
        typed = self.search_var.get().lower()
        
        if typed == '':
            # Show all options if search field is empty
            filtered = [opt for opt in self.options]
        else:
            # Filter options that start with the typed text (case insensitive)
            filtered = [
                opt for opt in self.options 
                if opt.lower().startswith(typed)
            ]
        
        # Update the listbox with filtered results
        self.update_listbox(filtered)
    
    def on_listbox_select(self, event):
        """Handle selection from the listbox"""
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            display_text = self.listbox.get(index)
            self.selected_display.set(display_text)
            
            # Find and store the corresponding value
            for opt in self.options:
                if opt == display_text:
                    self.selected_value.set(opt)
                    break
    
    def on_listbox_double_click(self, event):
        """Handle double-click selection"""
        self.on_listbox_select(event)
    
    def get_selected_value(self):
        """Get the underlying value of the selected option"""
        return self.selected_value.get()
    
    def get_selected_display(self):
        """Get the display text of the selected option"""
        return self.selected_display.get()
    
    def clear_selection(self):
        """Clear the current selection"""
        self.listbox.selection_clear(0, tk.END)
        self.selected_display.set("")
        self.selected_value.set("")
        self.search_var.set("")
        self.update_listbox([opt for opt in self.options])


comida = ["Apple", "Banana", "Blueberry", "Blackberry", "Cherry", "Coconut", "Grape", 
            "Lemon", "Lime", "Mango", "Orange", "Peach", "Pear", "Pineapple", "Strawberry",
            "Artichoke", "Asparagus", "Broccoli", "Carrot", "Cauliflower", "Celery",
                "Corn", "Cucumber", "Eggplant", "Garlic", "Ginger", "Lettuce", "Onion",
                "Pepper", "Potato", "Pumpkin", "Radish", "Spinach", "Tomato", "Zucchini",
            "Beef", "Chicken", "Duck", "Lamb", "Pork", "Turkey", "Venison"]


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Searchable Listbox")
    root.geometry("500x500")
    
    
    # Create the searchable listbox
    searchable_list = SearchableListbox(root, comida)
    
    # Control buttons frame
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)
    
    # Button to show selected value
    def show_selection():
        selected_display = searchable_list.get_selected_display()
        selected_value = searchable_list.get_selected_value()
        if selected_display:
            print(f"Selected: {selected_display} (Value: {selected_value})")
        else:
            print("No selection made")
    
    show_btn = ttk.Button(button_frame, text="Show Selection", command=show_selection)
    show_btn.pack(side=tk.LEFT, padx=5)
    
    # Button to clear selection
    clear_btn = ttk.Button(button_frame, text="Clear Selection", command=searchable_list.clear_selection)
    clear_btn.pack(side=tk.LEFT, padx=5)
    
    # Instructions
    instructions = tk.Label(root, 
                          text="• Type in the search box to filter options\n"
                               "• Only items starting with your input will be shown\n"
                               "• Click an item to select it\n"
                               "• Double-click to select and confirm", 
                          justify=tk.LEFT, fg="gray", font=('Arial', 9))
    instructions.pack(pady=10, padx=10, anchor=tk.W)
    
    root.mainloop()


