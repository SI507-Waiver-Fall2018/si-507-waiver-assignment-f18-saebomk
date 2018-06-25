import tweepy
import nltk
import json
import sys
from nltk.corpus import stopwords

username = sys.argv[1]
tweetRange = sys.argv[2]
stopWords = set(stopwords.words('english'))
stopWords.update(["http", "https", "RT"])

def twitter_account():
    consumer_key = "KFoPyjjH5Q75dTxw9Su5TPgrB"
    consumer_secret = "pke9UKC8tkimlGZNnXQ49QNLM18fAs5OjlfuL7J7kYHhlHUVtA"
    access_token = "953646991485087745-2mFHz0wBMeEAPhBq6iMxV1QtnKbHbLF"
    access_token_secret = "mmnf2JgHX85dtaAvcIXZcc6j2XnqT79QG5hf163qZpQGU"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def word_filtering(words):
    filtered_words = []
    for word in words:
        if word[0].isalpha():
            if word not in stopWords:
                filtered_words.append(word)
    return filtered_words

def word_Freq(words_list):
    word_freq_dict = {}
    for word in words_list:
        if word not in stopWords:
            if word not in word_freq_dict:
                word_freq_dict[word] = 1
            else:
                word_freq_dict[word] += 1
    sorted_words = sorted(word_freq_dict.items(), key = lambda x:x[1], reverse = True)
    return sorted_words[:5]

def word_tagging(word_list, word_tag):
    is_tag = lambda pos: pos[:2] == word_tag
    tag_words = word_Freq(word_filtering([word for (word, pos) in nltk.pos_tag(word_list) if is_tag(pos)]))
    return tag_words

def word_sorting(word_list):
    top_tagged_words = []
    for word in word_list:
        top_words = [word[0], "(", str(word[1]), ")"]
        top_words = "".join(top_words)
        top_tagged_words.append(top_words)
    return top_tagged_words

def twt_favorited(tweet_list):
    count = 0
    for tweet in tweet_list:
        if tweet.retweeted == False:
            count = count + tweet.favorite_count
    return count

def twt_retweeted(tweet_list):
    count = 0
    for tweet in tweet_list:
        if tweet.retweeted == False:
            count = count + tweet.retweet_count
    return count

def csv_output(word_list, ofile_name = "noun_data.csv"):
    f = open(ofile_name, "w")
    f.write("{},{}\n".format("Noun", "Number"))
    f.write('\n'.join('{},{}'.format(x[0] ,x[1]) for x in word_list))
    f.close()
    print("...Another", ofile_name, "is being created...")

twitter_output = twitter_account()
tweets = twitter_output.user_timeline(screen_name = username, count = int(tweetRange), includeRts = False)
twt_text = [tweet.text for tweet in tweets if tweet.retweeted == False]

lines = [line for line in twt_text if line != '']

word_list = []
for line in lines:
    tokenized = nltk.word_tokenize(line)
    word_list.extend(tokenized)

print("USER:", username)
print("TWEETS ANALYZED:", len(tweets))
print("VERBS:", ' '.join(str(p) for p in word_sorting(word_tagging(word_list, "NN"))))
print("NOUNS:", ' '.join(str(p) for p in word_sorting(word_tagging(word_list, "VB"))))
print("ADJECTIVES:", ' '.join(str(p) for p in word_sorting(word_tagging(word_list, "JJ"))))
print("ORIGINAL TWEETS:", len(twt_text))
print("TIMES FAVORITED (ORIGINAL TWEETS ONLY):", twt_favorited(tweets))
print("TIMES RETWEETED (ORIGINAL TWEETS ONLY):", twt_retweeted(tweets))

csv_output(word_tagging(word_list, "NN"))
