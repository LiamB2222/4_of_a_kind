from poker_ai.prob_engine import str_to_cards, mc_win_prob

def test_aa_vs_random3():
    hero = str_to_cards('As Ah')
    p = mc_win_prob(hero, [], 4, iters=5000)
    assert 0.40 < p < 0.45          # 经典统计结果 ~42%

def test_top_pair_flop():
    hero  = str_to_cards('Kc Qc')
    board = str_to_cards('Qs 8d 3h')
    p = mc_win_prob(hero, board, 2, iters=5000)
    assert 0.70 < p < 0.85
