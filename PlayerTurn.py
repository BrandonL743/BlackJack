# Make an Action
def actions(wallet, bet, pair, double_down):
    """
    Ask player for an action.

    pair (bool): True if 2-card hand has same value. False, otherwise.

    double_down (bool): True if player can double down. False, otherwise.

    return (str): Hit, double down, split, or stand
    """
    double_split_possible = wallet >= bet

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
            if action == 'double down' and not double_split_possible:
                print('You do not have enough money to double down.')
                print()
            elif action == 'split' and not double_split_possible:
                print('You do not have enough money to split.')
                print()
            else:
                print()
                break
    return action

# Player's Turn
def playerTurn(player, deck, hand, dealer_hand, split = ''):
    """  
    Player's turn.

    deck (dict): Current deck

    hand (list): Current hand

    bet (int): Bet amount
    """
    # Initial variables
    split_flag = hand[0] == hand[1]
    double_down_flag = True
    current_score = 0
    wallet = player.getWallet()
    bet = player.getBet()

    import time
    import Scoring
    import Board

    if split == 'SA':
        pass
    else:
        if split == 'S':
            split_flag = False
        while current_score < 21:
            # Ask for action
            action = actions(wallet, bet, split_flag, double_down_flag)
            if action == 'stand':
                break
            elif action == 'double down':
                player.updateWallet(-bet)
                player.addSideBet(bet)
                print(f'You bet an additional ${bet}.')
                print()
                deck.hit(hand)
                player.addDoubleDown(hand)
                Board.showBoard(player, hand, dealer_hand, 'deal_face')
                time.sleep(3)
                break
            elif action == 'split':
                player.updateWallet(-bet)
                player.setBet(bet)
                split_hand = deck.split(hand)
                print(f'The dealer splits your cards.')
                print(f'You bet an additional ${bet}.')
                print()
                Board.showBoardSplit(player, split_hand[0], split_hand[1], dealer_hand, 'deal_face')
                time.sleep(3)

                # Split hand 1
                print("You play the first split hand.")
                Board.showBoard(player, split_hand[0], dealer_hand, 'deal_face')
                time.sleep(3)
                if hand[0] == 'A':
                    split_hand1 = playerTurn(player, deck, split_hand[0], dealer_hand, 'SA')
                else:
                    split_hand1 = playerTurn(player, deck, split_hand[0], dealer_hand, 'S')
                
                # Split Hand 2
                print("You now play the second split hand.")
                Board.showBoard(player, split_hand[1], dealer_hand, 'deal_face')
                time.sleep(3)
                if hand[0] == 'A':
                    split_hand2 = playerTurn(player, deck, split_hand[1], dealer_hand, 'SA')
                else:
                    split_hand2 = playerTurn(player, deck, split_hand[1], dealer_hand, 'S')
                
                # After playing both hands
                if split_hand1 or split_hand2:
                    Board.showBoardSplit(player, split_hand1, split_hand2, dealer_hand, 'deal_face')
                    time.sleep(3)
                return split_hand1, split_hand2

            else:
                deck.hit(hand)
                Board.showBoard(player, hand, dealer_hand, 'deal_face')
                time.sleep(3)

            # After 1st round, player can not double down or split anymore
            double_down_flag = False
            split_flag = False
            # After action is completed, update current value
            current_score = Scoring.score(deck, hand)
        
    # Check for blackjack or bust
    current_score = Scoring.score(deck, hand)
    if current_score == 21:
        print('You have blackjack!')
        print()
        return hand
        # Player must stand
    elif current_score > 21:
        print('Ouch, you bust. ', end = '')
        if action == 'double down':
            print(f'You lose ${2*bet}.')
            player.removeSideBet(bet)
        else:
            print(f'You lose ${bet}.')
        player.loseBet()
        print()
        hand = []
        return hand
    else:
        print('You stand.')
        print()
        return hand