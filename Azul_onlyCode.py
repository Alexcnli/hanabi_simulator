import random
import os

MAX_HINT = 8
MAX_MISTAKE = 3
MAX_POINT = 25
PLAYER_RANGE = {2,3,4,5}

COLOR_LIST = ['red', 'green', 'blue', 'yellow', 'white']
COLOR_MAP = {
    'r': 'red',
    'g': 'green',
    'b': 'blue',
    'y': 'yellow',
    'w': 'white'
}

# input validation function
def valid_int(dialog, valid_set):
    while True:
        try:
            user_input = int(input(dialog).strip()) # Prompt user for input
            if user_input in valid_set:
                return user_input
        except: pass
        
# input validation function
def valid_input(dialog, valid_set):
    while True:
        user_input = input(dialog).strip().lower() # Prompt user for input
        if user_input in valid_set:
            return user_input
            
class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number
        self.is_color_hinted = False
        self.is_number_hinted = False

    def hint_color(self):
        self.is_color_hinted = True

    def hint_number(self):
        self.is_number_hinted = True

    def __repr__(self):
        return f"{self.color}_{self.number}"
    
class Deck:
    def __init__(self):
        self.deck = []
        self.create_deck()  # Automatically create the deck when an instance is initialized

    def create_deck(self):
        for color in COLOR_LIST:
            self.deck.extend([Card(color, i) for i in [1]*3 + [2]*2 + [3]*2 + [4]*2 + [5]])
        random.shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop() if self.deck else None  # Pop the last card from the deck

    def deck_size(self):
        return len(self.deck)

    def __repr__(self):
        return f"{self.deck}"    

class HanabiGame:
    def __init__(self):
        self.deck = Deck()
        self.play_area = {color: 0 for color in COLOR_LIST}
        self.discard_pile = []
        self.hints = MAX_HINT
        self.score = 0
        self.mistakes = 0
        self.players = []
        self.current_player = 0

    # play again after ended
    def play_again(self):
        check = valid_input("Wanna play again? (y/n): ", {'y','n'})
        if check == 'y':
            print("Sure! Let's do the Hanabi again!")
            return True
        elif check == 'n':
            print("Thank you for the playing!")
            return False

    # Every player start by drawing 5 card
    def start_game(self):
        # input validation
        player_count = valid_int("Enter number of players (2-5): ", PLAYER_RANGE)

        # every player starts with 5 hand
        self.players = [{f'Player {i+1}': [self.deck.draw_card() for _ in range(5)]} for i in range(player_count)]
        self.current_player = 0

    # Print out No. of cards in deck, discard, played pile, and other players' hand
    def board_display(self):
        print(f"\n---------------------- Player {self.current_player + 1}, this is your information: -----------------------\n")
        
        for index, player in enumerate(self.players):
            hands = player[list(player.keys())[0]]

            # other players' hand
            if index != self.current_player: # Player cannot see their own Hand
                print(f"       Player {index + 1}: {hands}")
            # current player's hand    
            else:
                card_descriptions = []
                # if color not hinted, displayed as '????', if number not hinted, displayed as '?'
                for card in hands:
                    card_desc = f"{card.color if card.is_color_hinted else '????'}_{card.number if card.is_number_hinted else '?'}"
                    card_descriptions.append(card_desc)
                your_hand = '[' + ', '.join(card_descriptions) + ']' # Unify display format
                print(f" (You) Player {index + 1}: {your_hand}")
       
        # Display the board
        print("----------------------------------------------------------------------------------")
        print(f"    Played card: {self.play_area}")
        print(f" Discarded card: {self.discard_pile}")
        print(f"Cards Remaining: {self.deck.deck_size()}")
        print(f"Number of Hints: {self.hints}/{MAX_HINT}")
        print(f"  Mistakes made: {self.mistakes}/{MAX_MISTAKE}")
        print(f"          Score: {self.score}")
        print("----------------------------------------------------------------------------------")

    def one_turn(self):
        self.board_display()
        self.choose_action()
        # check if the game ended after action
        if self.score == MAX_POINT:
            print("congratulation! You reach 25 points and you win!")
            return False
        elif self.mistakes == MAX_MISTAKE: 
            print("Game Over! You lose!")
            return False
        else: return True
        
    def choose_action(self):
        print(f"\nPlayer {self.current_player + 1}'s turn")
        choice = valid_input("Enter 'p' for play, 'd' for discard, or 'h' for hint: ", {'p','d','h'})

        if choice == 'p':
            self.play_card()
            self.draw_card()
            
        elif choice == 'd':
            self.discard_card()
            self.draw_card()
            
        elif choice == 'h':
            # only allow to hint when you have hints
            if self.hints > 0:
                self.give_hint()
            else:
                print("No hints available!")
                self.choose_action()
        
    def play_card(self):
        # retrieve the current player's hand
        hands = self.players[self.current_player][list(self.players[self.current_player].keys())[0]]
        hands_num = {i for i in range(1, len(hands) + 1)}
        
        #input validation
        card_index = valid_int(f"Enter card index to play (Oldest: 1, Newest: {len(hands)}): ", hands_num)

        #if valid, play to the board and get 1 point
        # card is valid if it is larger than the card on the board by exactly 1
        card = hands.pop(card_index-1)
        if self.play_area[card.color] == card.number - 1:
            self.play_area[card.color] += 1
            self.score += 1
            print(f"player {self.current_player+1} played {card} correctly.")
            
        # if invalid, go to discard pile and get 1 mistake
        else:
            self.discard_pile.append(card)
            self.mistakes += 1
            print(f"player {self.current_player+1} played {card}. Unfortunately it is wrong.")

    def discard_card(self):
        # retrieve the current player's hand
        hands = self.players[self.current_player][list(self.players[self.current_player].keys())[0]]
        hands_num = {i for i in range(1, len(hands) + 1)}
        
        #input validation
        card_index = valid_int(f"Enter card index to discard (Oldest: 1, Newest: {len(hands)}): ", hands_num)

        card = self.discard_pile.append(hands.pop(card_index-1))
        print(f"player {self.current_player+1}, you discarded {card}.")
        
        if self.hints < MAX_HINT:
            self.hints += 1

    # draw a card after playing or discarding
    def draw_card(self):
        if self.deck:
            card = self.deck.draw_card()  # Remove the last card from the deck
            self.players[self.current_player][list(self.players[self.current_player].keys())[0]].append(card)
        else:
            print("The deck is empty, no card to draw.")

    # give hint to other player
    def give_hint(self):
        #input validation
        hint_player_range = {i for i in range(1, len(self.players) + 1)}
        hint_player_range.discard(self.current_player + 1)
        player_num = valid_int("Enter player number to hint: ", hint_player_range)

        # retrieve the chosen player's hand
        hands = self.players[self.current_player][list(self.players[self.current_player].keys())[0]]
        
        # chosen player's hand in his own perspective
        # if color not hinted, displayed as '????', if number not hinted, displayed as '?'
        card_descriptions = []
        for card in hands:
            card_desc = f"{card.color if card.is_color_hinted else '????'}_{card.number if card.is_number_hinted else '?'}"
            card_descriptions.append(card_desc)
        hand_he_sees = '[' + ', '.join(card_descriptions) + ']' # Unify display format

        print(f"You have chosen to hint Player {player_num}")
        print(f"Your Perspective: {hands}")
        print(f" His Perspective: {hand_he_sees}")
        
        hint_type = valid_input("Enter 'c' for color, 'n' for number for hint type: ", {'c','n'})
        if hint_type == 'c':
            self.hint_color(hands)
            
        elif hint_type == 'n':
            self.hint_number(hands)
        self.hints -= 1
            
    def hint_color(self, hands):
        # create a set of color that can be hinted
        color_set = {card.color for card in hands}
        
        hint_color = valid_input(f"Enter a color to hint {color_set}: ", color_set)
        for card in hands:
            if card.color == hint_color:
                card.hint_color()

    def hint_number(self, hands):
        # create a set of number that can be hinted
        number_set = {card.number for card in hands}
        
        hint_number = valid_int(f"Enter a number to hint {number_set}: ", number_set)
        for card in hands:
            if card.number == hint_number:
                card.hint_number()

    def next_player(self):
        print("\n" * 49)
        print("\n" * 49)
        self.current_player = (self.current_player + 1) % len(self.players)

    def play(self):
        # initiate the board
        self.start_game()
        # loop ends if game ended or deck used up
        while self.deck.deck_size != 0:
            if self.one_turn() == False:
                break
            self.next_player()
        # one last round after deck used up
        if self.deck.deck_size == 0:
            print("\n ----- The Deck is used up, each player have one last round -----")
            input("Press any Key to continue: \n")
            for _ in range(player_count):
                if self.one_turn() == False:
                    break
                self.next_player()
            print(f"Game End! Your team got {self.count_point()} points.")

        if self.play_again():
            self.play()

if __name__ == "__main__":
    HanabiGame().play() 
