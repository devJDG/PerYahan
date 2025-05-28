import ttkbootstrap as tk
from tkinter import scrolledtext, messagebox
import time
import random

def generate_text(num_words=50):
    """
    Generates a random passage of common English words for the typing test.
    """
    words = [
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
        "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
        "person", "into", "year", "your", "good", "some", "could", "them", "see", "other",
        "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
        "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
        "even", "new", "want", "because", "any", "these", "give", "day", "most", "us",
        "has", "had", "did", "was", "were", "is", "are", "been", "very", "much",
        "many", "where", "why", "before", "down", "should", "through", "write", "right", "read",
        "find", "found", "call", "tell", "ask", "need", "feel", "mean", "leave", "put",
        "keep", "let", "begin", "seem", "help", "talk", "start", "run", "move", "play",
        "turn", "live", "believe", "hold", "bring", "happen", "provide", "set", "sit", "stand",
        "lose", "pay", "meet", "include", "continue", "learn", "change", "lead", "understand", "watch",
        "follow", "stop", "create", "speak", "allow", "add", "spend", "grow", "open", "walk",
        "win", "offer", "remember", "consider", "appear", "buy", "wait", "serve", "die", "send",
        "expect", "build", "stay", "fall", "cut", "reach", "kill", "remain", "suggest", "raise",
        "pass", "sell", "require", "report", "decide", "pull", "drive", "break", "receive", "agree",
        "return", "explain", "hope", "develop", "carry", "occur", "catch", "draw", "choose", "teach",
        "deal", "wish", "enter", "sign", "point", "act", "express", "prove", "improve", "maintain",
        "control", "manage", "avoid", "protect", "present", "discuss", "discover", "force", "prevent", "accept"
    ]
    random.shuffle(words)
    return ' '.join(words[:num_words])

def calculate_results(original_text, typed_text, time_taken):
    """
    Calculates the Words Per Minute (WPM) and accuracy.
    """
    correct_chars = 0
    for i in range(min(len(original_text), len(typed_text))):
        if original_text[i] == typed_text[i]:
            correct_chars += 1

    total_chars_original = len(original_text)
    accuracy = (correct_chars / total_chars_original) * 100 if total_chars_original > 0 else 0
    wpm = (correct_chars / 5) / (time_taken / 60) if time_taken > 0 else 0
    return wpm, accuracy

class TypingTestGUI:
    def __init__(self, master):
        self.master = master
        master.title("Monkey Type GUI")

        master.geometry("1000x750") # Slightly increased height to accommodate the new button

        self.passage = ""
        self.start_time = None
        self.test_started = False
        self.wpm = 0
        self.accuracy = 0
        self.elapsed_time = 0
        self.larger_font = ('Helvetica', 18) # Store font as instance attribute

        self.info_label = tk.tk.Label(master, text=self.get_current_info(), font=self.larger_font)
        self.info_label.pack(pady=10)
        self.update_info_display()

        self.instruction_label = tk.tk.Label(master, text="Click 'Start' to begin the typing test.", font=self.larger_font)
        self.instruction_label.pack(pady=15)

        self.passage_display = scrolledtext.ScrolledText(master, wrap=tk.tk.WORD, height=9, font=self.larger_font, state=tk.tk.DISABLED) # Increased height
        self.passage_display.pack(padx=20, pady=15, fill=tk.tk.BOTH, expand=True) # Fill and expand
        self.passage_display.tag_config("typed_correct", foreground="green")
        self.passage_display.tag_config("typed_incorrect", foreground="red")

        self.typing_area = scrolledtext.ScrolledText(master, wrap=tk.tk.WORD, height=9, font=self.larger_font) # Increased height
        self.typing_area.pack(padx=20, pady=15, fill=tk.tk.BOTH, expand=True) # Fill and expand
        self.typing_area.bind("<KeyPress>", self.start_timer)
        self.typing_area.bind("<KeyRelease>", self.check_typing)

        # Style for buttons
        style = tk.Style()
        style.configure('Larger.TButton', font=self.larger_font, padding=(10, 10))

        self.start_button = tk.Button(master, text="Start", command=self.start_test, bootstyle="primary", style='Larger.TButton')
        self.start_button.pack(pady=10)

        self.restart_button = tk.Button(master, text="Restart", command=self.restart_test, bootstyle="secondary", style='Larger.TButton')
        self.restart_button.pack(pady=10)
        self.restart_button.config(state=tk.tk.DISABLED) # Initially disabled

        self.results_label = tk.tk.Label(master, text="", font=('Helvetica', 20, 'bold')) # Increased font size
        self.results_label.pack(pady=15)

    def get_current_info(self):
        time_str = f"Time: {self.elapsed_time:.1f}s" if self.start_time else "Time: 0.0s"
        wpm_str = f"WPM: {self.wpm:.2f}"
        accuracy_str = f"Accuracy: {self.accuracy:.2f}%"
        return f"{time_str} | {wpm_str} | {accuracy_str}"

    def update_info_display(self):
        self.info_label.config(text=self.get_current_info())
        self.master.after(100, self.update_info_display)

    def start_test(self):
        self.passage = generate_text(num_words=50)
        self.passage_display.config(state=tk.tk.NORMAL)
        self.passage_display.delete(1.0, tk.tk.END)
        self.passage_display.insert(tk.tk.END, self.passage)
        self.passage_display.config(state=tk.tk.DISABLED)

        self.typing_area.delete(1.0, tk.tk.END)
        self.typing_area.config(state=tk.tk.NORMAL)
        self.typing_area.focus_set()

        self.start_button.config(state=tk.tk.DISABLED)
        self.restart_button.config(state=tk.tk.NORMAL) # Enable restart button
        self.results_label.config(text="")
        self.start_time = None
        self.test_started = False
        self.wpm = 0
        self.accuracy = 0
        self.elapsed_time = 0
        self.typing_area.bind("<KeyPress>", self.start_timer)
        self.typing_area.bind("<KeyRelease>", self.check_typing)
        self.colorize_typed_text()

    def restart_test(self):
        self.typing_area.config(state=tk.tk.NORMAL)
        self.typing_area.delete(1.0, tk.tk.END)
        self.start_button.config(state=tk.tk.NORMAL)
        self.restart_button.config(state=tk.tk.DISABLED)
        self.results_label.config(text="")
        self.start_time = None
        self.test_started = False
        self.wpm = 0
        self.accuracy = 0
        self.elapsed_time = 0
        self.typing_area.unbind("<KeyPress>")
        self.typing_area.unbind("<KeyRelease>")
        self.passage_display.config(state=tk.tk.NORMAL)
        self.passage_display.delete(1.0, tk.tk.END)
        self.passage_display.config(state=tk.tk.DISABLED)
        self.instruction_label.config(text="Click 'Start' to begin the typing test.", font=self.larger_font)
        self.update_info_display() # Reset time, WPM, Accuracy in the info label

    def start_timer(self, event):
        if not self.test_started:
            self.start_time = time.time()
            self.test_started = True
            self.typing_area.unbind("<KeyPress>")

    def check_typing(self, event=None):
        if self.test_started and self.start_time:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
            typed_text = self.typing_area.get("1.0", tk.tk.END).strip()
            if self.elapsed_time > 0:
                self.wpm, self.accuracy = calculate_results(self.passage, typed_text, self.elapsed_time)
            self.colorize_typed_text(typed_text)

            if len(typed_text) >= len(self.passage):
                self.end_test(typed_text)
            elif typed_text == self.passage:
                self.end_test(typed_text)

    def colorize_typed_text(self, typed=""):
        self.passage_display.config(state=tk.tk.NORMAL)
        self.passage_display.delete(1.0, tk.tk.END)
        self.passage_display.insert(tk.tk.END, self.passage)

        for i, char in enumerate(typed):
            if i < len(self.passage):
                if char == self.passage[i]:
                    self.passage_display.tag_add("typed_correct", f"1.{i}", f"1.{i+1}")
                else:
                    self.passage_display.tag_add("typed_incorrect", f"1.{i}", f"1.{i+1}")
            else:
                self.passage_display.tag_add("typed_incorrect", f"1.{i}", f"1.{i+1}")

        self.passage_display.config(state=tk.tk.DISABLED)

    def end_test(self, typed_text):
        end_time = time.time()
        time_taken = end_time - self.start_time
        wpm, accuracy = calculate_results(self.passage, typed_text, time_taken)
        self.wpm = wpm
        self.accuracy = accuracy
        self.results_label.config(text=f"Time: {time_taken:.2f}s | WPM: {self.wpm:.2f} | Accuracy: {self.accuracy:.2f}%", font=('Helvetica', 20, 'bold'))
        self.start_button.config(state=tk.tk.NORMAL)
        self.restart_button.config(state=tk.tk.NORMAL) # Enable restart after test ends
        self.typing_area.config(state=tk.tk.DISABLED)
        self.typing_area.unbind("<KeyRelease>")

if __name__ == "__main__":
    root = tk.Window(themename="flatly")
    gui = TypingTestGUI(root)
    root.mainloop()