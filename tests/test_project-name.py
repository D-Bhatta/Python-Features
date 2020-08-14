""" Tests for 'scripts' package """
import pytest

from scripts import scripts


def test_helloworld(capsys):
    """ Correct object argument prints """
    scripts.helloworld("cat")
    captured = capsys.readouterr()
    assert "cat" in captured.out


# This is supposed to fail
def test_helloworld_exception():
    with pytest.raises(TypeError):
        scripts.helloworld("1")
