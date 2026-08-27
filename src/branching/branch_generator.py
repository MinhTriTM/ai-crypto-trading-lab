"""BranchGenerator - sinh cac branch tu mot market state."""
from typing import List
import itertools, uuid
from .branch import Branch
from .dimensions.asset import AssetDimension
from .dimensions.direction import DirectionDimension
from .dimensions.position_size import PositionSizeDimension
from .dimensions.leverage import LeverageDimension
from .dimensions.time_offset import TimeOffsetDimension
from .dimensions.latency import LatencyDimension
from .dimensions.exit_time import ExitTimeDimension
from .dimensions.market_scenario import MarketScenarioDimension

class BranchGenerator:
    def __init__(self):
        self.asset_dim = AssetDimension()
        self.dir_dim = DirectionDimension()
        self.size_dim = PositionSizeDimension()
        self.lev_dim = LeverageDimension()
        self.time_dim = TimeOffsetDimension()
        self.lat_dim = LatencyDimension()
        self.exit_dim = ExitTimeDimension()
        self.scenario_dim = MarketScenarioDimension()

    def generate(self, parent: Branch | None = None, max_branches: int = 100) -> List[Branch]:
        branches: List[Branch] = []
        parent_id = parent.id if parent else None
        base_capital = parent.capital if parent else 1000.0
        # dam bao HOLD luon co mat, du max_branches nho
        hold_branch = Branch(parent_id=parent_id, symbol="BTCUSDT", action="HOLD", capital=base_capital)
        # neu max_branches ==1 thi chi tra HOLD
        if max_branches <= 1:
            return [hold_branch]
        # to hop co ban: asset x direction x size x leverage, chu tru slot cho HOLD
        for asset in self.asset_dim.values()[:3]:
            for direction in self.dir_dim.values():
                for size in self.size_dim.values()[:3]:
                    for lev in self.lev_dim.values()[:2]:
                        if len(branches) >= max_branches - 1:
                            break
                        branches.append(Branch(
                            parent_id=parent_id,
                            symbol=asset,
                            action=direction,
                            capital=base_capital,
                            position_pct=size/100,
                            leverage=lev,
                            decision_offset_ms=self.time_dim.sample(),
                            data_latency_ms=self.lat_dim.sample_data(),
                            order_latency_ms=self.lat_dim.sample_order(),
                            target=10000.0,
                            depth=(parent.depth+1) if parent else 0
                        ))
        # them HOLD cuoi
        branches.append(hold_branch)
        return branches[:max_branches]

    def expand(self, branch: Branch, children_per_branch: int = 7) -> List[Branch]:
        # sinh con: HOLD, CLOSE 25%, CLOSE 100%, ADD 5%, ADD 20%, REVERSE, wait 10ms
        actions = ["HOLD", "CLOSE_25", "CLOSE_100", "ADD_5", "ADD_20", "REVERSE", "WAIT_10MS"]
        children = []
        for act in actions[:children_per_branch]:
            child = Branch(
                parent_id=branch.id,
                symbol=branch.symbol,
                action=act,
                capital=branch.capital,
                position_pct=branch.position_pct,
                leverage=branch.leverage,
                depth=branch.depth+1
            )
            children.append(child)
        return children
