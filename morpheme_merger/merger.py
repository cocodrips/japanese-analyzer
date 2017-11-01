import enum
import pandas as pd
import MeCab

from mecab_parser import Parser
from morpheme_merger import Rule


class NormType(enum.Enum):
    RAW = 0
    NORM = 1
    BASE = 2


class MorphemeMerger:
    def __init__(self):
        self.rule = None

    def get_rule_pattern(self, text, norm=NormType.NORM,
                         skip=True, mecab_args=''):
        """
        :param str          text: Target text 
        :param NormType     norm: 
        :return: (word, posses)
        """
        parser = Parser(mecab_args=mecab_args)
        morphemes = parser.parse(text)

        i = 0
        words = []
        posses = []
        n = len(morphemes)
        while i < n:
            phases, rules, _i = self._rec_tree_check(morphemes, i)
            if phases is not None:
                if skip:
                    i = _i
                else:
                    i += 1

                words.append(''.join(phases))
                posses.append('->'.join(
                    ["{}({})".format(rule.poss[0], rule.poss[1])
                     for rule in rules]))
            else:
                i += 1

        return words, posses

    def _default_noun_rule(self):
        root = {}
        rule = Rule(['名詞', 'nan', 'nan', 'nan', 'nan'])
        root[rule] = {rule: {rule: {None: None}}}
        return root

    def set_rule_tree(self, rule_file_path, sheet_name):
        """
        ルールツリーを作る
        """
        rules = pd.read_excel(rule_file_path,
                              sheetname=sheet_name)

        poss_keys = ['pos0', 'pos1', 'pos2', 'pos3', 'pos4']

        # Set default value    
        rules['min'] = pd.to_numeric(rules['min']).fillna(1)
        rules['max'] = pd.to_numeric(rules['max']).fillna(1)
        rules[poss_keys] = rules[poss_keys].astype(str)
        rules['id'] = rules['id'].astype(str)

        # ツリー生成
        root = dict()
        prev_branches = [root]
        for i, rule in rules.iterrows():
            word = rule['id']
            repeat_min = int(rule['min'])
            repeat_max = int(rule['max'])
            poss = rule[poss_keys]

            r = Rule(list(poss.values))
            current_branches = []

            # ルールの区切り列の処理
            if word != 'nan':
                for prev_branch in prev_branches:
                    # 木の構成が終了するならNoneを入れておく
                    if prev_branch is not root:
                        prev_branch[None] = None
                prev_branches = [root]

            for prev_branch in prev_branches:
                branch = prev_branch
                for i in range(0, repeat_max + 1):
                    if i == 0:
                        if repeat_min == 0:
                            current_branches.append(branch)
                        continue

                    if r not in branch:
                        # 現在のブランチにnodeがなければ追加
                        branch[r] = dict()
                    branch = branch[r]
                    current_branches.append(branch)
            prev_branches = current_branches

        # 最後の行だった場合、最後にNoneをkeyにいれておく
        for prev_branch in prev_branches:
            if prev_branch is not root:
                prev_branch[None] = None
        self.rule = root

    def _rec_tree_check(self, morphemes, index, norm=NormType.NORM):
        """
        :param [Token]  tokens 
        :param int      index: tokensの 
        :param NormType norm 
        
        :return: (取り出されたフェーズ, 
                  フェーズに適用されたRuleのリスト, 
                  どこのindexまで進んだか)
        """
        path_word = []
        path_base = []
        path_rule = []
        i = index
        is_leaf_node = False
        current_branch = self.rule
        while not is_leaf_node:
            if i >= len(morphemes):
                if None in current_branch:
                    is_leaf_node = True
                    continue
                return None, None, None

            for rule, branch in current_branch.items():
                if rule is None:
                    is_leaf_node = True
                    break
                if rule.is_match(morphemes[i]):
                    current_branch = branch
                    path_word.append(morphemes[i].word)
                    path_base.append(morphemes[i].base)
                    path_rule.append(rule)
                    if rule.poss is None:
                        is_leaf_node = True
                    i += 1
                    break
            else:
                return None, None, None

        if norm == NormType.NORM:
            if path_base[-1] != '*':
                path_word[-1] = path_base[-1]
        if norm == NormType.BASE:
            for i in range(len(path_word)):
                if path_base[i] != '*':
                    path_word[i] = path_base[i]

        return (path_word, path_rule, i)
