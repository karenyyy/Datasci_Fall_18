import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import sys
import os
import json
import time
import datetime
import re

import pandas as pd


# customize the Listener
class MyListener(StreamListener):
    def __init__(self, raw_file, csv_file, text_file, max_num=300):
        super().__init__()
        self.raw_file = raw_file
        self.csv_file = csv_file
        self.text_file = text_file
        self.max_num = max_num
        self.count = 0
        self.start_time = time.time()

    def on_data(self, data):

        if data.startswith('{"limit":'):
            return

        # make sure it's English
        tweet = json.loads(data)
        if tweet['lang'] != 'en':
            return

        user_id = tweet['user']['id']
        user_name = tweet['user']['name']
        tweet_time = tweet['created_at']
        location = tweet['user']['location']
        text = tweet['text'].strip().replace('\n', ' ').replace('\t', ' ')

        # conform user_name to str
        if user_name is not None:
            user_name = ''.join([c if ord(c) < 128 else '' for c in user_name])
            user_name = user_name.replace(',', '')
        # conform location to str
        if location is not None:
            location = ''.join([c if ord(c) < 128 else '' for c in location])
            location = location.replace(',', '')

        # conform text to str after cleansing
        text = ''.join([c if ord(c) < 128 else '' for c in text])
        text = text.replace(',', ' ')
        text = re.sub(r'\"', '', text)
        text = re.sub(r'[_]{2,}', ' ', text)
        text = ' '.join(text.split())

        # save in different formats after preprocessing
        if not os.path.isfile(self.csv_file):
            with open(self.csv_file, 'w') as f:
                f.write(','.join(['user_id', 'user_name', 'tweet_time', 'location', 'text']) + '\n')
        if not os.path.isfile(self.text_file):
            with open(self.text_file, 'w') as f:
                f.write('text\n')

        with open(self.raw_file, 'a') as f_raw, open(self.csv_file, 'a') as f_csv, open(self.text_file, 'a') as f_text:
            f_raw.write(data.strip() + '\n')
            f_csv.write(','.join(map(str, [user_id, user_name, tweet_time, location, text])) + '\n')
            f_text.write(text + '\n')

            self.count += 1

            sys.stdout.write('\r{}/{} tweets downloaded'.format(self.count, self.max_num))
            sys.stdout.flush()

            if self.count == self.max_num:
                print('\nMaximum number reached.')
                end_time = time.time()
                elapse = end_time - self.start_time
                print('It took {} seconds to download {} tweets'.format(elapse, self.max_num))
                sys.exit(0)

    def on_error(self, status):
        print(status)
        return True


class TwitterPipeline(object):
    def __init__(self):
        self.methods = ['manual', 'file']

    def welcome(self):
        # Welcome
        print('===========================================================')
        print('Welcome to the user interface of gathering tweets pipeline!')
        print('You can press "Ctrl+C" at anytime to abort the program.')
        print('===========================================================')
        print()

    def current_datetime_str(self):
        return '{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}'

    def authenticate(self):
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_secret = ''

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        return auth

    def file_print_info(self):
        print('===========================================================')
        print('Please input the file name that contains your key words.')
        print('Notes:')
        print('    The file should contain key words in one or multiple lines, and multiple key words should be separated by *COMMA*.')
        print('        For example: NBA, basketball, Lebron James')
        print('    If the file is under the current directory, you can directly type the file name, e.g., "keywords.txt".')
        print('    If the file is in another directory, please type the full file name, e.g., "C:\\Downloads\\keywords.txt" (for Windows), or "/Users/xy/Downloads/keywords.txt" (for MacOS/Linux).')

    def manual_print_info(self):
        print('===========================================================')
        print('Please input your key words (separated by comma), and hit <ENTER> when done.')

    def check_method_exist(self):
        while True:
            m = input('Type "manual" or "file" >>> ')
            if m not in self.methods:
                print('\"{}\" is an invalid input! Please try again.\n'.format(m))
                m = 'manual'
                return m
            else:
                return m

    def check_file_exist(self):
        while True:
            file_name = input('Type your file name >>> ')
            if os.path.isfile(file_name):
                return file_name
            else:
                print('"{}" is not a valid file name! Please check if the file exists.\n'.format(file_name))
                file_name = 'tmp_file'
                return file_name

    def collect_file_key_words(self, file_name):
        key_words = []
        with open(file_name, 'r') as f:
            lines = f.readlines()
            if len(lines) == 0:
                print('\n{} is an empty file!\nTask aborted!'.format(file_name))
                sys.exit(1)

            for line in lines:
                line = line.strip()
                # Detect non-ASCII characters
                for c in line:
                    if ord(c) >= 128:
                        print('\n{} contains non-ASCII characters: "{}" \nPlease remove them and try again'.format(
                            file_name, c))
                        sys.exit(1)
                # Check delimiters
                if line.count(' ') > 1 and ',' not in line:
                    print('\nMore than 1 <space> symbols exist in the key words file, but none comma exists')
                    print('I\'m confused about your keywords. Please separate your key words by commas.')
                    sys.exit(1)

                words = line.split(',')
                for w in words:
                    if len(w.strip()) > 0:
                        key_words.append(w.strip())

        # Check key_words
        if len(key_words) == 0:
            print('\nZero key words are found in {}! Please check your key words file.'.format(file_name))
            sys.exit(1)
        return key_words

    def collect_manual_key_words(self):
        while True:
            line = input('Type the key words >>> ')
            line = line.strip()

            invalid_flag = False
            # Check empty
            if len(line) == 0:
                print('\nYour input is empty! Please try again.')
                invalid_flag = True
            # Detect non-ASCII characters
            for c in line:
                if ord(c) >= 128:
                    print('\nYour input contains non-ASCII characters: "{}"! Please try again.'.format(c))
                    invalid_flag = True
                    break
            # Check delimiters
            if line.count(' ') > 1 and ',' not in line:
                print('\nMore than 1 <space> symbols exist in your input, but none comma exists')
                print('I\'m confused about your keywords. Please try again')
                invalid_flag = True

            if invalid_flag:
                continue
            else:
                break

        # Process input
        key_words = []
        for w in line.split(','):
            if len(w.strip()) > 0:
                key_words.append(w.strip())

        # Print valid key words
        key_words = list(set(key_words))
        return key_words

    def num_of_tweets(self):
        # Prompt for number of tweets to be gathered
        print('===========================================================')
        print(
            'How many tweets do you want to gather? \nInput an integer number, or just hit <ENTER> to use the default number 300.')
        num_tweets = 300
        while True:
            s = input('Input an integer >>> ')
            s = s.strip()
            if len(s) == 0:
                break
            elif s.isdigit():
                num = int(s)
                if num > 0:
                    num_tweets = num
                    break
                else:
                    print('\nPlease input a number that is greater than 0.')
            else:
                print('\nPlease input a valid integer number.')

        print('{} tweets to be gathered.'.format(num_tweets))
        return num_tweets

    def collect_key_words(self):
        print('How do you want to specify your key words?')
        keywords = []
        m = self.check_method_exist()
        if m == 'file':
            self.file_print_info()
            filename = self.check_file_exist()
            keywords = self.collect_file_key_words(filename)
        elif m == 'manual':
            self.manual_print_info()
            keywords = self.collect_manual_key_words()
        return keywords

    def streaming(self):
        print('Start gathering tweets ...')

        postfix = self.current_datetime_str()
        raw_file = 'raw_{}.json'.format(postfix)
        csv_file = 'data_{}.csv'.format(postfix)
        text_file = 'text_{}.csv'.format(postfix)

        auth = self.authenticate()
        self.welcome()
        key_words = self.collect_key_words()
        print('\n{} unique key words being used: '.format(len(key_words)), key_words)

        num_tweets = self.num_of_tweets()
        mylistener = MyListener(raw_file=raw_file, csv_file=csv_file, text_file=text_file,
                                max_num=num_tweets)
        twitter_stream = Stream(auth, mylistener)
        twitter_stream.filter(track=key_words)


if __name__ == '__main__':
    tp = TwitterPipeline()
    tp.streaming()
