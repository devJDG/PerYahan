import random
import time

def calculate_hand_value(hand):
    value = 0
    for card in hand:
        if card in ['J', 'Q', 'K']:
            value += 0
        elif card == 'A':
            value += 1
        else:
            value += int(card)
    return value % 10

def determine_winner(player_hand, banker_hand):
    player_value = calculate_hand_value(player_hand)
    banker_value = calculate_hand_value(banker_hand)

    if player_value > banker_value:
        return "Player wins"
    elif banker_value > player_value:
        return "Banker wins"
    else:
        return "Tie"

def play_baccarat():
    deck = [str(i) for i in range(2, 10)] + ['A', 'J', 'Q', 'K'] * 4
    random.shuffle(deck)

    player_hand = []
    banker_hand = []

    # Deal initial two cards
    for _ in range(2):
        player_hand.append(deck.pop())
        banker_hand.append(deck.pop())

    print("Player hand:", player_hand, "Value:", calculate_hand_value(player_hand))
    print("Banker hand:", banker_hand, "Value:", calculate_hand_value(banker_hand))

    # Player draws a third card if their total is 5 or less
    player_value = calculate_hand_value(player_hand)
    if player_value <= 5:
        choice = input(f"Your total is {player_value}. Draw a third card? (y/n): ").strip().lower()
        if choice == 'y':
            player_hand.append(deck.pop())
            print("You drew:", player_hand[-1])
        else:
            print("You chose to stand.")
    else:
        print("You cannot draw a third card.")

    # Banker draws a third card based on the rules
    banker_value = calculate_hand_value(banker_hand)
    if banker_value <= 5:
        banker_hand.append(deck.pop())
        print("Banker draws a third card.")
    else:
        print("Banker stands.")

    # Show final hands
    print("\nFinal hands:")
    print("Player hand:", player_hand, "Value:", calculate_hand_value(player_hand))
    print("Banker hand:", banker_hand, "Value:", calculate_hand_value(banker_hand))

    # Determine the winner
    winner = determine_winner(player_hand, banker_hand)
    print("Result:", winner)

def main():
    while True:
        play_baccarat()
        print("\nNext game starts in:", end=" ")
        for i in range(5, 0, -1):
            print(f"{i}", end=" ", flush=True)
            time.sleep(1)
        print("\n")

if __name__ == "__main__":
    main()
