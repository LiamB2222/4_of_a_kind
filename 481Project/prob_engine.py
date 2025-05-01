# poker_ai/prob_engine.py
"""
Monte-Carlo 胜率计算 & 字符串转牌工具
"""

from treys import Card, Deck, Evaluator

__all__ = ["str_to_cards", "mc_win_prob"]

# ---------- 辅助：把形如 'Ah Kh' 的字符串转 Treys 整型列表 ----------
def str_to_cards(card_str: str):
    """
    'Ah Kh' -> [Card.new('Ah'), Card.new('Kh')]
    接受空格或逗号分隔；大小写随意。
    """
    clean = card_str.replace(',', ' ').split()
    return [Card.new(s.upper()) for s in clean]


# ---------- 核心：Monte-Carlo 胜率 ----------
def mc_win_prob(my_cards, board_cards, n_players, iters=20_000):
    """
    Monte-Carlo 估算在德州扑克牌局中获胜 (含分池) 的概率。

    Parameters
    ----------
    my_cards : list[int]   # 两张洞牌
    board_cards : list[int]# 0~5 张公共牌
    n_players : int        # 场上总玩家数(含自己)
    iters : int            # 抽样次数, 越大越准确, 2w 次约 <0.1 s

    Returns
    -------
    float  # 取值 0~1
    """
    evalr = Evaluator()
    wins = 0.0
    deck = Deck()

    # 移除已知牌
    for c in my_cards + board_cards:
        deck.cards.remove(c)

    for _ in range(iters):
        deck.shuffle()

        # 补足剩余公共牌
        need_board = 5 - len(board_cards)
        sim_board = board_cards + deck.draw(need_board)

        # 给其余 (n_players-1) 人各发两张
        villains = [deck.draw(2) for _ in range(n_players - 1)]

        hero_rank = evalr.evaluate(sim_board, my_cards)
        best_rank = hero_rank
        winners = 1  # 当前最优的人数

        for v in villains:
            r = evalr.evaluate(sim_board, v)
            if r < best_rank:          # 更强者出现
                best_rank = r
                winners = 1
            elif r == best_rank:       # 并列
                winners += 1

        if hero_rank == best_rank:     # 自己是最优者之一
            wins += 1.0 / winners      # 并列算分池

        deck.restore()                 # 还牌，保证独立试验

    return wins / iters
