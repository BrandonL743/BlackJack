# Initial variables
cards = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
card_values = {'A':(1,11), '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

import time
import random
import Cards
import Board
import FirstHand
import PlayerTurn
import DealerTurn
import Settlements

class Money(object):
    betting_box = []
    side_box = []
    double_down = []

    def __init__(self, wallet):
        self.wallet = wallet
        self.bet_amount = 0

    def setBet(self, bet_amount):
        self.bet_amount = bet_amount
        Money.betting_box.append(bet_amount)

    def updateWallet(self, new_money):
        self.wallet += new_money

    def returnBet(self):
        self.wallet += self.bet_amount
        self.betting_box.remove(self.bet_amount)
    
    def loseBet(self):
        self.betting_box.remove(self.bet_amount)
    
    def addSideBet(self, side_bet):
        self.side_box.append(side_bet)

    def removeSideBet(self, side_bet):
        """ Remove a bet/side bet from side bet box """
        self.side_box.remove(side_bet)

    def addDoubleDown(self, hand):
        Money.double_down.append(hand)

    def getWallet(self):
        return self.wallet

    def getBet(self):
        return self.bet_amount
    
    def getBetting_box(self):
        return Money.betting_box

    def getSideBox(self):
        return Money.side_box

    def getDoubleDownCheck(self):
        return Money.double_down

    def roundreset(self):
        self.bet_amount = 0
        Money.betting_box = []
        Money.side_box = []
        Money.double_down = []

# The Deck
def createDeck(deck_size = 6):
    """
    Create deck(s), each with 4 cards of A, 2-10, J, Q, K

    deck_size (int): Default 6 decks
    
    return (dict, str -> int): A deck of cards
    """
    deck = {}
    # Iterate over each card so {card name: # of cards}
    for card in cards:
        deck[card] = 4 * deck_size
    # Return deck
    return deck

# Betting Phase
def makeBet(player_pot):
    """
    Make a bet.

    player_pot (inst. class): The player instance.
    """
    money = player_pot.getWallet()
    while True:
        print(f"Your wallet:        (${money})")
        print('Minimum to play: $10. Maximum to bet: $500.')
        print()
        try:
            user_input = input('How much do you want to bet? $')
            if user_input == 'cash out':
                raise ConnectionAbortedError
            bet = int(user_input)
            assert 10 <= bet <= 500
            assert bet <= money
        # Quit the game
        except ConnectionAbortedError:
            break
        # Raise ValueError if input is not a number
        except ValueError:
            print('Please enter a valid amount to play.')
            print()
        except AssertionError:
            if bet < 10:
                print('Sorry, there is a $10 minimum to play.')
                print()
            elif bet > 500:
                print('Sorry, you can only bet up to a maximum of $500.')
                print()
            else:
                print('Sorry, you do not have the money to make this bet.')
                print()

        else:
            player_pot.setBet(bet)
            player_pot.updateWallet(-bet)
            print(f'You bet ${bet}.')
            print()
            break
    if user_input == 'cash out':
        return 'cash out'

# Playing the Game
def playBlackJack():
    """ Play the game """
    # Initial variables
    create_deck = createDeck()
    deck = Cards.Deck(create_deck, cards, card_values)
    cards_remain = deck.cardsRemain()
    player = Money(1000)

    print()
    print("Welcome to BlackJack!")
    print()
    print(f'--------------------------')
    print("Here are some ground rules:")
    print()
    print("Blackjack payouts are 3:2.")
    print()
    print("The dealer must stand on 17+.")
    print()
    print("You can only split once.")
    print()
    print("You must stand after splitting Aces.")
    print()
    print("You may leave the table at any time, before a round starts.")
    print()
    print("Simply type 'cash out' instead of betting.")
    print()
    print('Good luck and have fun!')
    print(f'--------------------------')
    time.sleep(5)
    print('The dealer will now cut and shuffle the deck.')
    time.sleep(2)
    print('The deck has now been shuffled.')
    print()

    # As long as player has money
    while player.getWallet() >= 10:
        player.roundreset()
        # Reshuffle deck if less than 1/4 cards remain
        if cards_remain < (52*6)/4:
            print('The dealer needs to reshuffle the deck.')
            new_deck = createDeck()
            deck = Cards.Deck(new_deck, cards, card_values)
            cards_remain = deck.cardsRemain()
            time.sleep(2)
            print('The deck has now been shuffled.')
            print()
        
        # Make a bet to play or quit game
        initial_input = makeBet(player)
        if initial_input == 'cash out':
            break

        # Deal initial cards
        player_cards = deck.assembleHand()
        dealer_cards = deck.assembleHand()
        # Show the board
        Board.showBoard(player, player_cards, dealer_cards, 'deal_face')
        time.sleep(3)

        # First Hand
        if FirstHand.blackjackInitial(player, player_cards, dealer_cards, deck):
            print()
            pass
        else:
            # Player's Turn
            print('It is now your turn.')
            player_hands_done = PlayerTurn.playerTurn(player, deck, player_cards, dealer_cards)

            if len(player.getBetting_box()) > 0:
                print("It is now the dealer's turn.")
                dealer_hands_done = DealerTurn.dealerTurn(player, deck, player_cards, dealer_cards)

                # Settlements
                print()
                time.sleep(2)
                Settlements.settlements(player, player_hands_done, dealer_hands_done, deck)
                print()

        # Check deck amount
        cards_remain = deck.cardsRemain()
        print(f'--------------------------')
        time.sleep(1)
    if initial_input == 'cash out':
        print(f'--------------------------')
        print(f'You leave with ${player.getWallet()}.')
        print()
        print("Thank you for playing. Goodbye!")
    else:
        print(f'--------------------------')
        print('You have run out of money.')
        print()
        print('Come back again when you have more. Goodbye!')
        print()

if __name__ == "__main__":
    playBlackJack()