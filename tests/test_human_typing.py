from hypothesis import given, strategies as st
from runner import human_typing


def test_pause_time():
    """Making sure that pause time is as long as documented.
    
    Since the value `pause_ms` is chosen at random, this test
    won't catch everything.

    """
    assert (
        0.5 <= human_typing.pause_time() <= 1
    ), "If you have updated the `pause_ms` variable, please make sure that you have also updated the documentation. Then, you can also update this test."

@given(st.characters())
def test_pick_typo(character):
    """Making sure that it only returns defined typos.

    Typos are defined in the `PLAUSIBLE_TYPOS` variable.
    """
    typo = human_typing.pick_typo(character)
    if character not in list(human_typing.PLAUSIBLE_TYPOS.keys()):
        # There shouldn't be a typo since none is defined.
        assert not typo
    else:
        if typo:
            # There isn't necessarily a typo each time.
            assert typo in human_typing.PLAUSIBLE_TYPOS[character]
        else:
            assert typo == None
