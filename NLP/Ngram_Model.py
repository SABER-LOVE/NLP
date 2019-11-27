"""
Ngram做的语言模型，可以根据语料训练，计算一句话的概率，以及几个乱序的字最可能合成一个字的概率
"""


import numpy as np
from collections import Counter
import jieba

# 测试语料
# corpus = "今日(11月25日)下午14:30，华为MatePad手机及全场景新品发布会将在上海举办，华为MatePad领衔的一大波新品即将发布。" \
#          " 可以看到华为MatePad采用四边超窄边框，金属外边框，左上角一枚挖孔摄像头，实现平板史上最高屏占比，视觉冲击力震撼。 " \
#          "刚刚，华为终端官方微博公布了华为MatePad最新海报，不同于此前的黑白照，这次渲染图将MatePad特色完全展现，完全可以当真机看待了。".split()

corpus = '''她的菜很好 她的菜很香 她的他很好 他的菜很香 他的她很好
很香的菜 很好的她 很菜的他 她的好 菜的香 他的菜 她很好 他很菜 菜很好'''.split()

# 语料的预处理 ----- 统计词频 + 构建字典
counter = Counter()  # 统计词频
for sentence in corpus:
    # print(sentence)
    for word in sentence:
        counter[word] += 1
counter = counter.most_common()  # 返回一个topN的结果，N没指定就是所有
print(counter)
length = len(counter)
word2id = {counter[i][0]: i for i in range(length)}
id2word = {i: w for w, i in word2id.items()}  # items()取出所有字典里面的键值对
# print(word2id)
# print(id2word)

# n-gram建模训练
unigram = np.array([i[1] for i in counter]) / sum(i[1] for i in counter)  # unigram的计算公式
# print(unigram)

bigram = np.zeros((length, length)) + 1e-8
# print(bigram)
for sentence in corpus:
    # print(len(sentence))
    sentence = [word2id[w] for w in sentence] # 句子用id的代号分隔来表示,句子的长度不变
    # print(len(sentence))
    for i in range(1, len(sentence)):
        bigram[sentence[i-1], [sentence[i]]] += 1
# print(bigram)
for i in range(length):
    bigram[i] /= bigram[i].sum()  # bigram的概率是只把这一行的相加计算，还是计算整个概率矩阵？？？有待考察
# print(bigram)

# 利于语言模型计算句子概率
def prob(sentence):
    s = [word2id[w] for w in sentence]  # 用id表示句子
    les = len(s)
    if les < 1:
        return 0
    p = unigram[s[0]]
    if les <= 2 :                  # 应该改成除了0长度之外，其他的粒度自己选择
        return p
    for i in range(1, les):
        p *= bigram[s[i-1], s[i]]    #计算概率的公式是p(w1）p(w2|w1)....p(wn|wn-1)
    return p
print(prob('菜很香'))

# 排列组合句子
# 大概思想是每次去掉其中一个值，然后递归的对剩余值进行去值，添加的操作
def permutation_and_combination(sen_ori, sen_all=None):
    sen_all = sen_all or [[]]
    length = len(sen_ori)
    if length == 1:
        sen_all[-1].append(sen_ori[0])
        sen_all.append(sen_all[-1][:-2])
        return sen_all
    for i in range(length):
        sen, word = sen_ori[:i] + sen_ori[i+1:], sen_ori[i]
        sen_all[-1].append(word)
        sen_all = permutation_and_combination(sen, sen_all)
    if sen_all[-1]:
        sen_all[-1].pop()  # pop掉list的最后一个
    else:
        sen_all.pop()
    return sen_all

# print(permutation_and_combination([1,2,3,4,5]))
# print(len(permutation_and_combination([1,2,3,4,5])))

def max_prob(words):
    """
    返回最大概率的排列组合
    :param words: 输入的字
    :return: 输出概率和排好的字
    """
    words = list(words)
    all = permutation_and_combination(words)
    pro, sen = max((prob(sentence),sentence) for sentence in all)
    return pro, ''.join(sen)

print(*max_prob(list('菜她的')))
print(*max_prob(list('香很的菜')))