import pandas as pd
from collections import Counter
import re
import math

# 读取数据
path = 'data/example.xlsx'
data = pd.read_excel(path)


# 预处理
def pretreatment(data, language='English'):
    """
    中英文文本预处理，英文去标点转化为小写；中文只保留中文字符、分词
    :param data: dataframe
    :param language: English or Chinese
    :return: articles：每个元素是一篇文章列表的列表，all_words：每个元素是一个词的列表
    """
    articles = []  # 每个元素是一篇文章列表
    all_words = []  # 每个元素是一个词
    if language == 'English':
        from string import punctuation
        for article in data:
            text = re.sub(r'[{}]+'.format(punctuation), '', str(article).lower())  # 转化为小写,去标点
            articles.append(text.split())
            all_words.extend(text.split())
    if language == 'Chinese':
        import jieba
        pattern = re.compile(r'[^\u4e00-\u9fa5]')
        for article in data:
            text = re.sub(pattern, '', str(article))  # 只保留中文字符
            jieba_list = jieba.lcut(text, cut_all=False)
            articles.append(jieba_list)
            all_words.extend(jieba_list)
    return articles, all_words


articles, all_words = pretreatment(data['正文'])

word_counts = dict(Counter(all_words))  # 统计词频
all_words_amount = len(all_words)  # 单词总数
propty = {word: (count / all_words_amount) for word, count in word_counts.items()}  # 概率


# 计算熵
def entropy(article, propty):
    result = -1
    if len(article) > 0:
        result = 0
    for word in article:
        word_propty = propty[word]
        result += (-word_propty) * math.log2(word_propty)
    return result


results = []
for article in articles:
    result = entropy(article, propty)
    results.append(result)
data['文本信息熵'] = results

data.to_excel('外国全样本信息熵.xlsx', index=False, encoding='utf8')
