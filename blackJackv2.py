import random
import time

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card in ['J', 'Q', 'K']:
            value += 10
        elif card == 'A':
            value += 11
            aces += 1
        else:
            value += int(card)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def deal_card(deck):
    return deck.pop()

def play_hand(deck, hand, hand_name="Your hand", allow_split=True, split_limit=4, current_splits=1):
    # Recursive split support
    hands = [hand]
    results = []
    i = 0
    splits = current_splits
    while i < len(hands):
        h = hands[i]
        # Only allow split if allowed, under split limit, and hand is a pair
        if allow_split and splits < split_limit and len(h) == 2 and h[0] == h[1]:
            split_choice = input(f"{hand_name} {i+1 if len(hands)>1 else ''} has two {h[0]}'s. Split? (y/n): ").strip().lower()
            if split_choice == 'y':
                hand1 = [h[0], deal_card(deck)]
                hand2 = [h[1], deal_card(deck)]
                print(f"First split hand: {hand1}")
                print(f"Second split hand: {hand2}")
                hands.pop(i)
                hands.insert(i, hand2)
                hands.insert(i, hand1)
                splits += 1
                continue  # Check the new hand at this index for further splits
        # Play the hand
        while True:
            value = calculate_hand_value(h)
            print(f"{hand_name} {i+1 if len(hands)>1 else ''}: {h} (Value: {value})")
            if value > 21:
                print(f"{hand_name} {i+1 if len(hands)>1 else ''} busts!")
                results.append((h, value, 'bust'))
                break
            choice = input(f"{hand_name} {i+1 if len(hands)>1 else ''} - Hit or stand? (h/s): ").strip().lower()
            if choice == 'h':
                card = deal_card(deck)
                h.append(card)
                print(f"You drew: {card}")
            elif choice == 's':
                print(f"{hand_name} {i+1 if len(hands)>1 else ''} stands.")
                results.append((h, value, 'stand'))
                break
            else:
                print("Invalid input. Please enter 'h' or 's'.")
        i += 1
    return results

def play_blackjack():
    # Create a standard 52-card deck
    deck = []
    for rank in [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']:
        deck.extend([rank] * 4)
    random.shuffle(deck)

    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    print(f"Your hand: {player_hand} (Value: {calculate_hand_value(player_hand)})")
    print(f"Dealer shows: {dealer_hand[0]}")

    # Play all hands (with recursive split)
    split_results = play_hand(deck, player_hand, allow_split=True, split_limit=4, current_splits=1)

    # Dealer plays their hand ONCE after all player hands
    print(f"\nDealer's hand: {dealer_hand} (Value: {calculate_hand_value(dealer_hand)})")
    while calculate_hand_value(dealer_hand) < 17:
        card = deal_card(deck)
        dealer_hand.append(card)
        print(f"Dealer draws: {card}")
        print(f"Dealer's hand: {dealer_hand} (Value: {calculate_hand_value(dealer_hand)})")
    dealer_value = calculate_hand_value(dealer_hand)

    # Compare each player hand to the final dealer hand
    if len(split_results) > 1:
        results = []
        for idx, (hand, player_value, status) in enumerate(split_results, 1):
            if status == 'bust':
                print(f"Dealer wins against hand {idx}!")
                results.append('lose')
                continue
            if dealer_value > 21:
                print(f"Dealer busts! You win hand {idx}!")
                results.append('win')
            elif dealer_value > player_value:
                print(f"Dealer wins against hand {idx}!")
                results.append('lose')
            elif dealer_value < player_value:
                print(f"You win hand {idx}!")
                results.append('win')
            else:
                print(f"Hand {idx} is a tie!")
                results.append('tie')
        print(f"\nSplit hand results: {results}")
        return
    # Normal play if not split
    hand, player_value, status = split_results[0]
    if status == 'bust':
        print("Dealer wins!")
        return
    if dealer_value > 21:
        print("Dealer busts! You win!")
    elif dealer_value > player_value:
        print("Dealer wins!")
    elif dealer_value < player_value:
        print("You win!")
    else:
        print("It's a tie!")

def main():
    while True:
        play_blackjack()
        print("\nNext game starts in:", end=" ")
        for i in range(5, 0, -1):
            print(f"{i}", end=" ", flush=True)
            time.sleep(1)
        print("\n")

if __name__ == "__main__":
    main()
