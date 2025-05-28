import random
import time

def load_words(filename="words.txt"):
    with open(filename, "r") as file:
        words = file.read().splitlines()
    return words

def typing_test(words):
    print("Type the following words as fast as you can:")
    input("Press Enter to start...")
    
    start_time = time.time()
    correct_count = 0
    total_words = len(words)

    for word in words:
        print(word, end=" ", flush=True)
        user_input = input()
        if user_input == word:
            correct_count += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    words_per_minute = (total_words / elapsed_time) * 60
    accuracy = (correct_count / total_words) * 100

    print("\n--- Results ---")
    print(f"Time: {elapsed_time:.2f} seconds")
    print(f"Words per minute: {words_per_minute:.2f}")
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    word_list = load_words()
    if not word_list:
      print("Error: words.txt file not found or empty. Please create a 'words.txt' file in the same directory.")
    else:
        random_words = random.sample(word_list, 10)
        typing_test(random_words)
