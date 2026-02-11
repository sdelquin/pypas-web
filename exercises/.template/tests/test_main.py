import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main

testdata = [
    (1, 1),
    (2, 4),
    (3, 9),
]


@pytest.mark.parametrize('x, expected', testdata)
def test_run(x, expected):
    assert main.run(x) == expected
