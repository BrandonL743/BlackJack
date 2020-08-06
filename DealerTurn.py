# The Dealer's Turn
def dealerTurn(player, deck, player_cards, hand):
    """
    The dealer reveals the face down card and keeps hitting cards until the score is 17-21, at which point the dealer stands, or busts.

    deck (dict): Current deck

    hand (list): Current hand

    return (tuple): The dealer's score
    """
    import time
    import Scoring
    import Board

    # Reveal dealer's hand
    print('The dealer reveals the face down card.')
    print()
    Board.showBoard(player, player_cards, hand, '')
    time.sleep(3)

    # Calculate dealer's current score
    current_score = Scoring.score(deck, hand)

    # Dealer hits as long as score is not 17-21
    while current_score < 17:
        print('The dealer hits.')
        deck.hit(hand)
        Board.showBoard(player, player_cards, hand, '')
        time.sleep(3)
        current_score = Scoring.score(deck, hand)

    # Check if dealer has blackjack
    if current_score == 21:
        print('The dealer has blackjack.')
    elif current_score > 21:
        print('The dealer busts.')
    else:
        print('The dealer stands.')

    # Finally return score
    return hand