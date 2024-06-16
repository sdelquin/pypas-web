import os

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore


def test_run():
    assert main.run() is True
