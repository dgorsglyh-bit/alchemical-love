# gui_main.py
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
from data import INGREDIENTS, RECIPES, LOCATIONS, NPCS
from inventory import Inventory
from alchemy_lab import AlchemyLab
from world import World

class HeartAlchemistGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Heart Alchemist - Алхимик Сердец")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        # Game Logic
        self.inventory = Inventory()
        self.world = World(self.inventory)
        self.lab = AlchemyLab(self.inventory)
        
        # Override inventory add/remove for GUI feedback
        self._setup_logic_overrides()

        # UI Styling
        self.bg_color = "#fff0f5" # Lavender Blush
        self.accent_color = "#ff4081" # Pink Accent
        self.text_color = "#4a148c" # Deep Purple
        self.panel_color = "#ffffff"
        
        self.root.configure(bg=self.bg_color)
        
        # Load Images
        self.bg_images = {}
        self.alchemist_images = {}
        self.load_assets()

        # Layout
        self.create_widgets()
        self.animate_shine() # Start shine effect
        self.update_location()

    def set_alchemist_emotion(self, emotion):
        """Changes the alchemist's expression (normal, happy, sad, surprised)"""
        if emotion in self.alchemist_images:
            self.alchemist_label.config(image=self.alchemist_images[emotion])
            # Reset to normal after 3 seconds if not already normal
            if emotion != "normal":
                self.root.after(3000, lambda: self.set_alchemist_emotion("normal"))

    def animate_shine(self):
        # Pulsing effect for the location name
        current_size = 28
        def pulse(step=0):
            size = 28 + (1 if step % 2 == 0 else -1)
            self.canvas.itemconfig(self.loc_label, font=("Playfair Display", size, "bold"))
            self.root.after(1000, lambda: pulse(step + 1))
        pulse()

    def _setup_logic_overrides(self):
        # We wrap the inventory add_item to update the GUI
        original_add = self.inventory.add_item
        def custom_add(item_name):
            original_add(item_name)
            self.update_inventory_display()
            self.set_alchemist_emotion("happy") # Happy when getting item
            # Visual feedback
            self.dialogue_text.config(fg="green")
            self.root.after(1000, lambda: self.dialogue_text.config(fg=self.text_color))
        self.inventory.add_item = custom_add

    def load_assets(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load backgrounds
        for loc_id, loc_data in LOCATIONS.items():
            img_path = os.path.join(script_dir, f"{loc_id}_bg.png")
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path).resize((900, 400), Image.Resampling.LANCZOS)
                    self.bg_images[loc_id] = ImageTk.PhotoImage(img)
                except Exception:
                    self.bg_images[loc_id] = self._create_gradient(loc_id)
            else:
                self.bg_images[loc_id] = self._create_gradient(loc_id)
        
        # Load alchemist portraits
        emotions = ["normal", "happy", "sad", "surprised"]
        assets_dir = os.path.join(script_dir, "assets")
        
        for em in emotions:
            # Look for assets in the assets folder
            target_path = None
            if os.path.exists(assets_dir):
                for f in os.listdir(assets_dir):
                    if f.startswith(f"alchemist_{em}_png") and f.endswith(".png"):
                        target_path = os.path.join(assets_dir, f)
                        break
            
            # Fallback to current directory for legacy support
            if not target_path:
                img_path = os.path.join(script_dir, f"alchemist_{em}.png")
                if os.path.exists(img_path):
                    target_path = img_path

            if target_path:
                try:
                    img = Image.open(target_path).resize((120, 150), Image.Resampling.LANCZOS)
                    self.alchemist_images[em] = ImageTk.PhotoImage(img)
                except Exception:
                    pass
            
            # Placeholder if image missing
            if em not in self.alchemist_images:
                colors = {"normal": "gray", "happy": "yellow", "sad": "blue", "surprised": "orange"}
                placeholder = Image.new('RGB', (120, 150), color=colors.get(em, "white"))
                self.alchemist_images[em] = ImageTk.PhotoImage(placeholder)

    def _create_gradient(self, loc_id):
        # Create a nice gradient if image is missing
        colors = {
            "workshop": ("#f48fb1", "#ad1457"), # Pinkish
            "market": ("#ce93d8", "#6a1b9a"), # Purple
            "park": ("#80deea", "#00838f") # Teal/Blue
        }
        c1, c2 = colors.get(loc_id, ("#ffc107", "#ff8f00"))
        img = Image.new('RGB', (900, 400), color=c1)
        return ImageTk.PhotoImage(img)

    def create_widgets(self):
        # Top Area: Image Canvas
        self.canvas = tk.Canvas(self.root, width=900, height=400, highlightthickness=0)
        self.canvas.pack(side="top")
        self.bg_container = self.canvas.create_image(0, 0, anchor="nw")
        
        # Overlay Rectangle for readability
        self.canvas.create_rectangle(0, 300, 900, 400, fill="black", stipple="gray50", outline="")
        
        # Location Overlay Text
        self.loc_label = self.canvas.create_text(50, 320, anchor="nw", text="", 
                                               fill="white", font=("Playfair Display", 28, "bold"))
        self.desc_label = self.canvas.create_text(50, 360, anchor="nw", text="", 
                                                fill="white", font=("Outfit", 12))
        
        # Alchemist Portrait (Top Left)
        self.alchemist_label = tk.Label(self.root, image=self.alchemist_images["normal"], 
                                       bg="#000", borderwidth=4, relief="flat", highlightthickness=2, highlightbackground=self.accent_color)
        # Place it absolutely over the canvas in the top left
        self.alchemist_label.place(x=20, y=20)

        # Bottom Area: Interaction & Inventory
        bottom_frame = tk.Frame(self.root, bg=self.bg_color, pady=20, padx=20)
        bottom_frame.pack(fill="both", expand=True)

        # left: Dialogue & Actions
        self.dialogue_frame = tk.Frame(bottom_frame, bg="white", relief="flat", padx=15, pady=15)
        self.dialogue_frame.pack(side="left", fill="both", expand=True)
        
        self.npc_name_lbl = tk.Label(self.dialogue_frame, text="", font=("Outfit", 12, "bold"), bg="white", fg=self.accent_color)
        self.npc_name_lbl.pack(anchor="nw")
        
        self.dialogue_text = tk.Label(self.dialogue_frame, text="Welcome, Apprentice.", wraplength=450, 
                                     justify="left", font=("Outfit", 11), bg="white", fg=self.text_color)
        self.dialogue_text.pack(anchor="nw", pady=10)

        self.action_btn_frame = tk.Frame(self.dialogue_frame, bg="white")
        self.action_btn_frame.pack(fill="x", side="bottom")

        # Right: Inventory & Movement
        right_frame = tk.Frame(bottom_frame, bg=self.bg_color, width=250)
        right_frame.pack(side="right", fill="y", padx=(20, 0))

        tk.Label(right_frame, text="INVENTORY", font=("Outfit", 10, "bold"), bg=self.bg_color, fg=self.accent_color).pack(anchor="nw")
        self.inv_box = tk.Text(right_frame, height=8, width=25, font=("Outfit", 10), state="disabled", bg="#fff5f8", relief="flat")
        self.inv_box.pack(pady=5)

        self.move_btn = tk.Button(right_frame, text="MOVE", command=self.show_move_options, 
                                 bg=self.accent_color, fg="white", font=("Outfit", 10, "bold"), 
                                 relief="flat", pady=8, width=20, activebackground="#ff80ab", activeforeground="white")
        self.move_btn.pack(pady=5)
        
        self.lab_btn = tk.Button(right_frame, text="ALCHEMY LAB", command=self.open_lab, 
                                bg="#ffd54f", fg="#5d4037", font=("Outfit", 10, "bold"), 
                                relief="flat", pady=8, width=20, activebackground="#fff176")
        # Only visible in workshop
        
    def update_location(self):
        loc_id = self.world.current_location_id
        loc_data = LOCATIONS[loc_id]
        
        # Update Canvas
        self.canvas.itemconfig(self.bg_container, image=self.bg_images[loc_id])
        self.canvas.itemconfig(self.loc_label, text=loc_data["name"])
        self.canvas.itemconfig(self.desc_label, text=loc_data["description"])
        
        # Update NPC visibility
        self.update_npc_panel()
        
        # Lab visibility
        if loc_id == "workshop":
            self.lab_btn.pack(pady=5)
        else:
            self.lab_btn.pack_forget()
            
        # React to travel
        if hasattr(self, 'last_loc'):
             if self.last_loc != loc_id:
                 self.set_alchemist_emotion("surprised")
        self.last_loc = loc_id

    def update_npc_panel(self):
        # Clear previous action buttons
        for widget in self.action_btn_frame.winfo_children():
            widget.destroy()

        npc_id = None
        for nid, data in NPCS.items():
            if data["location"] == self.world.current_location_id:
                npc_id = nid
                break
        
        if npc_id:
            npc = NPCS[npc_id]
            self.npc_name_lbl.config(text=npc["name"])
            self.dialogue_text.config(text=f"A visitor approaches.")
            
            btn = tk.Button(self.action_btn_frame, text=f"Talk to {npc['name']}", 
                           command=lambda n=npc_id: self.talk_to_npc(n),
                           bg=self.bg_color, fg=self.accent_color, relief="flat", font=("Outfit", 10))
            btn.pack(side="left", padx=5)
        else:
            self.npc_name_lbl.config(text="")
            self.dialogue_text.config(text="The area is quiet.")

    def talk_to_npc(self, npc_id):
        npc = NPCS[npc_id]
        self.dialogue_text.config(text=npc["dialogue"])
        
        for widget in self.action_btn_frame.winfo_children():
            widget.destroy()

        if npc_id == "sage":
            if not self.world.flags["sage_talked"]:
                btn = tk.Button(self.action_btn_frame, text="Receive Gift", 
                               command=self._sage_gift, bg=self.accent_color, fg="white")
                btn.pack(side="left")
            elif "Trust" in self.inventory.items and not "Support" in self.inventory.items:
                btn = tk.Button(self.action_btn_frame, text="Ask about Support", 
                               command=self._sage_support, bg=self.accent_color, fg="white")
                btn.pack(side="left")
            elif "Care" in self.inventory.items and not "Trust" in self.inventory.items:
                btn = tk.Button(self.action_btn_frame, text="Ask about Trust", 
                               command=self._sage_trust, bg=self.accent_color, fg="white")
                btn.pack(side="left")
            else:
                self.dialogue_text.config(text=npc["quest_hint"])

        elif npc_id == "florist":
            tk.Button(self.action_btn_frame, text=npc["options"]["1"], 
                      command=self._florist_help, bg=self.accent_color, fg="white").pack(side="left", padx=2)
            tk.Button(self.action_btn_frame, text=npc["options"]["2"], 
                      command=self._florist_chat, bg="white").pack(side="left", padx=2)
            if self.world.flags["florist_greeted"] and not "Respect" in self.inventory.items:
                 tk.Button(self.action_btn_frame, text="Help more", 
                      command=self._florist_respect, bg="#81d4fa").pack(side="left", padx=2)

        elif npc_id == "trickster":
            if not self.world.flags["puzzle_solved"]:
                self.dialogue_text.config(text=f"RIDDLE: {npc['puzzle']}")
                self.puzzle_entry = tk.Entry(self.action_btn_frame)
                self.puzzle_entry.pack(side="left", padx=5)
                tk.Button(self.action_btn_frame, text="Solve", command=self._solve_puzzle).pack(side="left")
                self.set_alchemist_emotion("surprised") # Puzzled/Thinking
            elif not "Patience" in self.inventory.items:
                tk.Button(self.action_btn_frame, text="Wait for a gift", 
                      command=self._trickster_patience, bg="#a5d6a7").pack(side="left", padx=2)
            else:
                self.dialogue_text.config(text="'You've already outsmarted me!'")

    def _sage_gift(self):
        self.inventory.add_item("Sincerity")
        self.world.flags["sage_talked"] = True
        self.set_alchemist_emotion("happy")
        self.update_npc_panel()

    def _sage_trust(self):
        self.inventory.add_item("Trust")
        self.set_alchemist_emotion("happy")
        self.update_npc_panel()

    def _sage_support(self):
        self.inventory.add_item("Support")
        self.set_alchemist_emotion("happy")
        self.update_npc_panel()

    def _florist_help(self):
        if not self.world.flags["florist_greeted"]:
            self.inventory.add_item("Care")
            self.inventory.add_item("Attention")
            self.world.flags["florist_greeted"] = True
            self.set_alchemist_emotion("happy")
        self.dialogue_text.config(text="'Wonderful! Care and Attention are vital for any heart alchemist.'")
        self.update_npc_panel()

    def _florist_respect(self):
        self.dialogue_text.config(text="'To earn my Respect, unscramble this word related to relationships: V-O-E-L'")
        for widget in self.action_btn_frame.winfo_children():
            widget.destroy()
        
        self.scramble_entry = tk.Entry(self.action_btn_frame)
        self.scramble_entry.pack(side="left", padx=5)
        tk.Button(self.action_btn_frame, text="Unscramble", command=self._solve_scramble).pack(side="left")

    def _solve_scramble(self):
        ans = self.scramble_entry.get().lower().strip()
        if ans == "love":
            self.inventory.add_item("Respect")
            messagebox.showinfo("Respect Earned", "The Florist is impressed!")
            self.set_alchemist_emotion("happy") # Added emotion for scramble success
        else:
            messagebox.showwarning("Not quite", "Try again! It's a very famous four-letter word.")
            self.set_alchemist_emotion("sad") # Added emotion for scramble failure
        self.update_npc_panel()

    def _trickster_patience(self):
        self.dialogue_text.config(text="'Wait for it... wait for it...'")
        self.set_alchemist_emotion("surprised") # Watching closely
        self.root.after(3000, self._give_patience)

    def _give_patience(self):
        self.inventory.add_item("Patience")
        messagebox.showinfo("Wait Over", "The Trickster rewards your Patience!")
        self.set_alchemist_emotion("happy")
        self.update_npc_panel()

    def _solve_puzzle(self):
        ans = self.puzzle_entry.get().lower().strip()
        if ans == "keyboard":
            self.inventory.add_item("Humor")
            self.inventory.add_item("Passion")
            self.world.flags["puzzle_solved"] = True
            self.set_alchemist_emotion("happy")
            messagebox.showinfo("Correct!", "Trickster gives you Humor and Passion!")
        else:
            self.inventory.add_item("Conflict")
            self.set_alchemist_emotion("sad")
            messagebox.showwarning("Wrong", "The Trickster laughs and tosses a Conflict stone at you.")
        self.update_npc_panel()

    def show_move_options(self):
        loc = self.world.get_current_location()
        move_win = tk.Toplevel(self.root)
        move_win.title("Travel")
        move_win.geometry("300x200")
        
        tk.Label(move_win, text="Where to go?", font=("Outfit", 12)).pack(pady=10)
        for conn in loc["connections"]:
            btn = tk.Button(move_win, text=LOCATIONS[conn]["name"], 
                           command=lambda c=conn: [self.world.move(c), self.update_location(), move_win.destroy()])
            btn.pack(pady=5, fill="x", padx=20)

    def open_lab(self):
        lab_win = tk.Toplevel(self.root)
        lab_win.title("Alchemy Lab")
        lab_win.geometry("400x500")
        
        tk.Label(lab_win, text="Brew a Potion", font=("Outfit", 14, "bold")).pack(pady=10)
        
        for name, data in RECIPES.items():
            frame = tk.Frame(lab_win, pady=10)
            frame.pack(fill="x", padx=20)
            
            tk.Label(frame, text=name, font=("Outfit", 11, "bold")).pack(anchor="nw")
            tk.Label(frame, text=f"Ingredients: {', '.join(data['ingredients'])}", font=("Outfit", 9), wraplength=350).pack(anchor="nw")
            
            btn = tk.Button(frame, text="BREW", command=lambda n=name: self.attempt_brew(n, lab_win))
            btn.pack(anchor="ne")

    def attempt_brew(self, potion_name, lab_win):
        recipe = RECIPES[potion_name]
        if self.inventory.has_ingredients(recipe["ingredients"]):
            self.inventory.consume_ingredients(recipe["ingredients"])
            messagebox.showinfo("Success!", f"Successfully brewed {potion_name}!\n\n{recipe['description']}")
            self.update_inventory_display()
            if potion_name == "True Love":
                messagebox.showinfo("The End", "CONGRATULATIONS!\nYou have found True Love and finished the game!")
                self.root.destroy()
            self.set_alchemist_emotion("happy")
            lab_win.destroy()
        else:
            self.set_alchemist_emotion("sad")
            messagebox.showerror("Failed", "You lack the necessary ingredients.")

    def update_inventory_display(self):
        self.inv_box.config(state="normal")
        self.inv_box.delete("1.0", "end")
        for item, count in self.inventory.items.items():
            self.inv_box.insert("end", f"• {item}: x{count}\n")
        self.inv_box.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = HeartAlchemistGUI(root)
    root.mainloop()
