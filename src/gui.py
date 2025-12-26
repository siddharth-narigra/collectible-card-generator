"""
Card Game Generator GUI Module

This module provides a graphical user interface for the Card Game Generator
application using Tkinter.
"""

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from card_generator import create_card_game_zip
from html_card_generator import get_available_templates


# =============================================================================
# Constants
# =============================================================================

WINDOW_TITLE = "Card Game Generator"
WINDOW_SIZE = "650x550"
FONT_TITLE = ('Arial', 18, 'bold')
FONT_LABEL = ('Arial', 12)
FONT_ENTRY = ('Arial', 12)
FONT_LOG = ('Consolas', 9)

MIN_CARDS = 1
MAX_CARDS = 20
DEFAULT_CARDS = 5

EXAMPLE_THEMES = [
    "Fantasy", "Sci-Fi", "Medieval", "Cyberpunk",
    "Steampunk", "Horror", "Space", "Pirates"
]


# =============================================================================
# Main GUI Class
# =============================================================================

class CardGameGeneratorGUI:
    """Main GUI application for the Card Game Generator."""
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the GUI application.
        
        Args:
            root: The Tkinter root window
        """
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(True, True)
        
        # Variables
        self.theme_var = tk.StringVar()
        self.num_cards_var = tk.StringVar(value=str(DEFAULT_CARDS))
        self.template_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready to generate cards...")
        
        # Template data
        self.templates = self._load_templates()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Set default output directory
        default_output = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
        self.output_dir_var.set(default_output)
        
        # Build UI
        self._setup_ui()
    
    def _load_templates(self) -> dict:
        """Load and filter available templates."""
        all_templates = get_available_templates()
        # Only include the supported templates
        allowed = ["bright_swiss", "detailed"]
        return {k: v for k, v in all_templates.items() if k in allowed}
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        self._create_header(main_frame)
        self._create_inputs(main_frame)
        self._create_progress_section(main_frame)
        self._create_log_section(main_frame)
        self._create_examples_section(main_frame)
    
    def _create_header(self, parent: ttk.Frame) -> None:
        """Create the title header."""
        title = ttk.Label(parent, text="Card Game Generator", font=FONT_TITLE)
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
    
    def _create_inputs(self, parent: ttk.Frame) -> None:
        """Create the input fields."""
        row = 1
        
        # Theme input
        ttk.Label(parent, text="Theme:", font=FONT_LABEL).grid(
            row=row, column=0, sticky="w", pady=5
        )
        theme_entry = ttk.Entry(parent, textvariable=self.theme_var, font=FONT_ENTRY, width=30)
        theme_entry.grid(row=row, column=1, sticky="ew", pady=5, padx=(10, 0))
        row += 1
        
        # Number of cards
        ttk.Label(parent, text="Number of Cards:", font=FONT_LABEL).grid(
            row=row, column=0, sticky="w", pady=5
        )
        num_spinbox = ttk.Spinbox(
            parent,
            from_=MIN_CARDS,
            to=MAX_CARDS,
            textvariable=self.num_cards_var,
            font=FONT_ENTRY,
            width=10
        )
        num_spinbox.grid(row=row, column=1, sticky="w", pady=5, padx=(10, 0))
        row += 1
        
        # Template selection
        ttk.Label(parent, text="Card Template:", font=FONT_LABEL).grid(
            row=row, column=0, sticky="w", pady=5
        )
        template_frame = ttk.Frame(parent)
        template_frame.grid(row=row, column=1, sticky="ew", pady=5, padx=(10, 0))
        template_frame.columnconfigure(0, weight=1)
        
        template_names = [info["name"] for info in self.templates.values()]
        self.template_combo = ttk.Combobox(
            template_frame,
            textvariable=self.template_var,
            values=template_names,
            state="readonly",
            font=FONT_ENTRY
        )
        self.template_combo.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Set default template
        if "Bright Swiss Design" in template_names:
            self.template_combo.set("Bright Swiss Design")
        elif template_names:
            self.template_combo.set(template_names[0])
        
        info_btn = ttk.Button(template_frame, text="Info", command=self._show_template_info, width=6)
        info_btn.grid(row=0, column=1)
        row += 1
        
        # Output directory
        ttk.Label(parent, text="Output Directory:", font=FONT_LABEL).grid(
            row=row, column=0, sticky="w", pady=5
        )
        output_frame = ttk.Frame(parent)
        output_frame.grid(row=row, column=1, sticky="ew", pady=5, padx=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var, font=('Arial', 10))
        output_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        browse_btn = ttk.Button(output_frame, text="Browse", command=self._browse_output_dir)
        browse_btn.grid(row=0, column=1)
        row += 1
        
        # Generate button
        self.generate_button = ttk.Button(
            parent,
            text="Generate Card Game",
            command=self._generate_cards
        )
        self.generate_button.grid(row=row, column=0, columnspan=2, pady=20)
    
    def _create_progress_section(self, parent: ttk.Frame) -> None:
        """Create the progress bar and status label."""
        self.progress_bar = ttk.Progressbar(
            parent,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5)
        
        status_label = ttk.Label(parent, textvariable=self.status_var, font=('Arial', 10))
        status_label.grid(row=7, column=0, columnspan=2, pady=5)
    
    def _create_log_section(self, parent: ttk.Frame) -> None:
        """Create the log text area."""
        ttk.Label(parent, text="Generation Log:", font=('Arial', 12, 'bold')).grid(
            row=8, column=0, columnspan=2, sticky="w", pady=(20, 5)
        )
        
        text_frame = ttk.Frame(parent)
        text_frame.grid(row=9, column=0, columnspan=2, sticky="nsew", pady=5)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        parent.rowconfigure(9, weight=1)
        
        self.log_text = tk.Text(text_frame, height=8, width=60, font=FONT_LOG)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
    
    def _create_examples_section(self, parent: ttk.Frame) -> None:
        """Create the example themes section."""
        examples_frame = ttk.LabelFrame(parent, text="Example Themes", padding="10")
        examples_frame.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        for i, theme in enumerate(EXAMPLE_THEMES):
            btn = ttk.Button(
                examples_frame,
                text=theme,
                command=lambda t=theme: self.theme_var.set(t)
            )
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=2, sticky="w")
    
    # =========================================================================
    # Event Handlers
    # =========================================================================
    
    def _show_template_info(self) -> None:
        """Display information about the selected template."""
        selected_name = self.template_var.get()
        if not selected_name:
            return
        
        for template_id, info in self.templates.items():
            if info["name"] == selected_name:
                features = self._get_template_features(template_id)
                message = (
                    f"Template: {info['name']}\n\n"
                    f"Description: {info['description']}\n\n"
                    f"Features:\n{features}"
                )
                messagebox.showinfo("Template Information", message)
                return
    
    def _get_template_features(self, template_id: str) -> str:
        """Get feature list for a template."""
        features = {
            "bright_swiss": (
                "• Bright yellow and blue color scheme\n"
                "• Bold, modern typography\n"
                "• Distinct header and footer sections\n"
                "• Image with luminosity blend mode"
            ),
            "detailed": (
                "• Ornate, detailed frame design\n"
                "• Textured background elements\n"
                "• Prominent name bar\n"
                "• Integrated stats and description area"
            ),
        }
        return features.get(template_id, "No features available.")
    
    def _get_selected_template_id(self) -> str:
        """Get the ID of the currently selected template."""
        selected_name = self.template_var.get()
        for template_id, info in self.templates.items():
            if info["name"] == selected_name:
                return template_id
        return "bright_swiss"
    
    def _browse_output_dir(self) -> None:
        """Open a directory browser dialog."""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def _log_message(self, message: str) -> None:
        """Add a message to the log area."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def _progress_callback(self, message: str, current: int, total: int) -> None:
        """Handle progress updates from the generator."""
        progress_percent = (current / total) * 100 if total > 0 else 0
        self.progress_var.set(progress_percent)
        self.status_var.set(message)
        self._log_message(f"[{current}/{total}] {message}")
    
    def _generate_cards(self) -> None:
        """Validate inputs and start card generation."""
        theme = self.theme_var.get().strip()
        if not theme:
            messagebox.showerror("Error", "Please enter a theme!")
            return
        
        try:
            num_cards = int(self.num_cards_var.get())
            if not MIN_CARDS <= num_cards <= MAX_CARDS:
                messagebox.showerror("Error", f"Number of cards must be between {MIN_CARDS} and {MAX_CARDS}!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of cards!")
            return
        
        output_dir = self.output_dir_var.get()
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                messagebox.showerror("Error", f"Could not create output directory: {e}")
                return
        
        template_id = self._get_selected_template_id()
        
        # Prepare UI for generation
        self.generate_button.config(state='disabled')
        self.progress_var.set(0)
        self.log_text.delete(1.0, tk.END)
        
        # Start generation thread
        thread = threading.Thread(
            target=self._generation_thread,
            args=(theme, output_dir, num_cards, template_id),
            daemon=True
        )
        thread.start()
    
    def _generation_thread(
        self,
        theme: str,
        output_dir: str,
        num_cards: int,
        template_id: str
    ) -> None:
        """Background thread for card generation."""
        try:
            template_name = self.templates[template_id]["name"]
            
            self._log_message(f"Starting generation of {num_cards} cards for theme: {theme}")
            self._log_message(f"Template: {template_name}")
            self._log_message(f"Output directory: {output_dir}")
            self._log_message("-" * 50)
            
            zip_file = create_card_game_zip(
                theme,
                output_dir,
                num_cards,
                template_id,
                self._progress_callback
            )
            
            self._log_message("-" * 50)
            self._log_message(f"SUCCESS! Card game generated: {zip_file}")
            
            # Show success message on main thread
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Card game generated successfully!\n\n"
                f"Template: {template_name}\n"
                f"File: {os.path.basename(zip_file)}\n"
                f"Location: {os.path.dirname(zip_file)}"
            ))
            
        except Exception as e:
            error_msg = f"Error generating cards: {e}"
            self._log_message(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            self.root.after(0, lambda: self.generate_button.config(state='normal'))


# =============================================================================
# Entry Point
# =============================================================================

def main() -> None:
    """Launch the Card Game Generator GUI."""
    root = tk.Tk()
    CardGameGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
