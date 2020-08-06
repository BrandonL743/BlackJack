def settlements(player, player_hands, dealer_hand, deck):
    """
    Unpacks player hands if more than 1 hand, then compares for potential settlements.

    player_hands (list or tuple): A list of cards, or a tuple of hands

    dealer_hand (list): Dealer's cards

    deck (dict): Current deck
    """
    import Scoring

    bet = player.getBet()
    betting_box = player.getBetting_box()
    betting_box_copy = betting_box[:]
    side_box = player.getSideBox()
    side_box_copy = side_box[:]
    double_down_check = player.getDoubleDownCheck()

    # Calculate total bet amount
    total_bet = 0
    for i in betting_box:
        total_bet += i
    for i in side_box:
            total_bet += i

    # Convert hand into a tuple
    if isinstance(player_hands, list):
        total_hands = (player_hands,)
    else:
        total_hands = player_hands

    dealer_score = Scoring.score(deck, dealer_hand)

    # If dealer busts, pay equal to all bets and side bets
    if dealer_score > 21:
        for i in side_box_copy:
            player.updateWallet(2*bet) # Give side bet, and return side bet
            player.removeSideBet(bet)
        for bet in betting_box_copy:
            player.updateWallet(bet)
            player.returnBet()
        print(f'You win ${total_bet}!')
    else:
        for play in total_hands:
            # Find the score
            player_score = Scoring.score(deck, play)

            # Find if this hand was a double down
            if play in double_down_check:
                sidebet_amount = side_box[0]
                # Compare scores
                if player_score == dealer_score:
                    player.returnBet()
                    player.updateWallet(sidebet_amount)
                    print(f"It's a standoff. You get back ${bet + sidebet_amount}.")
                elif player_score > dealer_score:
                    pass 
                    player.updateWallet(bet)
                    player.updateWallet(sidebet_amount)
                    player.returnBet()
                    print(f'You win ${bet + sidebet_amount}!')
                else:
                    player.loseBet()
                    player.removeSideBet(sidebet_amount)
                    print(f'You lose ${bet + sidebet_amount}.')
            
            # If no double down
            else:
                # Compare scores
                if player_score == dealer_score:
                    player.returnBet()
                    print(f"It's a standoff. You get back ${bet}.")
                elif player_score > dealer_score:
                    pass 
                    player.updateWallet(bet)
                    player.returnBet()
                    print(f'You win ${bet}!')
                else:
                    player.loseBet()
                    print(f'You lose ${bet}.')
