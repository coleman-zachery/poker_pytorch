from libs.constants import RANKS, SUITS
from libs.helpers import shuffle_hand, cardinal_subsets
import torch

def generate_royal_flush(card_exceptions=[]):
    ranks = RANKS[-5:]
    exclude_suits = set()
    for card_exception in card_exceptions:
        rank_char, suit_char = card_exception
        if rank_char in ranks:
            exclude_suits.add(suit_char)
    eligible_suits = [suit for suit in SUITS[3:] if suit not in exclude_suits]
    if len(eligible_suits) == 0: return None
    suit = eligible_suits[torch.randint(len(eligible_suits)).item()]
    hand = [rank + suit for rank in ranks]
    return shuffle_hand(hand)

def generate_straight_flush(card_exceptions=[]):
    eligible_hands = {suit: [cardinal_subsets(RANKS, 5)] for suit in SUITS[-4:]}
    return eligible_hands

def generate_four_of_a_kind(): pass
def generate_full_house(): pass
def generate_flush(): pass
def generate_straight(): pass
def generate_three_of_a_kind(): pass
def generate_two_pair(): pass
def generate_high_card(): pass

def generate_nothing():
    return ['__', '__', '__', '__', '__']

