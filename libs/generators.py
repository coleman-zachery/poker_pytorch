from libs.constants import RANKS, SUITS
from libs.helpers import shuffle_hand, cardinal_subsets
import torch

def generate_royal_flush(card_exceptions=[]):
    eligible_hands = [[rank + suit for rank in RANKS[-5:]] for suit in SUITS[-4:]]
    for rank, suit in card_exceptions:
        eligible_hands = [hand for hand in eligible_hands if rank + suit not in hand]
    hand = eligible_hands[torch.randint(len(eligible_hands)).item()]
    return shuffle_hand(hand)

def generate_straight_flush(card_exceptions=[]):
    eligible_hands = [[[rank + suit for rank in subset] for subset in cardinal_subsets(RANKS[3:-1], 5)] for suit in SUITS[-4:]]
    for rank, suit in card_exceptions:
        eligible_hands = [hand for suit_hands in eligible_hands for hand in suit_hands if rank + suit not in hand]
    hand = eligible_hands[torch.randint(len(eligible_hands), (1,)).item()]
    return shuffle_hand(hand)

def generate_four_of_a_kind(card_exceptions=[]):
    eligible_hands = [rank + suit for suit in SUITS[-4:] for rank in RANKS[3:]]
    return eligible_hands

def generate_full_house(): pass
def generate_flush(): pass
def generate_straight(): pass
def generate_three_of_a_kind(): pass
def generate_two_pair(): pass
def generate_high_card(): pass

def generate_nothing():
    return ['__', '__', '__', '__', '__']
