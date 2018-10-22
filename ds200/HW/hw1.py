import datascience
from datascience import *
from urllib.request import urlopen
import re
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import numpy as np

little_women_url = 'https://raw.githubusercontent.com/ehmatthes/pcc_prep/master/chapter_10/little_women.txt'
save_dir = '.'


class ChapterParser:
    def __init__(self, url, save_dir):
        self.url = url
        self.save_dir = save_dir
        self.punctuation = ['.', ',', ';', '!', '?', '\"']
        self.stop_words = set(stopwords.words('english'))
        self.word_freq = {}

    def read_url(self):
        return re.sub('\\s+', ' ', urlopen(self.url).read().decode())

    def tokenize(self, words):
        for p in self.punctuation:
            words = words.replace(p, ' ')
        words = words.strip().split()
        return words

    def chapter_word_count(self, words):
        return len(words)

    def plot_chapter_word_count(self, chap_len_list):
        fig = plt.figure(figsize=(8, 8))
        bar_width = 0.5
        chapters = tuple('chapter{}'.format(i) for i in range(1, len(chap_len_list)+1))
        idx = np.arange(len(chap_len_list))
        plt.bar(idx, tuple(chap_len_list))
        plt.xticks(idx + bar_width, chapters, rotation='vertical')
        plt.show()
        fig.savefig(fname=self.save_dir + '/chapter_word_count.png')

    def total_chapter_count(self, raw_text):
        return len(raw_text.split('CHAPTER '))

    def extract_one_chapter(self, raw_text, chapter_num):
        return raw_text.split('CHAPTER ')[chapter_num]

    def filter_stopwords(self, words):
        return [w for w in words if not w in self.stop_words]


    def cal_freq(self, words):
        for word in words:
            self.word_freq[word] = self.word_freq.get(word, 0) + 1
        self.word_freq = sorted(self.word_freq.items(),
                                key=lambda x: x[1],
                                reverse=True)

    def plot_word_freq(self, chapter_num, threshold):
        fig = plt.figure(figsize=(8, 8))
        self.word_freq = [item for item in self.word_freq if item[1] > threshold]
        words, freq = zip(*self.word_freq)
        indexes = np.arange(len(words))
        bar_width = 0.35
        bar_width = 0.35

        plt.bar(indexes, freq)
        plt.xticks(indexes + bar_width, words, rotation='vertical')
        plt.show()
        fig.savefig(fname=self.save_dir + '/chapter{}_word_frequency.png'.format(chapter_num))

    def create_wordcloud(self, words, chapter_num):
        words = ' '.join(words)
        wordcloud = WordCloud(relative_scaling=1.0,
                              stopwords=self.stop_words).generate(words)
        fig = plt.figure(figsize=(8, 8))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        fig.savefig(fname=self.save_dir + '/chapter{}-wordcloud.png'.format(chapter_num))

    def main(self, remove_stopwords=False):
        raw_txt = self.read_url()
        chapters_num = self.total_chapter_count(raw_text=raw_txt)
        chap_len_list = []
        if not remove_stopwords:
            self.save_dir = 'original_words'
            if not os.path.exists(path=self.save_dir):
                os.mkdir(path=self.save_dir)
            for i in range(chapters_num):
                chapter = self.extract_one_chapter(raw_text=raw_txt,
                                                   chapter_num=i)
                words = self.tokenize(words=chapter)
                print('----creating the wordcloud for chapter {}----'.format(i))
                self.create_wordcloud(words=words, chapter_num=i)
                chap_len = self.chapter_word_count(words=words)
                self.cal_freq(words=words)
                print('----plotting the word frequency for chapter {}----'.format(i))
                threshold = self.word_freq[int(len(set(words)) // 25)][1]
                self.plot_word_freq(chapter_num=i, threshold=threshold)
                chap_len_list.append(chap_len)
                self.word_freq = {}

        else:
            self.save_dir = 'filtered_words'
            if not os.path.exists(path=self.save_dir):
                os.mkdir(path=self.save_dir)
            for i in range(chapters_num):
                chapter = self.extract_one_chapter(raw_text=raw_txt,
                                                   chapter_num=i)
                words = self.tokenize(words=chapter)
                words = self.filter_stopwords(words=words)
                self.create_wordcloud(words=words, chapter_num=i)
                chap_len = self.chapter_word_count(words=words)
                self.cal_freq(words=words)
                print('----plotting the word frequency for chapter {}----'.format(i))
                threshold = self.word_freq[int(len(set(words)) // 25)][1]
                self.plot_word_freq(chapter_num=i, threshold=threshold)
                chap_len_list.append(chap_len)
                self.word_freq = {}

        print('----plotting the chapter length distribution----')
        self.plot_chapter_word_count(chap_len_list=chap_len_list)

    def sentiment_classify(self):
        return NotImplementedError


if __name__ == '__main__':
    cp = ChapterParser(url=little_women_url,
                       save_dir=save_dir)
    cp.main()
