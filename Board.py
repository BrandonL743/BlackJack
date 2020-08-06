# Display Hand
def displayHand(user, hand, face_down = ''):
    """
    Displays the hand.

    user (str): Player or dealer

    hand (list): Current hand

    face_down (str): 'deal_face' for face down card. Empty, otherwise.
    """
    face_down_card = '[ ]'
    # Enclose each card with [ ]
    hand_i = '] ['.join(hand)
    hand_show = f'[{hand_i}]'

    # Displays hand with player's cards aligned with dealer's cards
    if user == 'dealer' and face_down == 'deal_face':
        return f"[{hand[0]}] {face_down_card}"
    else:
        return f"{hand_show}"

def showBettingBox(player):
    try:
        box_list = [str(int) for int in player.getBetting_box()]
    except:
        box_list = []
    box_show = ' $'.join(box_list)
    return box_show

def showSideBox(player):
    try:
        side_list = [str(int) for int in player.getSideBox()]
    except:
        side_list = []
    side_show = ' $'.join(side_list)
    return side_show

def showWallet(player):
    wallet = player.getWallet()
    return wallet

def showBoard(player, player_hand, dealer_hand, face_down):
    """
    Shows the state of the board.
    
    """
    print(f'-------------------------------------------------------')
    print(f"The dealer's cards: {displayHand('dealer', dealer_hand, face_down)}")
    print()
    print(f"Your cards:         {displayHand('player', player_hand, face_down)}")
    print()
    print(f"Betting box:        |${showBettingBox(player)}|")

    if player.getSideBox():
        print(f"Side bets:          |${showSideBox(player)}|")

    print()
    print(f"Your wallet:        (${showWallet(player)})")
    print(f'-------------------------------------------------------')
    print()

def showBoardSplit(player, left_hand, right_hand, dealer_hand, face_down):
    """
    Shows the state of the board if there's been a split
    
    """
    print(f'-------------------------------------------------------')
    print(f"The dealer's cards: {displayHand('dealer', dealer_hand, face_down)}")
    print()

    if left_hand == []:
        print(f"Your cards:         {displayHand('player', right_hand, face_down)}")
    elif right_hand == []:
        print(f"Your cards:         {displayHand('player', left_hand, face_down)}")
    else:
        print(f"Your cards:         {displayHand('player', left_hand, face_down)}")
        print(f"                    {displayHand('player', right_hand, face_down)}")

    print()
    print(f"Betting box:        |${showBettingBox(player)}|")

    if player.getSideBox():
        print(f"Side bets:          |${showSideBox(player)}|")

    print()
    print(f"Your wallet:        (${showWallet(player)})")
    print(f'-------------------------------------------------------')
    print()