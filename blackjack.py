import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:

    # Initializing the Card class
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # For printing the Card
    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:

    # Initilaizing the Deck class
    def __init__(self):
        self.deck = []

        # Creating a deck of 52 cards
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    # For printing the deck
    def __str__(self):
        deck_comp = ''
        # Adding each Card object's print string
        for card in self.deck:
            deck_comp += '\n '+card.__str__()
        return 'The deck has:' + deck_comp

    # To shuffle the deck
    def shuffle(self):
        random.shuffle(self.deck)

    # Pop a card from the deck and returns it
    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]  # Updating value of Hand
        if card.rank == 'Ace':
            self.aces += 1  # Updating the no. of aces

    # if total value > 21 and I still have an ace
    # then change value of the ace to 1 from 11
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    # Initilaizing the Chips class
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet  # Updating value of Chips

    def lose_bet(self):
        self.total -= self.bet  # Updating value of Chips


def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Please enter a valid bet!')
        else:
            if chips.bet > chips.total:
                print(f"Sorry, your bet can't exceed {chips.total}.")
            else:
                break


def hit(deck, hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Would you like to Hit or Stand? Enter 'H' or 'S'. ")

        if x[0].upper() == 'H':
            hit(deck, hand)  # hit() function defined above

        elif x[0].upper() == 'S':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()


def push(player, dealer):
    print("Dealer and Player tie! It's a push.")


if __name__ == "__main__":
    while True:
        # Opening statement
        print('\n\nWelcome to BlackJack! \nGet as close to 21 as you can without going over!\nDealer hits until he reaches 17. \nAces count as 1 or 11.\n')

        # Creating & shuffling the deck and dealonng two cards to each player
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Setting up the Player's chips
        player_chips = Chips()  # remember the default value is 100

        # Prompting the Player for their bet
        take_bet(player_chips)

        # Showing all cards except one of the Dealer's card
        show_some(player_hand, dealer_hand)

        while playing:

            # Prompting for Player to Hit or Stand
            hit_or_stand(deck, player_hand)

            # Showing all cards except one of the Dealer's card
            show_some(player_hand, dealer_hand)

            # If player's hand exceeds 21, running player_busts() and breaking out of loop
            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand, player_chips)
                break

        # If Player hasn't busted, playing Dealer's hand until Dealer reaches 17
        if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            # Showing all cards
            show_all(player_hand, dealer_hand)

            # Running different winning scenarios
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)

            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)

            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)

            else:
                push(player_hand, dealer_hand)

        # Informing Player of their chips total
        print("\nPlayer's winnings stand at", player_chips.total)

        # Asking to play again
        new_game = input(
            "Would you like to play another hand? Enter 'Y' or 'N'. ")

        if new_game[0].upper() == 'Y':
            playing = True
            continue
        else:
            print("Thanks for playing!\n")
            break
