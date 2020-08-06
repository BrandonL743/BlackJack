class Deck(object):

    def __init__(self, deck, cards, values):
        self.deck = deck
        self.cards = cards
        self.values = values

    # Is Card Valid
    def isCardValid(self, card):
        """
        Checks if the card is available in the deck

        card (str): Card to be checked

        return (bool): True if available. False otherwise.
        """
        if self.deck[card] > 0:
            return True
        else:
            return False

    # Draw an available card
    def drawCard(self):
        """
        Draw an available card from the deck.

        return (str): An available card
        """
        import random
        
        while True:
            draw_card = random.choice(self.cards)
            if self.isCardValid(draw_card):
                self.deck[draw_card] -= 1
                break
        return draw_card

    # Assemble the hand
    def assembleHand(self):
        """
        Assembles the user's hand.

        return (list): Player or dealer's hand.
        """
        user_cards = []
        for i in range(2):
            card = self.drawCard()
            user_cards.append(card)
        return user_cards

    def getValues(self):
        """
        Get the point value of card.

        return (dict): Point value of each card.
        """
        return self.values

    # Cards Remain
    def cardsRemain(self):
        """
        Calculates remaining cards in deck.
        
        return (int): Cards remaining
        """
        cards_remain = 0
        available_card_list = self.deck.values()
        for card in available_card_list:
            cards_remain += card
        return cards_remain

    # Hit
    def hit(self, hand):
        """
        Deals 1 additional card and adds to hand.

        hand (list): Current hand
        """
        hit_card = self.drawCard()
        hand.append(hit_card)

    # Splitting Pairs
    def split(self, hand):
        """
        Split hand into 2, with each hand receiving +1 card and playing separate games.

        For split A's, deal +1 card to each, then stand. If blackjack, player wins back bet if dealer does not have blackjack.
        
        bet (int): Bet amount

        deck (dict): Current deck

        hand (list): Pair of cards

        return (tuple): 2 new split hands
        """
        # Deal 1 new card to each hand
        split_hand = []
        for i in range(2):
            split_hand.append(self.drawCard())
        hand_1 = [hand[0], split_hand[0]]
        hand_2 = [hand[1], split_hand[1]]
        # Return separate hands
        return (hand_1, hand_2)






