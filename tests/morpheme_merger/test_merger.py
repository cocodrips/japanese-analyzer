import os
from morpheme_merger import MorphemeMerger

root = os.path.abspath(os.path.dirname(__file__))


def morpheme_merger():
    """
    :rtype: MorphemeMerger 
    """
    filepath = os.path.join(root, 'test_rules.xlsx')
    _mm = MorphemeMerger()
    _mm.set_rule_from_excel(filepath, 'test')
    return _mm


def test_set_rule_tree_from_excel():
    filepath = os.path.join(root, 'test_rules.xlsx')
    mm = MorphemeMerger()
    mm.set_rule_from_excel(filepath, 'test')
    assert len(mm.rule.keys()) == 2


def test_set_rule_tree_from_csv():
    filepath = os.path.join(root, 'test_pn_rule.csv')
    mm = MorphemeMerger()
    mm.set_rule_from_csv(filepath, sep='\t')
    assert len(mm.rule.keys()) == 6


def test_get_rule_pattern():
    mm = morpheme_merger()
    words, posses = mm.get_rule_pattern('今日は職場についた時点で満点')

    assert len(words) == 4
    assert words[0] == '今日は'
    assert words[1] == '職場'
    assert posses[0] == '名詞(副詞可能)->助詞(係助詞)'
