from konlpy_tc.tag import Okt_edit
import emoji
import re


class Threecow():

    def __init__(self):
        self.emoji_dic = emoji.UNICODE_EMOJI
        self.emoji_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
        self.re_emoji = re.compile('|'.join(re.escape(p) for p in self.emoji_list))
        self.okt_edit = Okt_edit()
        
       

    def emoticon(self, result):
        emo_lst = []
        for idx, (token, _) in enumerate(result):
            if re.search(self.re_emoji, token):
                lst = [(x+'_'+self.emoji_dic[x][1:-1], 'Emoji') for x in token]
                emo_lst.append((idx, lst))
        emo_lst.reverse()
        for idx, emo in emo_lst:
            result.pop(idx)
            result[idx:idx] = emo
        return result
    
    def hashtag(self, result):
        for idx, (token, tag) in enumerate(result):
            if tag == 'Hashtag':
                phrase = self.okt_edit.phrases(token[1:])[0]
                new_token = re.sub(phrase, ' '+phrase+' ' , token[1:]).strip().split()
                h = []
                for x in new_token:
                    if x == phrase:
                        h.append((x, 'Hashtag_Noun'))
                    else:
                        tmp = self.okt_edit.pos(x)
                        for token, tag in tmp:
                            h.append((token, 'Hashtag_'+tag))         
                result[idx] = tuple(h)
        return result

    def tagger(self, text):
        result = self.okt_edit.pos(text)
        result = self.emoticon(result)
        result = self.hashtag(result)
        return result

    def tokenizer(self, text):
        tag_result = self.tagger(text)
        token_lst = []
        for x in tag_result:
            if type(x[0]) == str:
                token_lst.append(x[0])
            else:
                for y in x:
                    token_lst.append(y[0])
        return token_lst
            
if __name__ == "__main__":
    text = '다이어트 해야되는데...😂😂\n.\n.\n.\n#멋짐휘트니스연산점 #연산동pt'
    text2 = '술스타그램 그자체❤❤\n#럽스타그램 #운동하는커플 #태닝'
    text3 = '서피비치'
    threecow = Threecow()
    print('='*100)
    print('\nThreecow : ', threecow.tagger(text2))
    print('\n', '='*100)
    print('\ntokenize 결과: ')
    print(threecow.tokenizer(text2))