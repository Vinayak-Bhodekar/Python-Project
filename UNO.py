import random
import os

colors = ["red", "yellow", "green", "blue"]
actions = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "reverse", "skip", "draw_plus_2"]
wild_cards = ["Wild_+4_Card", "Wild_Card"]
action1 = ["reverse", "skip", "draw_plus_2"]
deck = []
# create deck 
def create_deck():
    for color in colors:
        for action in actions:
            card = f"{color} {action}"
            deck.append(card)
            if action != "0":
                deck.append(card)
    for wild in wild_cards:
        deck.extend([wild] * 4)
    return deck
#suffle deck
def shuffle_deck(deck):
    random.shuffle(deck)
# giving cards to player and computer
def distribute_cards(deck):
    player = [deck.pop() for _ in range(7)]
    computer = [deck.pop() for _ in range(7)]
    return player, computer
# choosing color for wild cards
def choose_color(is_computer):
    if is_computer:
        return random.choice(colors)
    color_choices = {1: "red", 2: "yellow", 3: "green", 4: "blue"}
    while True:
        try:
            choice = int(input("CHOOSE YOUR WILD CARD COLOR\n1. Red\n2. Yellow\n3. Green\n4. Blue\nEnter your choice: "))
            if choice in color_choices:
                return color_choices[choice]
            print("Invalid Number. Please choose between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def wild_card_condition(hand,choosed_color):
    legal = []
    for card in hand:
        if card not in wild_cards:
            split_card = card.split(maxsplit=1)
            if len(split_card) == 2:
                color, action = split_card
                if color == choosed_color:
                    legal.append(card)
    return legal

# function gives legal cards every time
def get_legal_cards(hand, discard_pile_top, current_color):
    legal = []
    if discard_pile_top in wild_cards:
        if wild_cards[0] == discard_pile_top:
            return hand
        if wild_cards[1] == discard_pile_top:
            legals = wild_card_condition(hand,current_color)
            return legals
    discard_color, discard_action = current_color, discard_pile_top.split(maxsplit=1)[1]
    for card in hand:
        if card in wild_cards:
            legal.append(card)
        else:
            color, action = card.split(maxsplit=1)
            if color == discard_color or action == discard_action:
                legal.append(card)
    return legal
# takes input from plyer
def player_input(player_hand, legal_cards):
    while True:
        try:
            choice = int(input("Enter the number of the card: "))
            if 1 <= choice <= len(player_hand):
                selected_card = player_hand[choice - 1]
                if selected_card in legal_cards:
                    return selected_card
                print("You cannot play that card. Please choose a valid card.")
            else:
                print("Invalid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
# interface
def interface(player_hand, computer_hand_size, discard_pile, current_color):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"             DISCARD PILE: {discard_pile[-1]} ({current_color})")
    print(f"                       Computer cards: {computer_hand_size}")
    print("\nPlayer cards:\n")
    for i, card in enumerate(player_hand):
        print(f"{i + 1}. {card}")
    print("\nLegal cards: ", get_legal_cards(player_hand, discard_pile[-1], current_color))
# when legal_cards is empty
def draw_card(deck, hand):
    if deck:
        hand.append(deck.pop())
    else:
        print("Deck is empty. No cards to draw.")
# computer pov
def computer_play(hand, discard_pile_top, current_color):
    legal = get_legal_cards(hand, discard_pile_top, current_color)
    if wild_cards[0] in legal:
        return wild_cards[0]
    if wild_cards[1] in legal:
        return wild_cards[1]
    return random.choice(legal) if legal else None
# check all moves
def game_rule(deck, hand, discard_pile, player_no, refer, current_color):
    discard_top = discard_pile[-1]
    if discard_top in wild_cards:
        if discard_top == wild_cards[0]:
            for _ in range(4):
                hand.append(deck.pop())
            refer = 1
        elif discard_top == wild_cards[1]:
            refer = 0
        current_color = choose_color(player_no == 0)
    else:
        color, action = discard_top.split()
        current_color = color
        if action in action1:
            if action == "reverse":
                player_no = (player_no + 1) % 2
            elif action == "skip":
                player_no = (player_no + 1) % 2
            elif action == "draw_plus_2":
                for _ in range(2):
                    hand.append(deck.pop())
                refer = 1
    return player_no, refer, current_color
# setup the discard pile
def discard_pile_setup(deck):
    discard_pile = []
    while True:
        card = deck.pop()
        if card not in wild_cards:
            discard_pile.append(card)
            break
        else:
            deck.insert(0, card)
            shuffle_deck(deck)
    return discard_pile
# delete the card from the plyer and computer deck
def delete_element(hand, card):
    hand.remove(card)
# run whole functions
def gameplay():
    deck = create_deck()
    shuffle_deck(deck)
    player, computer = distribute_cards(deck)
    discard_pile = discard_pile_setup(deck)
    current_color = discard_pile[-1].split()[0]
    player_turn = 1
    refer = 0
    while True:
        if player_turn == 1:
            interface(player, len(computer), discard_pile, current_color)
            legal = get_legal_cards(player, discard_pile[-1], current_color)
            if not legal:
                draw_card(deck, player)
            else:
                selected_card = player_input(player, legal)
                delete_element(player, selected_card)
                discard_pile.append(selected_card)
                player_turn, refer, current_color = game_rule(deck, computer, discard_pile, player_turn, refer, current_color)
        else:
            legal = get_legal_cards(computer, discard_pile[-1], current_color)
            if not legal:
                draw_card(deck, computer)
            else:
                selected_card = computer_play(computer, discard_pile[-1], current_color)
                delete_element(computer, selected_card)
                discard_pile.append(selected_card)
                player_turn, refer, current_color = game_rule(deck, player, discard_pile, player_turn, refer, current_color)
        player_turn = (player_turn + 1) % 2
        if refer:
            player_turn = (player_turn + 1) % 2
            refer = 0
        if not player:
            print("Player wins!")
            break
        if not computer:
            print("Computer wins!")
            break
gameplay()
