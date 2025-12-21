def cardinal_subsets(x, n):
    return zip(*(x[i:len(x)-n+i+1] for i in range(n)))

#   CARD_MAP
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
    (RANKS__, RANKS_WILD, *RANKS_SUITS) = list(zip(*CARD_RANKS))
    _REQUIREMENT = 5

    # 11    five of a kind (cache other kinds)
    rank_counts = {}
    wild_ranks = sum([WILD__, WILD_WILD, sum(WILD_SUITS)])
    rank_counts["W"] = wild_ranks
    rank_requirement = _REQUIREMENT - wild_ranks
    for i, row in list(enumerate(CARD_RANKS, start=2))[::-1]:
        if (row_sum := sum(row)) >= rank_requirement:
            return "five of a kind", [i] * 5
        if row_sum > 0:
            rank_counts[row_sum] = rank_counts.get(row_sum, []) + [i]

    # 10    royal flush     /  9    straight flush (track straights for later)
    straight_flush_requirement = _REQUIREMENT - WILD_WILD
    straight = None
    for i, subset in enumerate(cardinal_subsets(CARD_MAP[::-1] + [CARD_MAP[-1]], 5)):
        ranks__, ranks_wild, *ranks_suits = list(zip(*subset[::-1]))

        for j, suit_ranks in enumerate(ranks_suits):
            requirement = straight_flush_requirement - WILD_SUITS[j]
            sequence_count = sum([a + b > 0 for a, b in zip(ranks_wild, suit_ranks)])
            if sequence_count >= requirement:
                return ("royal flush" if i == 0 else "straight flush"), list(range(14-i,9-i,-1))

        requirement = straight_flush_requirement - WILD__ - sum(WILD_SUITS)
        sequence_count = sum([sum(rank) > 0 for rank in subset])
        if (straight is None) and sequence_count >= requirement:
            straight = 5, "straight", list(range(14-i,9-i,-1))

    rank_items = []
    for key, values in rank_counts.items():
        if key == "W": continue
        for value in values:
            rank_items += [value] * key
    flat_ranks = sorted([item for row in rank_items for item in row], reverse=True)
    print(rank_items)

    #  8    four of a kind
    if kind_4 := rank_counts.get(4 - rank_counts["W"], None):
        match_4 = kind_4[0]
        remainder = [rank for rank in flat_ranks if rank != match_4]
        _return = [match_4] * 4 + remainder[:_REQUIREMENT - 4] + [0] * _REQUIREMENT
        return 8, "four of a kind", _return[:_REQUIREMENT]

    #  7    full house
    kind_2 = rank_counts.get(2, [])
    if (rank_counts["W"] == 1) and len(kind_2) > 1:
            return 7, "full house", [kind_2[0]] * 3 + [kind_2[1]] * 2
    if kind_3 := rank_counts.get(3, None):
        match_3, *_kind_2 = kind_3
        sorted_kind_2 = sorted(kind_2 + _kind_2, reverse=True)
        if len(sorted_kind_2) > 0:
            return 7, "full house", [match_3] * 3 + [sorted_kind_2[0]] * 2

    #  6    flush
    flush = None
    wild_suits = sum([__WILD, WILD_WILD, sum(RANKS_WILD)])
    flush_requirement = _REQUIREMENT - wild_suits
    for __suit, wild_suit, ranks_suit in zip(*[__SUITS] + [WILD_SUITS] + [RANKS_SUITS]):
        if sum([__suit, wild_suit, sum(ranks_suit)]) >= flush_requirement:
            flush_ranks = sorted([14] * (wild_suits + wild_suit) + [item for row in [[rank] * count for rank, count in enumerate(ranks_suit, start=2) if count > 0] for item in row] + [0] * _REQUIREMENT, reverse=True)[:_REQUIREMENT]
            if (flush is None) or flush_ranks > flush[1]:
                flush = 6, "flush", flush_ranks
    if flush: return flush

    #  5    straight
    if straight:
        return straight

    #  4    three of a kind
    if kind_3 := rank_counts.get(3 - rank_counts["W"], None):
        match_3 = kind_3[0]
        remainder = [rank for rank in flat_ranks if rank != match_3]
        _return = [match_3] * 3 + remainder[:_REQUIREMENT - 3] + [0] * _REQUIREMENT
        return 4, "three of a kind", _return[:_REQUIREMENT]

    #  3    two pair
    if len(kind_2) > 1:
        match_1, match_2, *_ = kind_2
        remainder = [rank for rank in flat_ranks if rank not in [match_1, match_2]]
        _return = [match_1] * 2 + [match_2] * 2 + remainder[:_REQUIREMENT - 4] + [0] * _REQUIREMENT
        return 3, "two pair", _return[:_REQUIREMENT]

    #  2    one pair
    if kind_2 := rank_counts.get(2 - rank_counts["W"], None):
        match_2 = kind_2[0]
        remainder = [rank for rank in flat_ranks if rank != match_2]
        _return = [match_2] * 2 + remainder[:_REQUIREMENT - 2] + [0] * _REQUIREMENT
        return 2, "one pair", _return[:_REQUIREMENT]

    #  1    high card
    if (len(remainder) > 0) and remainder[0] > 0:
        _return = remainder + [0] * (_REQUIREMENT - 1)
        return 1, "high card", _return[:_REQUIREMENT]

    #  0    nothing
    return 0, "nothing", [0] * _REQUIREMENT
