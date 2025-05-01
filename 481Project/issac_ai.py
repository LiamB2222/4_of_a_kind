# poker_ai/simple_ai.py
"""
极简 Rule-Based AI：
  • 估算胜率
  • 比 pot odds 高就跟/加注，否则弃
"""

from .prob_engine import mc_win_prob

class SimplePokerAI:
    """
    act(state) -> 'fold' | 'call' | ('raise', amount)
    """
    def __init__(self, seat_id: int, total_players: int,
                 sim_iters: int = 10_000, agro_threshold: float = 0.65):
        self.seat_id = seat_id
        self.total_players = total_players
        self.sim_iters = sim_iters
        self.agro_threshold = agro_threshold

    # ------------------------------------------------------------------
    def act(self, state: dict):
        """
        state 示例
        {
          'my_cards' : [int,int],
          'board'    : list[int],   # 0~5 张
          'pot'      : int,
          'to_call'  : int,         # 跟注所需
          'min_raise': int          # 场上最小加注额
        }
        """
        win_p = mc_win_prob(
            state['my_cards'], state['board'],
            self.total_players, self.sim_iters
        )

        # pot odds = 跟注金额 / (底池+跟注金额)
        pot_odds = (state['to_call'] /
                    (state['pot'] + state['to_call'])) if state['to_call'] else 0

        # ----------- 决策逻辑 -----------
        if win_p < pot_odds - 0.02:              # 低于赔率 → 亏，弃牌
            return 'fold' if state['to_call'] else 'call'

        if win_p > self.agro_threshold and state['min_raise'] > 0:
            # 大概率优势 → 加注
            raise_amt = max(state['min_raise'],
                            int(state['pot'] * 0.75))
            return ('raise', raise_amt)

        # 其他情况 → 跟注 / 过牌
        return 'call'
