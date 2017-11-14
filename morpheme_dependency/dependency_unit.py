import CaboCha
from mecab_parser import Morpheme


# def DependenctUnit:
#     def __init

class DependencyParser:
    def __init__(self):
        self.cp = CaboCha.Parser('-f1')

    def token_to_morpheme(self, token):
        splited = token.feature.split(',')
        yomi = token.surface if len(splited) < 8 else splited[7]
        return Morpheme(token.surface,
                        splited,
                        splited[6],
                        yomi)

    def parse_to_morpheme_group(self, text):
        '''
        CaboChaの形態素グループの単位に区切る
        お餅はあんまり好きじゃない
          お餅は---D
          あんまり-D
        好きじゃない
        
        =>
        [
            [お(お:接頭詞,名詞接続,*,*,*,*,お,オ,オ),
             餅(餅:名詞,一般,*,*,*,*,餅,モチ,モチ), 
             は(は:助詞,係助詞,*,*,*,*,は,ハ,ワ)], 
            [あんまり(あんまり:副詞,助詞類接続,*,*,*,*,あんまり,アンマリ,アンマリ)],
            [すき(すき:名詞,一般,*,*,*,*,すき,スキ,スキ),
             じゃ(じゃ:助詞,副助詞,*,*,*,*,じゃ,ジャ,ジャ),
             ない(ない:助動詞,*,*,*,特殊・ナイ,基本形,ない,ナイ,ナイ)]
        ]
        '''

        def has_chunk(token):
            return token.chunk is not None

        def chunk_by(func, col):
            '''
            `func`の要素がTrueのアイテムで区切る
            https://blog.spot-corp.com/other/2016/07/19/cabocha_nlp.html
            '''
            result = []
            for item in col:
                if func(item):
                    result.append([])
                else:
                    result[-1].append(self.token_to_morpheme(item))
            return result

        tree = self.cp.parse(text)
        tokens = [tree.token(i) for i in range(tree.size())]
        head_list = [self.token_to_morpheme(token)
                     for token in filter(has_chunk, tokens)]
        tails_list = chunk_by(has_chunk, tokens)
        morpheme_groups = [[head] + tails for head, tails in
                           zip(head_list, tails_list)]
        return morpheme_groups
