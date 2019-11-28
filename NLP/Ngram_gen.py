from collections import Counter
from jieba import lcut
from random import choice

# corpus = '''
# 风儿吹过!
# 时光的记!'''.strip().split("\n")
# corpus = [lcut(line) for line in corpus]

with open("corpus", "r",encoding='utf-8') as f:
    corpus = [lcut(line) for line in f.read().strip().split()]
# print(corpus)

# unigram
unigram = Counter(word for words in corpus for word in words)
# print(unigram)

# bigram
bigram = {w:Counter() for w in unigram.keys()}
# print(bigram)
for words in corpus:
    for i in range(len(words)-1):
        bigram[words[i]][words[i+1]] += 1
print(bigram)
print(bigram['风儿'])

# bigram-gen
def generate_text_bigram(first_word, text_length=60, freedom=3):
    # Select the first word for the text
    if first_word not in unigram:
        first_word = choice(unigram.keys())
    text = first_word
    # select the next word with the bigram algorithm
    # w: the count of all the next word of the first word, then sort by the w
    next_word = sorted(bigram[first_word], key=lambda w: bigram[first_word][w])
    for _ in range(text_length):
        if not next_word:
            break
        next_word = choice(next_word[:freedom])
        text += next_word
        next_word = sorted(bigram[next_word], key=lambda w: bigram[next_word][w])
    print("Bigram文本生成:" + text)


generate_text_bigram('我',8,10)