# Initial variables
cards = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
card_values = {'A':(1,11), '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}
money = 1000
betting_box = []
import random

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

# Betting
def betting():
    """
    Before each round, ask player a bet.
        min = $10
        max = $500

    return (int): Bet amount
    """
    # Global frames
    global money

    # Always loop until valid bet amount
    while True:
        # Print current money
        print('You have', '$' + str(money) + '.')
        print('Minimum to play: $10. Maximum to bet: $500.')
        print()
        # Ask how much to bet
        # Assert bet is within $10-$500
        # Assert bet is within available money
        try:
            bet = int(input('How much do you want to bet? $'))
            assert 10 <= bet <= 500
            assert bet <= money
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
        # Print bet amount and money remaining
        # Then break loop
        else:
            # Reassigns money in global frame
            money -= bet
            print('You bet', '$' + str(bet) + '.')
            print()
            break
    return bet

# Shuffle and Cut - Maybe not include the cutting part
def shuffle():
    """
    Dealer shuffles the cards    
    """
    print('The deck has now been shuffled.', '\n')

# Draw an available card
def drawCard(deck):
    """
    Draw an available card from the deck.

    deck (dict): Deck being used to play

    return (str): An available card
    
    """
    # Is Card Valid
    def isCardValid(card):
        """
        Checks if card is available in deck.

        card (str): Card to check

        return (bool): True if available. False otherwise.
        """
        if deck[card] > 0:
            return True
        else:
            return False

    while True:
        # Draw a random card and check validity
        draw_card = random.choice(cards)
        if isCardValid(draw_card):
            # Take card out of dictionary values
            deck[draw_card] -= 1
            break
    return draw_card

# Display Hand
def displayHand(user, hand, face_down = False):
    """
    Displays the hand.

    user (str): Player or dealer

    hand (list): Current hand

    face_down (bool): initially False. True if there's face down card.
    """
    # Label for dealer or player
    if user == 'dealer':
        whos_cards = "The dealer's cards:"
    else:
        whos_cards = 'Your cards:'

    face_down_card = '[ ]'
    # Enclose each card with [ ]
    hand_i = '] ['.join(hand)
    hand_show = f'[{hand_i}]'

    # Displays hand with player's cards aligned with dealer's cards
    if user == 'dealer' and face_down:
        return f"{whos_cards} [{hand[0]}] {face_down_card}"
    elif user == 'dealer':
        return f"{whos_cards} {hand_show}"
    elif user == 'player' and face_down:
        return f"{whos_cards}         {hand_show} {face_down_card}"
    else:
        return f"{whos_cards}         {hand_show}"

# The Deal
def deal(play_deck):
    """
    Deal 2 cards each to player and dealer.

    play_deck (dict, str -> int): Deck being used to play

    return (tuple): 2-card hand of player and dealer
    """
    player_cards = []
    dealer_cards = []

    # Deal 2 cards to player
    for i in range(2):
        player_cards.append(drawCard(play_deck))
    # Deal 2 cards to dealer
    for i in range(2):
        dealer_cards.append(drawCard(play_deck))

    # Displaying hands
    print(displayHand('dealer', dealer_cards, True))
    print()
    print(displayHand('player', player_cards))
    print()
    return (player_cards, dealer_cards)

# Scoring
def score(hand):
    """
    Calculates the current score with the given hand.

    hand (list): Current hand
    
    return (int): Current score
    """
    # Card Frequency
    def cardFreq(hand):
        """
        Determines frequency of each card in hand.

        hand (list): Hand

        return (dict str -> int): The amount of times a card is repeated in hand
        """
        freq = {}
        for card in hand:
            freq[card] = freq.get(card,0) + 1
        return freq

    # Find frequency of current hand
    card_freq = cardFreq(hand)

    current_score = 0
    # Calculate score of all non-A cards
    for key in card_freq:
        if key == 'A':
            pass
        else:
            current_score += card_freq[key]*card_values[key]

    # Dealing with A cards
    try:
        # All other A's = 1
        # 2A = 22 already, so A = 11 only once
        current_score += card_freq['A'] - 1
    # If no A cards
    except KeyError:
        pass
    else:
        # Test for A = 11
        try:
            test_score = current_score
            test_score += 11
            assert test_score <= 21
        # If A = 11 busts, A = 1
        except AssertionError:
            current_score += 1
        else:
            current_score += 11
    # Finally
    finally:
        return current_score
  
# BlackJacks In First Round
def blackjackInitial(player_cards, dealer_cards, bet):
    """
    Deals with initial round, checking player and dealer for blackjacks, includes insurance.
    
    player_cards (list): The player's 2-card hand

    dealer_cards (list): The dealer's 2-card hand

    return (bool): True if blackjack in 1st round. False, otherwise.
    """
    # Insurance
    def insurance():
        """
        Asks player for an insurance bet or to take even money.

        bet (int): Bet amount
        player_blackjack (bool): If the player has blackjack

        return (int): Insurance bet or 0
        """
        # Ask player to take even money or make insurance bet
        while True:
            if player_blackjack:
                insurance_ask = 'take an even money'
                insurance_bet = bet
            else:
                insurance_ask = 'make an insurance bet'
                insurance_bet = bet/2
            try:
                ans = input(f'Do you want to {insurance_ask} of ${insurance_bet}? ')
                ans_lower = ans.lower()
                assert ans_lower == 'yes' or ans_lower == 'no'
            except:
                print('Please enter yes or no.')
                print()
            else:
                print()
                break
        if ans == 'no':
            return 0
        else:
            return insurance_bet

    # Possible outcomes
    def outcomes(player_blackjack, dealer_blackjack, bet, insurance_bet):
        """
        Possible outcomes:
            1. Player blackjack, even money = + bet
            2. Player blackjack, no even money, dealer blackjack = + bet
            3. Player blackjack, no even money, no dealer blackjack = + 1.5*bet
            4. Player no blackjack, insurance, dealer has blackjack = + bet
            5. Player no blackjack, insurance, no dealer blackjack = - insurance_bet
            6. Player no blackjack, no insurance, dealer blackjack = - bet

        player_blackjack (bool): True if blackjack. False, otherwise.
        dealer_blackjack (bool): True if blackjack. False, otherwise.
        bet (int): Bet amount
        insurance_bet (int): Insurance bet amount
        """
        # Global frames
        global money
        
        # Deals with insurance cases
        if insurance_bet == bet:
            insurance = 'decided to take even money'
        elif insurance_bet > 0:
            insurance = 'made an insurance bet'

        # Deals with player with blackjack
        if player_blackjack:
            if insurance_bet == bet:
                money += bet
                print(f'You {insurance}. You win ${bet}!')
            else:
                if dealer_blackjack:
                    money += bet
                    print(f"It's a standoff. You get back ${bet}.")
                else:
                    blackjack_win = round(1.5*bet, 2)
                    money += blackjack_win
                    print(f'You win ${blackjack_win}!')
        # Deals with player without blackjack
        else:
            if insurance_bet > 0:
                print(f'You {insurance}. ', end = '')
                if dealer_blackjack:
                    money += bet
                    print(f'You win ${2*insurance_bet}!')
                else:
                    money -= insurance_bet
                    print(f'You lose ${insurance_bet}.')
            elif dealer_blackjack:
                print(f'You lose ${bet}.')

    # Check player for blackjack
    player_blackjack = score(player_cards) == 21
    # Check dealer for blackjack
    dealer_blackjack = score(dealer_cards) == 21

    if player_blackjack:
        print('Winner, winner chicken dinner! You have blackjack!')
        # If dealer does not have potential blackjack
        if dealer_cards[0] != 'A' or card_values[dealer_cards[0]] != 10:
            # Win Game
            outcomes(player_blackjack, False, bet, 0)
        
    if dealer_cards[0] == 'A' or card_values[dealer_cards[0]] == 10:
        print('The dealer may have blackjack.')

        # Dealing with insurance bet
        if dealer_cards[0] == 'A':
            print()
            insurance_bet = insurance()
        else:
            insurance_bet = 0

        # Takes even money and end round
        if insurance_bet == bet:
            outcomes(player_blackjack, False, bet, insurance_bet)
        # Otherwise, check for dealer blackjack
        else:
            print('The dealer looks at face down card.')
            # If blackjack, show hand
            if dealer_blackjack:
                print('The dealer has blackjack.')
                print(displayHand('dealer', dealer_cards))
                print()
            else:
                print('The dealer does not have blackjack.')

            # Decide an outcome
            outcomes(player_blackjack, dealer_blackjack, bet, insurance_bet)
            print()

    # At the very end, return True or False for blackjack in 1st round
    if player_blackjack or dealer_blackjack:
        return True
    else:
        return False

# Make an Action
def actions(pair, double_down):
    """
    Ask player for an action.

    pair (bool): True if 2-card hand has same value. False, otherwise.

    double_down (bool): True if player can double down. False, otherwise.

    return (str): Hit, double down, split, or stand
    """
    if pair:
        split = 'split, '
    else:
        split = ''

    if double_down:
        doubledown = 'double down, '
    else:
        doubledown = ''

    while True:
        try:
            action = input(f'What would you like to do: hit, {doubledown}{split}or stand? ')
            if pair and doubledown:
                assert action == 'hit' or action == 'double down' or action == 'split' or action == 'stand'
            elif not pair and doubledown:
                assert action == 'hit' or action == 'double down' or action == 'stand'
            elif pair and not doubledown:
                assert action == 'hit' or action == 'split' or action == 'stand'          
            else:
                assert action == 'hit' or action == 'stand'
        except AssertionError:
            print('Sorry. That is not a valid action.')
            print()
        else:
            print()
            break
    return action

# Doubling Down
def doubleDown(bet, deck, hand):
    """
    Player doubles bet and dealer gives only 1 card, face down.
    Card is revealed after dealer's turn.

    deck (dict str -> int): Deck used to play

    hand (list): Current hand
    """
    # Global frames
    global money

    print(f'You bet an additional ${bet}.')
    money -= bet

    hand.append(drawCard(deck))
    print(displayHand('player', hand))
    print()

# Splitting Pairs
def split(bet, deck, hand):
    """
    Place an additional bet and split hand into 2, with each hand receiving +1 card and playing separate games.

    For split A's, deal +1 card to each, then stand. If blackjack, player wins back bet if dealer does not have blackjack.
    
    bet (int): Bet amount

    deck (dict): Current deck

    hand (list): Pair of cards

    return (tuple): 2 new split hands
    """
    # Global frames
    global money
    
    print(f'The dealer splits your cards.')
    print(f'You bet an additional ${bet}.')
    print()
    money -= bet

    # Deal 1 new card to each hand
    split_hand =[]
    for i in range(2):
        split_hand.append(drawCard(deck))
    hand_1 = [hand[0], split_hand[0]]
    hand_2 = [hand[1], split_hand[1]]

    # Displays new hands
    print(displayHand('player', hand_1))
    print()
    print(displayHand('player', hand_2))
    print()
    print(money)
    # Return separate hands
    return (hand_1, hand_2)

# Hit
def hit(user, deck, hand):
    """
    Deals 1 additional card and adds to hand.

    deck (dict): Deck being used to play

    hand (list): Current hand
    """
    # Draws an available card and adds to hand
    hand.append(drawCard(deck))

    # Displays new hand
    print(displayHand(user, hand))
    print()


# Player's Turn
def playerTurn(deck, hand, bet):
    """  
    Player's turn.

    deck (dict): Current deck

    hand (list): Current hand

    bet (int): Bet amount
    """
    # Split flag
    split_flag = hand[0] == hand[1]
    # Double down flag
    double_down_flag = True

    # Initial score to make a move
    current_score = 0

    # As long as card value < 21
    while current_score < 21:
        # Ask for action
        action = actions(split_flag, double_down_flag)
        if action == 'stand':
            break
        elif action == 'double down':
            doubleDown(bet, deck, hand)
            # After double down, player can do no more action
            break
        elif action == 'split':
            split_hand = split(bet, deck, hand)
            # Check if split A's
            if hand[0] == 'A':
                score(split_hand[0])
                score(split_hand[1])
            else:
            # Maybe recursive, play smaller games H1,H2
                playerTurn(deck, split_hand[0], bet)
                playerTurn(deck, split_hand[1], bet)
        else:
            hit('player', deck, hand)
        # After 1st round, player can not double down or split anymore
        double_down_flag = False
        split_flag = False
        # After action is completed, update current value
        current_score = score(hand)

    # Check for blackjack or bust
    if current_score == 21:
        print('Yay! Blackjack!')
        print()
        # Player must stand
    elif current_score > 21:
        print('Ouch. Bust.')
        print()
    # If stand
    else:
        pass

    


"""
For player turn


    Split
        If you split, you CANNOT split further
            You can STILL double down, hit or stand


For blackjack in 1st round,
    Have to account for bet returning back to player money total
        Ex. Take even money, if bet = 10, dealer gives $10. Then bet returns back to player

"""







# Reshuffling

# The Dealer's Turn
def dealerTurn(deck, hand):
    """
    The dealer reveals the face down card and keeps hitting cards until the score is 17-21, at which point the dealer stands, or busts.

    deck (dict): Current deck

    hand (list): Current hand

    return (tuple): The dealer's score
    """
    # Reveal dealer's hand
    print('The dealer reveals the face down card.')
    print(displayHand('dealer', hand))
    print()
    # Calculate dealer's current score
    current_score = score(hand)

    # As long as score is not 17-21
    while current_score < 17:
        # Hit
        print('The dealer hits.')
        # print()
        hit('dealer', deck, hand)
        current_score = score(hand)

    # Check if dealer has blackjack
    if current_score == 21:
        print('The dealer has blackjack.')
    elif current_score > 21:
        print('The dealer busts.')
    else:
        print('The dealer stands.')

    # Finally return score
    return current_score

    







# After dealer turn ends, compare dealers score with (all if applicable) player score
# Iterate over each player score
# max() which one to find winner

"""
After dealer's turn ends, bust or stand or 21
    If dealer busts,
        dealer gives player additional bet. bet is then returned to player

        Ex. bet = 2 chips
            dealer gives 2 chips
            player now has 4 chips


    After dealer stands, compare scores
        If player score is higher, player wins additional bet. bet is then returned to player (2*bet)

        If dealer score is higher, player loses bet.

    If dealer score == player score,
        player gets back bet. no win/no lose


If player busts, lose bet automatically. End round.



    """ 

# Playing The Game
def playBlackJack():
    """
    Play the game.
    """
    # Create the deck
    deck = createDeck()

    while money >= 10:
        # Start betting
        bet = betting()
        betting_box.append(bet)
        # Shuffle the deck
        shuffle()

        player_hand = ['4','4']
        dealer_hand = ['5','10']
        # # Deal 1st round
        # hand = deal(deck)
        # player_hand = hand[0]
        # dealer_hand = hand[1]
        # Blackjacks 1st Round
        round_over = blackjackInitial(player_hand, dealer_hand, bet)
        # # If blackjack in 1st round, round ends
        if round_over:
            break 
        print('It is now your turn.')
        # Otherwise, it's player turn
        player_scores = playerTurn(deck, player_hand, bet)
        print("It is now the dealer's turn.")
        dealer_score = dealerTurn(deck, dealer_hand)

if __name__ == "__main__":
    playBlackJack()