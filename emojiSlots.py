import tkinter as tk
from tkinter import messagebox
import random

# --- Constants ---
INITIAL_BALANCE = 100
MIN_BET = 1
MAX_BET = 100 # Or can be a percentage of balance

# Symbols and their payout multipliers (for 3 of a kind)
SYMBOLS = {
    "🍒": 2,
    "🍊": 3,
    "🍉": 4,
    "⭐": 5,
    "🔔": 10,
    "💎": 20
}

# List of symbols for easier random selection
SYMBOL_KEYS = list(SYMBOLS.keys())
NUM_REELS = 3

class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emoji Slot Machine")
        self.root.geometry("450x400") # Adjusted size for better layout
        self.root.resizable(False, False)

        self.balance = INITIAL_BALANCE

        # --- UI Elements ---
        # Frame for reels
        reel_frame = tk.Frame(root, pady=10)
        reel_frame.pack()

        self.reel_labels = []
        for i in range(NUM_REELS):
            label = tk.Label(reel_frame, text="❓", font=("Arial", 60), width=2, relief="sunken", borderwidth=2)
            label.pack(side=tk.LEFT, padx=10)
            self.reel_labels.append(label)

        # Frame for controls
        control_frame = tk.Frame(root, pady=10)
        control_frame.pack()

        tk.Label(control_frame, text="Bet:", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.bet_var = tk.StringVar(value=str(MIN_BET))
        self.bet_entry = tk.Entry(control_frame, textvariable=self.bet_var, width=5, font=("Arial", 14))
        self.bet_entry.grid(row=0, column=1, padx=5, pady=5)

        self.spin_button = tk.Button(control_frame, text="SPIN!", font=("Arial", 16, "bold"), command=self.spin_reels, bg="green", fg="white", width=10, height=2)
        self.spin_button.grid(row=0, column=2, rowspan=2, padx=20, pady=5) # Span 2 rows for larger button

        tk.Label(control_frame, text="Balance:", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.balance_label = tk.Label(control_frame, text=f"${self.balance}", font=("Arial", 14, "bold"), fg="blue")
        self.balance_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Message display
        self.message_label = tk.Label(root, text="Welcome! Place your bet.", font=("Arial", 14), fg="black", pady=10)
        self.message_label.pack()

        self.update_balance_display()

    def update_balance_display(self):
        self.balance_label.config(text=f"${self.balance:.2f}") # Format to 2 decimal places if needed

    def show_message(self, message, color="black"):
        self.message_label.config(text=message, fg=color)

    def spin_reels(self):
        # 1. Get and validate bet
        try:
            bet_amount = int(self.bet_var.get())
        except ValueError:
            self.show_message("Invalid bet amount!", "red")
            return

        if not (MIN_BET <= bet_amount <= MAX_BET):
            self.show_message(f"Bet must be between ${MIN_BET} and ${MAX_BET}.", "red")
            return

        if bet_amount > self.balance:
            self.show_message("Not enough balance!", "red")
            return

        # 2. Deduct bet and spin
        self.balance -= bet_amount
        self.update_balance_display()
        self.show_message("Spinning...", "black")
        self.root.update_idletasks() # Ensure message updates before potential delay

        # Simulate spinning animation (optional, but nice)
        # For a real animation, you'd use after() and update labels repeatedly
        # Here, we'll just show the result directly
        
        current_reels = [random.choice(SYMBOL_KEYS) for _ in range(NUM_REELS)]

        # Update reel displays
        for i in range(NUM_REELS):
            self.reel_labels[i].config(text=current_reels[i])
        
        # 3. Check for win
        winnings, win_message = self.check_win(current_reels, bet_amount)

        if winnings > 0:
            self.balance += winnings
            self.show_message(f"{win_message} You won ${winnings}!", "green")
        else:
            self.show_message("No win this time. Try again!", "orange")

        self.update_balance_display()

        # 4. Check for game over
        if self.balance < MIN_BET:
            self.show_message(f"Game Over! You ran out of money.", "red")
            self.spin_button.config(state=tk.DISABLED)
            self.bet_entry.config(state=tk.DISABLED)
            messagebox.showinfo("Game Over", "You've run out of balance. Thanks for playing!")
            # Optionally, offer a reset button here or close the game.

    def check_win(self, reels, bet):
        """
        Checks for winning combinations.
        Currently only checks for three of a kind.
        """
        # Check for three of a kind
        if reels[0] == reels[1] == reels[2]:
            symbol = reels[0]
            multiplier = SYMBOLS[symbol]
            payout = bet * multiplier
            return payout, f"🎉 Three {symbol}s! 🎉"
        
        # Add more winning conditions if desired (e.g., two cherries, specific sequences)
        # Example: Two Cherries anywhere
        # cherry_count = reels.count("🍒")
        # if cherry_count == 2:
        #     return bet * 1, "Two Cherries!" # Small payout for two cherries
        # if cherry_count == 1 and reels[0] == "🍒": # Cherry on first reel
        #     return bet * 0.5, "One Cherry on first reel!" 

        return 0, ""


if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineApp(root)
    root.mainloop()