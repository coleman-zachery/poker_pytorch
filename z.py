from libs.classify import player_winner_index

for item in player_winner_index(["W_", "Q♣"], ["W♥", "_♥", "_♥", "_♥", "_♥"], ["K♥", "9_", "K♦", "J♠", "XW"]):
    print(item)
