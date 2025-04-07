import tkinter as tk
import os
from tkinter import ttk
import controller
import observer
# ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 3 | Token
import random
# ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 3 | Token

# ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 6 | Screen
class SetupScreen:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.window = tk.Toplevel(root)
        self.window.title("Monopoly Setup")
        
        # Default values
        self.num_players = 2
        self.player_info = []  # Will store (name, token) tuples directly
        self.current_widgets = []  # To track current widgets
        self.house_rules = {
            "free_parking_payout": False,
            "auction_properties": False,
            "double_salary_on_go": False
        }
        
        self._create_widgets()
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Player count selection
        ttk.Label(main_frame, text="Number of Players (2-8):").grid(row=0, column=0, sticky="w")
        self.player_count = tk.IntVar(value=2)
        ttk.Spinbox(main_frame, from_=2, to=8, textvariable=self.player_count,
                   command=self._update_player_fields).grid(row=0, column=1, sticky="ew")
        
        # Player info frame
        self.player_frame = ttk.Frame(main_frame)
        self.player_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")
        
        # House rules
        ttk.Label(main_frame, text="House Rules:").grid(row=2, column=0, sticky="w", pady=(10,0))
        
        self.free_parking_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Free Parking collects all taxes", 
                       variable=self.free_parking_var).grid(row=3, column=0, sticky="w")
        
        self.auction_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Auction unowned properties", 
                       variable=self.auction_var).grid(row=4, column=0, sticky="w")
        
        self.double_salary_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Double salary for landing on Go", 
                       variable=self.double_salary_var).grid(row=5, column=0, sticky="w")
        
        # Start button
        ttk.Button(main_frame, text="Start Game", command=self._start_game).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Initialize player fields
        self._update_player_fields()
    
    def _update_player_fields(self):
        # Clear existing widgets and info
        for widget in self.current_widgets:
            widget.destroy()
        self.current_widgets = []
        self.player_info = []  # Clear previous player info
        
        # Create new fields for each player
        tokens = ["🎩 Top Hat", "👢 Boot", "🐈 Cat", "🛳️ Battleship", 
                 "🚗 Racecar", "🎙️ Thimble", "🛞 Wheelbarrow", "🔨 Iron"]
        used_tokens = []
        
        for i in range(self.player_count.get()):
            # Name entry
            ttk.Label(self.player_frame, text=f"Player {i+1} Name:").grid(row=i, column=0, sticky="w")
            name_entry = ttk.Entry(self.player_frame)
            name_entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.current_widgets.append(name_entry)
            
            # Token selection
            ttk.Label(self.player_frame, text="Token:").grid(row=i, column=2, sticky="w", padx=5)
            token_var = tk.StringVar()
            available_tokens = [t for t in tokens if t not in used_tokens]
            if not available_tokens:
                available_tokens = tokens  # Reset if we run out of unique tokens
            token_var.set(available_tokens[0])
            used_tokens.append(available_tokens[0])
            
            token_menu = ttk.OptionMenu(self.player_frame, token_var, *available_tokens)
            token_menu.grid(row=i, column=3, sticky="ew", padx=5)
            self.current_widgets.append(token_menu)
            
            # Store the StringVar and Entry directly
            self.player_info.append((name_entry, token_var))
    
    def _start_game(self):
        # Collect player info from current widgets
        players = []
        for i in range(self.player_count.get()):
            if i < len(self.player_info):
                name_entry, token_var = self.player_info[i]
                try:
                    name = name_entry.get() or f"Player {i+1}"
                    token = token_var.get().split()[0]  # Get just the emoji
                    players.append((name, token))
                except tk.TclError:
                    # Fallback if widget was destroyed
                    players.append((f"Player {i+1}", random.choice(["🎩", "👢", "🐈", "🛳️", "🚗", "🎙️", "🛞", "🔨"])))
        
        # Collect house rules
        self.house_rules = {
            "free_parking_payout": self.free_parking_var.get(),
            "auction_properties": self.auction_var.get(),
            "double_salary_on_go": self.double_salary_var.get()
        }
        
        self.window.destroy()
        self.callback(players, self.house_rules)

# ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 6 | Screen

def get_board_square_images():
    """return a List of all the file paths for the board square images"""
    square_images = []
    for i in range(40):
        path = os.path.join("resources", "images", "properties", f"{i}.png")
        square_images.append(path)
    return square_images

class View (observer.Observer):
    """Class to create the GUI for the Monopoly game"""
    width = 1280
    height = 720

    def __init__(self, root):
        super().__init__()
        # Set-up a simple window
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 5 | Move Token
        self.player_tokens = {}
        self.token_offset = 0
        self.board_image = None
        self.board_label = None
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 5 | Move Token

        self.images = []
        self.root = root
        root.title("Monopoly 1920")

        #tight coupling with the controller
        #not ideal, but we will refactor later
        #self.controller = controller

        root.geometry(f'{self.width}x{self.height}')
        root.resizable(False, False)

        self.main_frame = ttk.Frame(root, padding=10, relief='groove')

        #create the frames
        logo_frame = self._create_logo_frame()
        middle_frame = self._create_middle_frame()
        msg_frame = self._create_msg_frame()

        #pack the frames
        logo_frame.pack(fill=tk.BOTH, expand=True)
        middle_frame.pack(fill=tk.BOTH, expand=False)
        msg_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self._add_listeners()

        #self.setup_game()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 5 | Move Token
    def _calculate_board_position(self, space_index):
        """Calculate screen coordinates for a given board space index"""
        if not self.board_label:
            return 0, 0

        corner_spaces = {0: "Go", 10: "Jail", 20: "Free Parking", 30: "Go To Jail"}
              
        # Get the board's screen position
        board_x = self.board_label.winfo_rootx()+10
        board_y = self.board_label.winfo_rooty()-35
        board_width = self.board_label.winfo_width()
        board_height = self.board_label.winfo_height()

        # Calculate positions based on space index
        segment_length = board_width // 10
        if 0 <= space_index <= 10:
            x = board_x + board_width - (space_index * segment_length) - segment_length//2
            y = board_y + board_height - 20
        elif 11 <= space_index <= 20:
            x = board_x + 20
            y = board_y + board_height - ((space_index-10) * segment_length) - segment_length//2
        elif 21 <= space_index <= 30:
            x = board_x + ((space_index-20) * segment_length) - segment_length//2
            y = board_y + 20
        else:
            x = board_x + board_width - 20
            y = board_y + ((space_index-30) * segment_length) - segment_length//2

        if y == 381:
            x -= 10
        
        if y == 583:
            x += 10
            y -= 35

        if x == 143:
            x -= 20
            y -= 10

        if x == 133:
            x -= 10
            y -= 10
        

        print(x,y)
        x += random.randint(-3, 3)
        y += random.randint(-3, 3) # this is to make sure tokens don't overlap
        return x, y
    
    def _update_player_tokens(self, players):
        """Update all player tokens on the board with proper size accounting"""
        # Remove all existing tokens
        for token in self.player_tokens.values():
            token.place_forget()
        
        space_counts = {}
        
        for player in players:
            if player.bankrupt_declared:
                continue
                
            pos = player.position
            space_counts[pos] = space_counts.get(pos, 0) + 1
            offset = self.token_offset * (space_counts[pos] - 1)
            
            x, y = self._calculate_board_position(pos)
            
            # Adjust for token size (assuming tokens are roughly 20x20 pixels)
            token_size = 20
            x += offset - token_size//2
            y += offset - token_size//2
            
            x -= 1
            y -= 1
            if player.name not in self.player_tokens:
                # Create a styled label for the token
                token_label = ttk.Label(
                    self.main_frame, 
                    text=player.token, 
                    font=("Arial", 12),
                    relief='solid',
                    width=2,
                    anchor='center'
                )
                self.player_tokens[player.name] = token_label
            else:
                token_label = self.player_tokens[player.name]
                
            token_label.place(x=x, y=y)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 5 | Move Token

    # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 4 | Multiplayer
    def get_player_count(self):
        """Number of players (2-8)."""
        from tkinter import simpledialog
        while True:
            num = simpledialog.askinteger(
                "Player Count",
                "How many players? (2-8)",
                parent=self.root,
                minvalue=2,
                maxvalue=8
            )
            if num:  # If user didn't cancel
                return num
            return 2
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 4 | Multiplayer
    def _add_listeners(self):
        """Add listeners to the view"""
        self.observe("update_state_box", self.update_state_box)
        self.observe("update_card", self.update_card)
        self.observe("update_state", self._update_text)
        self.observe("choice", self._choose)


    def _create_middle_frame(self):
        """Create the middle frame of the GUI"""
        middle_frame = ttk.Frame(self.main_frame, padding=10)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 5 | Move Token
        self.board_image = tk.PhotoImage(file=r"resources/images/monopoly.png")
        self.board_label = ttk.Label(middle_frame, image=self.board_image)
        self.board_label.pack(side='left', anchor='n', padx=75)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 5 | Move Token

        # preload all the images for the board squares
        self._preload_images()

        card_image = self.images[0]
        self.card = ttk.Label(middle_frame, image=card_image)

        button_frame = ttk.Frame(middle_frame, padding=10)

        #create buttons
        self.mid_buttons = []
        self.roll_button = ttk.Button(button_frame, text="Roll Dice", command=lambda: self._action_taken("roll") )
        self.roll_button.pack(side='top', anchor='center', pady=(10, 10))
        self.mid_buttons.append(self.roll_button)

        self.purchase_button = ttk.Button(button_frame, text="Purchase", command=lambda: self._action_taken("purchase"))
        self.purchase_button.pack(side='top', anchor='center', pady=(10, 10))
        self.purchase_button.state(['active'])
        self.mid_buttons.append(self.purchase_button)

        self.mortgage_button = ttk.Button(button_frame, text="Mortgage", command=lambda: self._action_taken("mortgage"))
        self.mortgage_button.pack(side='top', anchor='center', pady=(10, 10))
        self.mortgage_button.state(['active'])
        self.mid_buttons.append(self.mortgage_button)

        self.unmortgage_button = ttk.Button(button_frame, text="Unmortgage", command=lambda: self._action_taken("unmortgage"))
        self.unmortgage_button.pack(side='top', anchor='center', pady=(10, 10))
        self.unmortgage_button.state(['active'])
        self.mid_buttons.append(self.unmortgage_button)

        self.bankrupt_button = ttk.Button(button_frame, text="Go Bankrupt", command=lambda: self._action_taken("bankrupt"))
        self.bankrupt_button.pack(side='top', anchor='center', pady=(10, 10))
        self.bankrupt_button.state(['active'])
        self.mid_buttons.append(self.bankrupt_button)

        self.end_turn_button = ttk.Button(button_frame, text="End Turn", command=lambda: self._action_taken("end_turn"))
        self.end_turn_button.pack(side='top', anchor='center', pady=(10, 10))
        self.end_turn_button.state(['active'])
        self.mid_buttons.append(self.end_turn_button)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 1 | Jail        
        self.pay_jail_button = ttk.Button(button_frame, text="Pay Jail Fine", command=lambda: self._action_taken("pay_jail"))
        self.pay_jail_button.pack(side='top', anchor='center', pady=(10, 10))
        self.mid_buttons.append(self.pay_jail_button)

        self.use_jail_card_button = ttk.Button(button_frame, text="Use Jail Card", command=lambda: self._action_taken("use_jail_card"))
        self.use_jail_card_button.pack(side='top', anchor='center', pady=(10, 10))
        self.mid_buttons.append(self.use_jail_card_button)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 1 | Jail

        button_frame.pack(side='left', anchor='center', pady=(0, 0), padx=50)

        self.card.pack(side='left', anchor='n', padx=100, pady=(100, 0))
        self.card.image = card_image



        return middle_frame

    def _create_msg_frame(self):
        """Create the frame at the bottom of the screen to display messages"""
        msg_frame = ttk.Frame(self.main_frame, padding=10, relief='raised', borderwidth=3)

        self.state_box = tk.Text(msg_frame, width=60, height=10, background='black', foreground='white')
        self.state_box.pack(side='left', padx=(100,30))

        self.text_box = tk.Text(msg_frame, width=60, height=10, background='black', foreground='white')
        self.text_box.pack(side='left', padx=(30,100))

        return msg_frame

    def _create_logo_frame(self):
        """Create the frame at the top of the screen to display the logo"""
        logo_frame = ttk.Frame(self.main_frame, padding=10)
        # load a logo resource
        logo_image = tk.PhotoImage(file=r"resources/images/monopoly_logo.png")
        logo = ttk.Label(logo_frame, image=logo_image)
        logo.pack(side='top', anchor='n')
        logo.image = logo_image

        return logo_frame

    def _action_taken(self, action):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 1 | Jail
        if action == "pay_jail":
            observer.Event("pay_jail", None)
        if action == "use_jail_card":
            observer.Event("use_jail_card", None)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 1 | Jail

        if action == "roll":
            #tell the controller roll was clicked
            print("roll clicked")
            observer.Event("roll", None)

        if action == "purchase":
            observer.Event("purchase", None)

        if action == "mortgage":
            observer.Event("mortgage", None)

        if action == "unmortgage":
            observer.Event("unmortgage", None)

        if action == "mortgage_specific":
            observer.Event("mortgage_specific", 0)

        if action == "end_turn":
            #self.text_box.delete(1.0, tk.END)
            observer.Event("end_turn", self._clear_text)

    def update_state(self, state, text):
        """Function to update the state of the game"""
        if state == "roll":
            self._await_roll(text)
        elif state == "purchase":
            self._await_purchase()
        elif state == "moves":
            self._await_moves()
        elif state == "moves_or_bankrupt":
            self._await_moves_or_bankrupt()

    def purchase(self):
        observer.Event("purchase", None)

    def update_card(self, index):
        card_image = self.images[index]
        try:
            self.card['image'] = card_image
        except:
            pass

    def _clear_text(self):
        print("clearing text")
        self.text_box.delete(1.0, tk.END)

    def _update_text(self, text=""):
        #self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, text+"\n")

    def update_state_box(self, text=""):
        self.state_box.delete(1.0, tk.END)
        self.state_box.insert(tk.END, text)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 5 | Move Token
        if hasattr(self, '_gameboard'):
            self._update_player_tokens([self._gameboard.get_current_player()] + self._gameboard._GameBoard__players)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 5 | Move Token

    def _choose(self, choices):
        #good idea disable all buttons

        self.popup_menu = tk.Menu(self.root,
                                       tearoff=0)

        for c in choices:
            self.popup_menu.add_command(label=c,
                                        command=lambda ch=c: self.pick(ch))
        self.popup_menu.add_separator()

        lbl = "Cancel"
        if len(choices) == 0:
                lbl = "No properties to mortgage (click to cancel)"

        self.popup_menu.add_command(label=lbl,
                                    command=self.popup_menu.grab_release)
        try:
            self.popup_menu.tk_popup(600, 300, 0)
        finally:
            self.popup_menu.grab_release()

    def pick(self, s):
        observer.Event("mortgage_specific", s)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 3 | Token
    def get_player_info(self, player_num):
        """name and token"""
        from tkinter import Toplevel, ttk, StringVar
        tokens = ["🎩 Top Hat", "👢 Boot", "🐈 Cat", "🛳️ Battleship", 
                "🚗 Racecar", "🎙️ Thimble", "🛞 Wheelbarrow", "🔨 Iron"]
        
        dialog = Toplevel(self.root)
        dialog.title(f"Player {player_num}")
        
        ttk.Label(dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Token:").grid(row=1, column=0, padx=5, pady=5)
        token_var = StringVar()
        token_var.set(tokens[0])
        token_dropdown = ttk.Combobox(dialog, textvariable=token_var, values=tokens)
        token_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        result = [None, None]
        
        def on_ok():
            result[0] = name_entry.get() or f"Player {player_num}"
            result[1] = token_var.get().split()[0]
            dialog.destroy()
        
        ttk.Button(dialog, text="OK", command=on_ok).grid(row=2, columnspan=2)
        
        dialog.wait_window()
        return result[0], result[1]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 3 | Token

    def _preload_images(self):
        '''Function to preload all the images for the board squares'''
        square_images = get_board_square_images()
        for image in square_images:
            img = tk.PhotoImage(file=image)
            self.images.append(img)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 2 | Player name
    def get_player_name(self, player_num):
        """Prompt player to enter name"""
        from tkinter import simpledialog
        name = simpledialog.askstring(f"Player {player_num}", f"Enter name for Player {player_num}:", parent=self.root)
        return name
    # ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 2 | Player name
# ~~~~~~~~~~~~~~~~~~~~~~~~~ start task 6 | Screen
'''launch the GUI'''
if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    
    def start_game(players, house_rules):
        root.deiconify()
        from controller import Controller  # Import here to avoid circular imports
        game_controller = Controller(root, players, house_rules)  # Use different variable name
    
    setup = SetupScreen(root, start_game)
    root.mainloop()
# ~~~~~~~~~~~~~~~~~~~~~~~~~ end task 6 | Screen