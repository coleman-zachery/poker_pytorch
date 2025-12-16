from libs.constants import RANKS, SUITS

def cardinal_subsets(x, n):
    return zip(*(x[i:len(x)-n+i+1] for i in range(n)))

#RANKS = "_?W23456789XJQKA"
#SUITS = "_?W♣♦♥♠"

def classify_poker_hand(poker_hand):
    RANK_CHARS = "_W23456789XJQKA"
    SUIT_CHARS = "_W♣♦♥♠"
    CARD_MAP = [[0 for _ in SUIT_CHARS] for _ in RANK_CHARS]
    for rank, suit in poker_hand:
        CARD_MAP[RANK_CHARS.index(rank)][SUIT_CHARS.index(suit)] += 1
    (
        (     __,     __WILD,     *__SUITS),
        ( WILD__,  WILD_WILD,  *WILD_SUITS),
                               *CARD_RANKS
    ) = CARD_MAP
    (    RANKS__, RANKS_WILD, *RANKS_SUITS) = list(zip(*CARD_RANKS))
    _REQUIREMENT = 5

    # five of a kind (cache other kinds)
    rank_counts = {}
    wild_ranks = sum([WILD__, WILD_WILD, sum(WILD_SUITS)])
    rank_counts["W"] = wild_ranks
    rank_requirement = _REQUIREMENT - wild_ranks
    for i, row in list(enumerate(CARD_RANKS, start=2))[::-1]:
        if (row_sum := sum(row)) >= rank_requirement:
            return "five of a kind", [i] * 5
        if (row_sum_wilds := row_sum + wild_ranks) > 0:
            rank_counts[row_sum_wilds] = rank_counts.get(row_sum_wilds, []) + [i]

    # royal and straight flush (cache straights and flushes)
    straight_flush_requirement = _REQUIREMENT - WILD_WILD
    suitless_straight = None
    print(CARD_MAP)
    for i, subset in enumerate(cardinal_subsets(CARD_MAP[::-1] + CARD_MAP[-1], 5)):
        print(i, subset)
        ranks__, ranks_wild, *ranks_suits = list(zip(*subset[::-1]))

        for j, suit_ranks in enumerate(ranks_suits):
            requirement = straight_flush_requirement - WILD_SUITS[j]
            sequence_count = sum([a + b > 0 for a, b in zip(ranks_wild, suit_ranks)])
            if sequence_count >= requirement:
                return ("royal flush" if i == 0 else "straight flush"), list(range(14-i,9-i,-1))

        requirement = straight_flush_requirement - WILD__ - sum(WILD_SUITS)
        sequence_count = sum([sum(rank) > 0 for rank in subset])
        if suitless_straight is None and sequence_count >= requirement:
            suitless_straight = "straight", list(range(14-i,9-i,-1))

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

    print(rank_counts)
    return

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
