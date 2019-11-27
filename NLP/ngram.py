#############################
#   使用NLTK包实现 n-gram   #
############################

# 导入相关的包
from nltk import bigrams
from nltk import ngrams


# bi-gram
def bigram(string):
    strings = string.split()
    string_bigrams = bigrams(strings)
    for grams in string_bigrams:
        print(grams)

# n-grams
def ngram(string, N):
    strings = string.split()
    string_ngrams = ngrams(strings, N)
    for grams in string_ngrams:
        print(grams)


#############################
#        实现 n-gram        #
############################
def n_gram(string, N):
    string = str(string)
    n_grams = []
    for i in range(0, len(string) - N):
        n_grams.append(string[i:i+3])
    return n_grams

def n_gram2(string, N):  # 构造字典
    output = {}
    for i in range(len(string) - N + 1):
        ngramTemp = "".join(string[i:i+N])
        if ngramTemp not in output:
            output[ngramTemp] = 0
        output[ngramTemp] += 1
    return output


if __name__ == '__main__':
    # bigram("I really like song, it's pretty awesome.")
    # ngram("I really like song, it's pretty awesome.", 3)
    # ngram("我不仅喜欢唱歌还喜欢打游戏", 3)
    # n_gram("I really like song, it's pretty awesome.", 3)
    print(n_gram2("我不仅喜欢唱歌还喜欢打游戏", 3))