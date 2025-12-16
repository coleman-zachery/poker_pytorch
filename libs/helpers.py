from libs.constants import RANKS, SUITS
from libs.classify import cardinal_subsets
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

def find_sequence(size, rank_counts, num_wilds):
    numbers = set(rank_counts.keys()) - set(0)
    if not numbers: return num_wilds >= size
    _rank_tuples = [i for i, _ in enumerate(RANKS) if i > 2]
    rank_tuples = [_rank_tuples[-1]] + _rank_tuples # allow wrapping high card to low-side
    for subset in cardinal_subsets(rank_tuples, size)[::-1]:
        if num_wilds >= len(set(subset) - numbers): return subset
    return None

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
        "five of a kind": 11,
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
        11: "five of a kind",
    }
    return index_map[index]

def shuffle_hand(hand):
    indices = torch.randperm(len(hand))
    shuffled = [hand[i] for i in indices]
    return shuffled

def random_item(items):
    return items[torch.randint(len(items), (1,)).item()]
