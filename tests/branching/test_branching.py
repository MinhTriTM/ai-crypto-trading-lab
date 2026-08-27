from src.branching.branch_generator import BranchGenerator

def test_branch_generator():
    gen = BranchGenerator()
    branches = gen.generate(max_branches=10)
    assert len(branches) == 10
    assert any(b.action=="HOLD" for b in branches)

def test_expand():
    from src.branching.branch import Branch
    gen = BranchGenerator()
    parent = Branch(symbol="BTCUSDT", action="LONG", capital=1000)
    children = gen.expand(parent, children_per_branch=3)
    assert len(children) == 3
    assert all(c.parent_id == parent.id for c in children)
