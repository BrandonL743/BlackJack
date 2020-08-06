# Insurance
def insurance(player_blackjack, bet, wallet):
    """
    Asks player for an insurance bet or to take even money.

    return (int): Insurance bet or 0
    """
    insurance_possible = wallet >= bet//2
    if player_blackjack:
        insurance_ask = 'take an even money'
        insurance_bet = bet
    else:
        insurance_ask = 'make an insurance bet'
        insurance_bet = bet//2
    
    # Ask player to take even money or make insurance bet
    while True:
        try:
            ans = input(f'Do you want to {insurance_ask} of ${insurance_bet}? ')
            ans_lower = ans.lower()
            assert ans_lower == 'yes' or ans_lower == 'no'
        except:
            print('Sorry. That is not a valid answer.')
            print()
        else:
            if ans_lower == 'yes' and (not player_blackjack) and (not insurance_possible):
                print('You do not have enough money to make an insurance bet.')
                print()
            else:
                print()
                break
    if ans == 'no':
        return 0
    else:
        return insurance_bet

# Possible outcomes
def outcomes(player, player_blackjack, dealer_blackjack, insurance_bet):
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
    # Get wallet and bet
    money = player.getWallet()
    bet = player.getBet()
    
    # Deals with insurance cases
    if insurance_bet == bet:
        insurance = 'decided to take even money'
    elif insurance_bet > 0:
        insurance = 'made an insurance bet'

    # Deals with player with blackjack
    if player_blackjack:
        if insurance_bet == bet:
            player.updateWallet(bet)
            player.returnBet()
            player.removeSideBet(insurance_bet)
            print(f'You {insurance}. You win ${bet}!')
        else:
            if dealer_blackjack:
                player.returnBet()
                print(f"It's a standoff. You get back ${bet}.")
            else:
                blackjack_win = int(1.5*bet)
                player.updateWallet(blackjack_win)
                player.returnBet()
                print(f'You win ${blackjack_win}!')
    # Deals with player without blackjack
    else:
        if insurance_bet > 0:
            print(f'You {insurance}. ', end = '')
            if dealer_blackjack:
                player.returnBet() # You just win back your bet
                player.removeSideBet(insurance_bet)
                print(f'You win ${2*insurance_bet}!')
            else:
                player.updateWallet(-insurance_bet)
                player.removeSideBet(insurance_bet)
                print(f'You lose ${insurance_bet}.')
        elif dealer_blackjack:
            player.updateWallet(-bet)
            player.loseBet()
            print(f'You lose ${bet}.')


# BlackJacks In First Round
def blackjackInitial(player, player_cards, dealer_cards, deck):
    """
    Deals with initial round, checking player and dealer for blackjacks, includes insurance.
    
    player (inst. Money): The player

    player_cards (list): The player's 2-card hand

    dealer_cards (list): The dealer's 2-card hand

    deck (inst. Deck): Current deck

    return (bool): True if blackjack in 1st round. False, otherwise.
    """
    import time
    import Scoring
    import Board

    # Get card values and bet amount
    card_values = deck.getValues()
    wallet = player.getWallet()
    bet = player.getBet()
    
    # Check player for blackjack
    player_blackjack = Scoring.score(deck, player_cards) == 21
    # Check dealer for blackjack
    dealer_blackjack = Scoring.score(deck, dealer_cards) == 21

    if player_blackjack:
        print('Winner, winner chicken dinner! You have blackjack!')
        time.sleep(2)
        # If dealer does not have potential blackjack
        if not (dealer_cards[0] == 'A' or card_values[dealer_cards[0]] == 10):
            # Win Game
            outcomes(player, player_blackjack, False, 0)
        
    if dealer_cards[0] == 'A' or card_values[dealer_cards[0]] == 10:
        print('The dealer may have blackjack.')
        time.sleep(1)

        # Dealing with insurance bet
        if dealer_cards[0] == 'A':
            print()
            insurance_bet = insurance(player_blackjack, bet, wallet)
        else:
            insurance_bet = 0

        # Only add insurance bet to side box if non-0
        if insurance_bet > 0:
            player.addSideBet(insurance_bet)

        # Takes even money and end round
        if insurance_bet == bet:
            outcomes(player, player_blackjack, False, insurance_bet)
        # Otherwise, check for dealer blackjack
        else:
            print('The dealer looks at face down card.')
            time.sleep(1)
            # If blackjack, show hand
            if dealer_blackjack:
                print('The dealer has blackjack.')
                print()
                Board.showBoard(player, player_cards, dealer_cards, '')
                time.sleep(3)

            else:
                print('The dealer does not have blackjack.')
                print()
                Board.showBoard(player, player_cards, dealer_cards, 'deal_face')
                time.sleep(3)

            # Decide an outcome
            outcomes(player, player_blackjack, dealer_blackjack, insurance_bet)

    # At the very end, return True or False for blackjack in 1st round
    if player_blackjack or dealer_blackjack:
        return True
    else:
        return False