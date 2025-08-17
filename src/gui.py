import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from card_generator import create_card_game_zip
from html_card_generator import get_available_templates

class CardGameGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Game Generator")
        self.root.geometry("650x550")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Card Game Generator", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Theme input
        ttk.Label(main_frame, text="Theme:", font=('Arial', 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.theme_var = tk.StringVar()
        theme_entry = ttk.Entry(main_frame, textvariable=self.theme_var, font=('Arial', 12), width=30)
        theme_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Number of cards
        ttk.Label(main_frame, text="Number of Cards:", font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.num_cards_var = tk.StringVar(value="5")
        num_cards_spinbox = ttk.Spinbox(main_frame, from_=1, to=20, textvariable=self.num_cards_var, 
                                       font=('Arial', 12), width=10)
        num_cards_spinbox.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Template selection
        ttk.Label(main_frame, text="Card Template:", font=('Arial', 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.template_var = tk.StringVar()
        
        # Get available templates
        self.templates = get_available_templates()
        # Filter templates to only include 'Bright Swiss Design' and 'Detailed Representation'
        allowed_templates = ["bright_swiss", "detailed"]
        filtered_templates = {k: v for k, v in self.templates.items() if k in allowed_templates}
        self.templates = filtered_templates
        template_names = [info["name"] for info in self.templates.values()]
        template_ids = list(self.templates.keys())
        
        # Create template selection frame
        template_frame = ttk.Frame(main_frame)
        template_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        template_frame.columnconfigure(0, weight=1)
        
        self.template_combo = ttk.Combobox(template_frame, textvariable=self.template_var, 
                                          values=template_names, state="readonly", font=("Arial", 11))
        self.template_combo.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Set default template to 'Bright Swiss Design' if available
        if "Bright Swiss Design" in template_names:
            self.template_combo.set("Bright Swiss Design")
        elif template_names:
            self.template_combo.set(template_names[0])
        
        # Template info button
        info_button = ttk.Button(template_frame, text="Info", command=self.show_template_info, width=6)
        info_button.grid(row=0, column=1)
        
        # Output directory
        ttk.Label(main_frame, text="Output Directory:", font=('Arial', 12)).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.output_dir_var = tk.StringVar(value=os.path.join(os.path.dirname(os.path.dirname(__file__)), "output"))
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var, font=('Arial', 10))
        output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_button = ttk.Button(output_frame, text="Browse", command=self.browse_output_dir)
        browse_button.grid(row=0, column=1)
        
        # Generate button
        self.generate_button = ttk.Button(main_frame, text="Generate Card Game", 
                                         command=self.generate_cards, style='Accent.TButton')
        self.generate_button.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to generate cards...")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=('Arial', 10))
        status_label.grid(row=7, column=0, columnspan=2, pady=5)
        
        # Results text area
        ttk.Label(main_frame, text="Generation Log:", font=('Arial', 12, 'bold')).grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(9, weight=1)
        
        self.log_text = tk.Text(text_frame, height=8, width=60, font=('Consolas', 9))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Example themes
        examples_frame = ttk.LabelFrame(main_frame, text="Example Themes", padding="10")
        examples_frame.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        example_themes = ["Fantasy", "Sci-Fi", "Medieval", "Cyberpunk", "Steampunk", "Horror", "Space", "Pirates"]
        for i, theme in enumerate(example_themes):
            btn = ttk.Button(examples_frame, text=theme, 
                           command=lambda t=theme: self.theme_var.set(t))
            btn.grid(row=i//4, column=i%4, padx=5, pady=2, sticky=tk.W)
    
    def show_template_info(self):
        """Show information about the selected template"""
        selected_name = self.template_var.get()
        if not selected_name:
            return
        
        # Find template by name
        selected_template = None
        selected_id = None
        for template_id, template_info in self.templates.items():
            if template_info["name"] == selected_name:
                selected_template = template_info
                selected_id = template_id
                break
        
        if selected_template:
            info_text = f"Template: {selected_template['name']}\n\n"
            info_text += f"Description: {selected_template['description']}\n\n"
            
            if selected_id == "bright_swiss":
                info_text += "Features:\n"
                info_text += "• Bright yellow and blue color scheme\n"
                info_text += "• Bold, modern typography\n"
                info_text += "• Distinct header and footer sections\n"
                info_text += "• Image with luminosity blend mode"
            elif selected_id == "detailed":
                info_text += "Features:\n"
                info_text += "• Ornate, detailed frame design\n"
                info_text += "• Textured background elements\n"
                info_text += "• Prominent name bar\n"
                info_text += "• Integrated stats and description area"
            
            messagebox.showinfo("Template Information", info_text)
    def get_selected_template_id(self):
        """Get the ID of the currently selected template"""
        selected_name = self.template_var.get()
        for template_id, template_info in self.templates.items():
            if template_info["name"] == selected_name:
                return template_id
        return "classic"  # Default fallback
    def browse_output_dir(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def log_message(self, message):
        """Add message to log text widget"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def progress_callback(self, message, current, total):
        """Callback function for progress updates"""
        progress_percent = (current / total) * 100
        self.progress_var.set(progress_percent)
        self.status_var.set(message)
        self.log_message(f"[{current}/{total}] {message}")
        self.root.update_idletasks()
    
    def generate_cards(self):
        """Generate card game in a separate thread"""
        theme = self.theme_var.get().strip()
        if not theme:
            messagebox.showerror("Error", "Please enter a theme!")
            return
        
        try:
            num_cards = int(self.num_cards_var.get())
            if num_cards < 1 or num_cards > 20:
                messagebox.showerror("Error", "Number of cards must be between 1 and 20!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of cards!")
            return
        
        template_id = self.get_selected_template_id()
        
        output_dir = self.output_dir_var.get()
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output directory: {e}")
                return
        
        # Disable generate button
        self.generate_button.config(state='disabled')
        self.progress_var.set(0)
        self.log_text.delete(1.0, tk.END)
        
        # Start generation in separate thread
        thread = threading.Thread(target=self._generate_cards_thread, 
                                 args=(theme, output_dir, num_cards, template_id))
        thread.daemon = True
        thread.start()
    
    def _generate_cards_thread(self, theme, output_dir, num_cards, template_id):
        """Thread function for card generation"""
        try:
            template_name = self.templates[template_id]["name"]
            
            self.log_message(f"Starting generation of {num_cards} cards for theme: {theme}")
            self.log_message(f"Template: {template_name}")
            self.log_message(f"Output directory: {output_dir}")
            self.log_message("-" * 50)
            
            zip_file = create_card_game_zip(theme, output_dir, num_cards, template_id, self.progress_callback)
            
            self.log_message("-" * 50)
            self.log_message(f"SUCCESS! Card game generated: {zip_file}")
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                f"Card game generated successfully!\\n\\nTemplate: {template_name}\\nFile: {os.path.basename(zip_file)}\\nLocation: {os.path.dirname(zip_file)}"))
            
        except Exception as e:
            error_msg = f"Error generating cards: {str(e)}"
            self.log_message(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            # Re-enable generate button
            self.root.after(0, lambda: self.generate_button.config(state='normal'))

def main():
    root = tk.Tk()
    app = CardGameGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

