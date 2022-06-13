from bs4 import BeautifulSoup as bs
import requests
from konlpy.tag import Hannanum
import re
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import sys
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)





if __name__ == "__main__":


    title_data = ''
    count = ['1', '11', '21', '31']

    query = '금리'
    sdate = '20220601'
    edate = '20220610'

    sd1 = '20220601'
    sd2 = '20220610'

    print(sd1)

    for i in count:

        url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=' + query + '&ds=' + sdate + \
              '&de=' + edate + "&start=" + i + '&nso=so%3Ar%2Cp%3Afrom' + sd1 + 'to' + sd2
        print(url)

        response = requests.get(url)
        html_text = response.text

        soup = bs(html_text, 'html.parser')

        titles = soup.select('a.news_tit')

        for j in titles:
            title = j.get_text()
            title_data = title_data + title
            # print(title)
    title_data = re.sub(query, '', title_data)
    title_data = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', title_data)
    print(title_data)

    hannanum = Hannanum()

    sentences_tag = []
    sentences_tag = hannanum.nouns(title_data)
    print(sentences_tag)

    df = pd.DataFrame(sentences_tag, columns=['word'])
    print(df)
    df_count = df['word'].value_counts()
    df_count = df_count.head(10)
    print(df_count)

    nouns_set = ''
    nouns_set = ' '.join(sentences_tag)
    print(nouns_set)

    noun_adj_list = []

    # for word, tag in sentences_tag:
    #     if tag in ['Noun', 'Adjective']:
    #         noun_adj_list.append(word)

    result = ''
    wc = WordCloud(font_path='c:/windows/fonts/malgun.ttf',
                   background_color="white").generate(nouns_set)
    plt.figure(figsize=(15, 10))
    plt.imshow(wc)
    plt.axis('off')
    plt.show()

    # ax1 = self.fig.add_subplot(211)
    # ax2 = self.fig.add_subplot(212)
    # ax1.bar(df_count.index, df_count.values)
    #
    # ax2.imshow(wc)
    # ax2.axis('off')
    # self.canvas.draw()
    #
    # ax1.figure.clear()


# --------- 크롤링 url 입력
# query = input('검색할 키워드 입력 :')
# url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query='+ query
#
# response = requests.get(url)
# html_text = response.text
#
# soup = bs(html_text, 'html.parser')
#
# titles = soup.select('a.news_tit')
#
# title_data = ''
# for i in titles:
#     title = i.get_text()
#     title_data = title_data + title
#     #print(title)
#
#
# title_data = re.sub('#', '', title_data)
# print(title_data)
#
# kkma = Kkma()
#
# sentences_tag = []
# sentences_tag = kkma.nouns(title_data)
# print(kkma.nouns(title_data))
#
# nouns_set = ''
# nouns_set = ' '.join(sentences_tag)
# # print(nouns_set)
#
#
# # noun_adj_list = []
# #
# # for word, tag in sentences_tag:
# #     if tag in ['Noun', 'Adjective']:
# #         noun_adj_list.append(word)
# #
# # result = ''
# wc = WordCloud(font_path='c:/windows/fonts/malgun.ttf',
#               background_color="white").generate(nouns_set)
# plt.figure(figsize=(15, 10))
# plt.imshow(wc)
# plt.axis('off')
# plt.show()