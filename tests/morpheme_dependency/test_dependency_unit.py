import pytest
from morpheme_dependency import DependencyParser


def test_parse():
    dp = DependencyParser()
    target = dp.parse_to_morpheme_group('お餅はあんまりすきじゃない')
    assert len(target[0]) == 3
    assert len(target[2]) == 3
