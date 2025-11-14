# import RANKS and SUITS from constants.py
from libs.constants import RANKS, SUITS
import torch

def card_str_to_tuple(card_str):
    rank_char, suit_char = card_str
    rank = RANKS.index(rank_char)
    suit = SUITS.index(suit_char)
    return (rank, suit)

def card_strings_to_tensor(card_strings):
    card_tuples = [card_str_to_tuple(cs) for cs in card_strings]
    card_tensor = torch.tensor(card_tuples, dtype=torch.long)
    return card_tensor

def classify_poker_hand(card_tuples):
    ranks = [rank for rank, _ in card_tuples if rank > 2]
    rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
    wild_ranks = [rank for rank, _ in card_tuples if rank == 2]
    is_flush = len(set(suit for _, suit in card_tuples if suit > 1)) == 1
    sorted_ranks = sorted(ranks)
    # check for straight (including low-Ace straight)
    is_straight = False
    if len(sorted_ranks) >= 5:
        if sorted_ranks == list(range(sorted_ranks[0], sorted_ranks[0] + 5)):
            is_straight = True
        elif sorted_ranks[-4:] == [10, 11, 12, 13] and sorted_ranks[0] == 14:
            is_straight = True

    if is_straight and is_flush and sorted_ranks[-1] == 14:
        return "royal flush"
    elif is_straight and is_flush:
        return "straight flush"
    elif 4 in rank_counts.values():
        return "four of a kind"
    elif 3 in rank_counts.values() and 2 in rank_counts.values():
        return "full house"
    elif is_flush:
        return "flush"
    elif is_straight:
        return "straight"
    elif 3 in rank_counts.values():
        return "three of a kind"
    elif list(rank_counts.values()).count(2) == 2:
        return "two pair"
    elif 2 in rank_counts.values():
        return "one pair"
    elif len(ranks) > 0:
        return "high card"
    else:
        return "nothing"

def poker_hand_label_to_index(label):
    label_map = {
        "nothing": 0,
        "high card": 1,
        "one pair": 2,
        "two pair": 3,
        "three of a kind": 4,
        "straight": 5,
        "flush": 6,
        "full house": 7,
        "four of a kind": 8,
        "straight flush": 9,
        "royal flush": 10,
    }
    return label_map[label]

def reverse_poker_hand_index(index):
    index_map = {
        0: "nothing",
        1: "high card",
        2: "one pair",
        3: "two pair",
        4: "three of a kind",
        5: "straight",
        6: "flush",
        7: "full house",
        8: "four of a kind",
        9: "straight flush",
        10: "royal flush",
    }
    return index_map[index]

def shuffle_hand(hand):
    indices = torch.randperm(len(hand))
    shuffled = [hand[i] for i in indices]
    return shuffled

def cardinal_subsets(x, n):
    return list(zip(*(x[i:] for i in range(n))))

def random_item(items):
    return items[torch.randint(len(items), (1,)).item()]
