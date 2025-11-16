from libs.constants import RANKS, SUITS
import torch

def cardinal_subsets(x, n):
    return zip(*(x[i:] for i in range(n)))

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

#RANKS = "_?W23456789XJQKA"
#SUITS = "_?W♣♦♥♠"

def classify_poker_hand(poker_hand):

    RANK_CHARS = "_W23456789XJQKA"
    SUIT_CHARS = "_W♣♦♥♠"

    CARD_MAP = [[0] * len(SUIT_CHARS)] * len(RANK_CHARS)
    for rank, suit in poker_hand:
        CARD_MAP[RANK_CHARS.index(rank)][SUIT_CHARS.index(suit)] += 1

    requirement = 5 - sum(CARD_MAP[1])
    for i, row in list(enumerate(CARD_MAP))[:1:-1]:
        if sum(row) >= requirement:
            return "five of a kind", [i] * 5

    _requirement = 5 - CARD_MAP[1][1]
    high_cards = CARD_MAP[-5:]
    for rank_indexes in cardinal_subsets(list(range(2, 15))[::-1] + [14], 5):
        wild_column = 0




        wild_column = [rank[1] for rank in high_cards]
        for col_i in range(2, 6):
            requirement = _requirement - CARD_MAP[1][col_i]
            suit_column = [rank[col_i] for rank in high_cards]
            if sum([a + b > 0 for a, b in zip(wild_column, suit_column)]) >= requirement:
                return "royal flush", [14, 13, 12, 11, 10]

        wild_column = [rank[1] for rank in CARD_MAP[2:]]



    rank_counts = {}
    wild_ranks = 0
    for rank, suit in poker_hand:
        if rank == "W": wild_ranks += 1
        elif rank in RANK_CHARS:
            rank_int = RANK_CHARS.index(rank) + 2
            rank_counts[rank_int] = rank_counts.get(rank_int, 0) + 1
    sorted_rank_counts = sorted(rank_counts.items(), key=lambda x: (x[0], x[1]), reverse=True)
    (rank, count), *_ = sorted_rank_counts + [(0, 0)]

    if count + wild_ranks >= 5:
        return "five of a kind", [rank if wild_ranks < 5 else 14] * 5







    ranks = []
    rank_counts = {}
    wild_ranks = 0
    suit_counts = {}
    wild_suits = 0
    for rank, suit in card_tuples:
        if rank > 2:
            ranks.append(rank)
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        if rank == 2: wild_ranks += 1
        if suit > 2: suit_counts[suit] = suit_counts.get(suit, 0) + 1
        if suit == 2: wild_suits += 1

    sequence = find_sequence(5, ranks, wild_ranks)
    is_flush = sorted(suit_counts.values(), reverse=True)[0] + wild_suits >= 5
    if sequence and list(sequence) == list(range(11, 16)) and is_flush: return "royal flush", sequence
    if sequence and is_flush: return "straight flush", sequence

    if sorted_rank_counts[0] + wild_ranks == 4: return "four of a kind", [sorted_ranks[0]] * 4 + [sorted_ranks[1]]


    kind_2 = sorted_rank_counts[1] + wild_ranks - 2
    if kind_2 >= 0 and sorted_rank_counts[0] + kind_2 >= 3: return "full house", [sorted_ranks[0]] * 3 + [sorted_ranks[1]] * 2

    if is_flush: return "flush", [RANKS[-1]] * wild_ranks + sorted_ranks
    if sequence: return "straight", sequence

    if sorted_rank_counts[0] + wild_ranks >= 3: return "three of a kind", [sorted_ranks[0]] * 3 + sorted_ranks[1:3]
    kind_2 = sorted_rank_counts[1] + wild_ranks - 2
    if kind_2 >= 0 and sorted_rank_counts[0] + kind_2 >= 2: return "two pair", [sorted_ranks[0]] * 2 + [sorted_ranks[1]] * 2 + [sorted_ranks[2]]
    if sorted_rank_counts[0] + wild_ranks >= 2: return "one pair", [sorted_ranks[0]] * 2 + sorted_ranks[1:5]

    _ranks = sorted_ranks + [0] * (5 - len(ranks))
    if _ranks[0] > 0: return "high card", _ranks 
    return "nothing", _ranks

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
