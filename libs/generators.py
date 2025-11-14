from libs.constants import RANKS, SUITS
from libs.helpers import shuffle_hand, cardinal_subsets, random_item

def generate_deck(card_exceptions=[]):
    return [rank + suit for rank in RANKS for suit in SUITS if rank + suit not in card_exceptions]

def generate_royal_flush(card_exceptions=[]):
    eligible_suits = set(SUITS[-4:])
    for rank, suit in card_exceptions:
        if suit not in eligible_suits: continue
        if rank in RANKS[-5:]: eligible_suits.discard(suit)
        if len(eligible_suits) == 0: return None
    eligible_hands = [[rank + suit for rank in RANKS[-5:]] for suit in eligible_suits]
    hand = random_item(eligible_hands)
    return shuffle_hand(hand)

def generate_straight_flush(card_exceptions=[]):
    eligible_hands = [[rank + suit for rank in subset] for suit in SUITS[-4:] for subset in cardinal_subsets(RANKS[3:-1], 5)]
    return eligible_hands
    for card in card_exceptions:
        eligible_hands = [hand for suit_hands in eligible_hands for hand in suit_hands if card not in hand]
    hand = random_item(eligible_hands)
    return shuffle_hand(hand)

def generate_four_of_a_kind(card_exceptions=[]):
    eligible_hands = []
    for rank in RANKS[3:]:
        for rank_char, _ in card_exceptions:
            if rank == rank_char: break
        else:
            four_kind = [rank + suit for suit in SUITS[-4:]]
            remaining_cards = generate_deck(card_exceptions + four_kind)
            eligible_hands.append(four_kind + [remaining_cards])
    hand = random_item(eligible_hands)
    *a, b = hand
    hand = a + random_item(b)
    return shuffle_hand(hand)

def generate_full_house(): pass
def generate_flush(): pass
def generate_straight(): pass
def generate_three_of_a_kind(): pass
def generate_two_pair(): pass
def generate_high_card(): pass

def generate_nothing():
    return ['__', '__', '__', '__', '__']
