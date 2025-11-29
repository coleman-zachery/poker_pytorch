from libs.constants import RANKS, SUITS
import torch

def cardinal_subsets(x, n):
    return zip(*(x[i:len(x)-n+i+1] for i in range(n)))

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

    _, RANKLESS_WILD, *RANKLESS_SUITS = CARD_MAP[0]
    SUITLESS_WILD, WILD_WILD, *WILD_SUITS = CARD_MAP[1]

    # five of a kind (cache other kinds)
    rank_counts = {}
    print("rank_counts")
    print(rank_counts)
    print()

    suitless_requirement = 5 - sum([SUITLESS_WILD, WILD_WILD, sum(WILD_SUITS)])
    for i, row in list(enumerate(CARD_MAP))[:1:-1]:
        if (row_sum := sum(row)) >= suitless_requirement:
            return "five of a kind", [i] * 5
        rank_counts[row_sum] = rank_counts.get(row_sum, []) + [i]

    # royal and straight flush (cache straights and flushes)
    _requirement = 5 - WILD_WILD
    suitless_straight = None
    for i, subset in enumerate(cardinal_subsets(CARD_MAP[:1:-1] + CARD_MAP[-1], 5)):
        _, wilds, *suits = list(zip(*subset))
        for j, suit in enumerate(suits):
            sequence_count = sum([a + b > 0 for a, b in zip(wilds, suit)])
            requirement = _requirement - WILD_SUITS[j]
            if sequence_count >= requirement:
                return "royal or straight flush"
        sequence_count = sum([sum(rank) > 0 for rank in subset])
        if suitless_straight is None and sequence_count >= suitless_requirement:
            suitless_straight = "straight"

#   		0	1		2	3	4	5
#   		_	W		♣	♦	♥	♠
#   0	_	0	0		0	0	0	0
#   1	W	0	0		0	0	0	0
#   								
#   2	2	0	0		0	0	0	0
#   3	3	0	0		0	0	0	0
#   4	4	0	0		0	0	0	0
#   5	5	0	0		0	0	0	0
#   6	6	0	0		0	0	0	0
#   7	7	0	0		0	0	0	0
#   8	8	0	0		0	0	0	0
#   9	9	0	0		0	0	0	0
#   10	X	0	0		0	0	0	0
#   11	J	0	0		0	0	0	0
#   12	Q	0	0		0	0	0	0
#   13	K	0	0		0	0	0	0
#   14	A	0	0		0	0	0	0

    # four of a kind
    #    sorted_ranks = [rank for rank in sort_poker_hand(poker_hand) if rank != i]
    #return "four of a kind", [i] * 4 + [sorted_ranks[0]]

    # full house
    kind_2 = sorted_rank_counts[1] + wild_ranks - 2
    if kind_2 >= 0 and sorted_rank_counts[0] + kind_2 >= 3: return "full house", [sorted_ranks[0]] * 3 + [sorted_ranks[1]] * 2

    # flush
    flush_requirement = _requirement - RANKLESS_WILD
    _, _, *suits = list(zip(*CARD_MAP[2:]))
    for i, suit in enumerate(suits):
        suit_count = sum(suit) + RANKLESS_SUITS[i] + WILD_SUITS[i]
        if suit_count >= flush_requirement:
            return "flush", None

    # straight
    if suitless_straight: return suitless_straight

    # three of a kind
    if sorted_rank_counts[0] + wild_ranks >= 3: return "three of a kind", [sorted_ranks[0]] * 3 + sorted_ranks[1:3]

    # two pair
    kind_2 = sorted_rank_counts[1] + wild_ranks - 2
    if kind_2 >= 0 and sorted_rank_counts[0] + kind_2 >= 2: return "two pair", [sorted_ranks[0]] * 2 + [sorted_ranks[1]] * 2 + [sorted_ranks[2]]

    # one pair
    if sorted_rank_counts[0] + wild_ranks >= 2: return "one pair", [sorted_ranks[0]] * 2 + sorted_ranks[1:5]

    # high card
    _ranks = sorted_ranks + [0] * (5 - len(ranks))
    if _ranks[0] > 0: return "high card", _ranks 

    # nothing
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
