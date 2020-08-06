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

# Scoring
def score(deck, hand):
    """
    Calculates the current score with the given hand.

    deck (inst. Deck): Current deck

    hand (list): Current hand
    
    return (int): Current score
    """
    # Get card values
    card_values = deck.getValues()

    card_freq = cardFreq(hand)

    current_score = 0
    # Calculate score of all non-A cards
    for key in card_freq:
        if key == 'A':
            pass
        else:
            current_score += card_freq[key]*card_values[key]

    try:
        # All other A's = 1
        # 2A = 22 already, so A = 11 only once
        current_score += card_freq['A'] - 1
    except KeyError:
        pass
    else:
        try:
            test_score = current_score
            test_score += 11
            assert test_score <= 21
        except AssertionError:
            current_score += 1
        else:
            current_score += 11
    finally:
        return current_score