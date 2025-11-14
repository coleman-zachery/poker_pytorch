from libs.constants import RANKS, SUITS
from libs.helpers import shuffle_hand, cardinal_subsets, random_item

def generate_deck(card_exceptions=[]):
    return list(set([rank + suit for rank in RANKS[3:] for suit in SUITS[-4:]]) - set(card_exceptions))

def generate_royal_flush(card_exceptions=[]):
    eligible_suits = set(SUITS[-4:])
    for rank, suit in card_exceptions:
        if suit not in eligible_suits: continue
        if rank in RANKS[-5:]: eligible_suits.discard(suit)
        if len(eligible_suits) == 0: return None
    eligible_hands = [[rank + suit for rank in RANKS[-5:]] for suit in eligible_suits]
    if len(eligible_hands) == 0: return None
    hand = random_item(eligible_hands)
    return shuffle_hand(hand)

def generate_straight_flush(card_exceptions=[]):
    eligible_hands = []
    for suit in SUITS[-4:]:
        for subset in cardinal_subsets(RANKS[3:-1], 5):
            hand = [rank + suit for rank in subset]
            if len(set(hand) & set(card_exceptions)) > 0: continue
            eligible_hands.append(hand)
    if len(eligible_hands) == 0: return None
    hand = random_item(eligible_hands)
    return shuffle_hand(hand)

def generate_four_of_a_kind(card_exceptions=[]):
    eligible_hands = []
    for rank in set(RANKS[3:]) - set([rank_char for rank_char, _ in card_exceptions]):
        four_kind = [rank + suit for suit in SUITS[-4:]]
        remaining_cards = generate_deck(card_exceptions + four_kind)
        if len(remaining_cards) == 0: continue
        eligible_hands.append(four_kind + [remaining_cards])
    if len(eligible_hands) == 0: return None
    *four_kind, fifth_cards = random_item(eligible_hands)
    hand = four_kind + random_item(fifth_cards)
    return shuffle_hand(hand)

def generate_full_house(card_exceptions=[]):
    ranks = {}
    for rank, suit in generate_deck(card_exceptions):
        ranks.setdefault(rank, []).append(rank + suit)
    eligible_3 = []
    for cards in ranks.values():
        if len(cards) == 4:
            for i in range(4): eligible_3.append([cards[i:] + cards[:i]][:3])
        elif len(cards) == 3: eligible_3.append(cards)
    three_kind = random_item(eligible_3)

    # TODO: finish full house generator
    ranks = {}
    for rank, suit in generate_deck(card_exceptions + three_kind):
        ranks.setdefault(rank, []).append(rank + suit)
    eligible_2 = []
    for cards in ranks.values():
        if len(cards) == 4:
            for i in range(4): eligible_2.append([cards[i:] + cards[:i]][:3])
        elif len(cards) == 3: eligible_3.append(cards)
    three_kind = random_item(eligible_3)

    eligible_hands = []
    rank_counts = {rank: 4 for rank in RANKS[3:]}
    for rank, _ in card_exceptions:
        rank_counts[rank] -= 1
    rank_3 = [rank for rank, count in rank_counts.items() if count >= 3]
    rank_2 = [rank for rank, count in rank_counts.items() if count >= 2]
    for r3 in rank_3:

def generate_flush(): pass
def generate_straight(): pass
def generate_three_of_a_kind(): pass
def generate_two_pair(): pass
def generate_high_card(): pass

def generate_nothing():
    return ['__', '__', '__', '__', '__']
