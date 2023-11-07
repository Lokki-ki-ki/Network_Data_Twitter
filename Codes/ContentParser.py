import pandas as pd
import json
import logging
import re
import numpy as np
from langdetect import detect


class ContentParser:
    def __init__(self):
        pass

    def read_retweets(self, path, date):
        """
        Input:
            path: path of the Retweets folder, which should be the /Retweets/ folder
            
            date: date of the data, e.g. "04-13"

        Output:
            content_dict: a dictionary of {user: {retweets_id: retweets content}}
        """
        with open("{}tweets_content_one_2023-{}_new.json".format(path, date), 'r') as f:
            content_dict_one = json.load(f)
            f.close()
        with open('{}tweets_content_two_2023-{}_new.json'.format(path, date), 'r') as f:
            content_dict_two = json.load(f)
            f.close()
        content_dict = {**content_dict_one, **content_dict_two}
        return content_dict
    
    def read_tweets(self, path, date):
        """
        Input:
            path: path of the Tweets folder, which should be the /Tweets/ folder

            date: date of the data, e.g. "04-13"

        Output:
            content_dict: a dictionary of {user: {tweets content related dic}}
        """
        with open("{}tweets_content_one_2023-{}.json".format(path, date), 'r') as f:
            content_dict_one = json.load(f)
            f.close()
        with open('{}tweets_content_two_2023-{}.json'.format(path, date), 'r') as f:
            content_dict_two = json.load(f)
            f.close()
        content_dict = {**content_dict_one, **content_dict_two}
        return content_dict
    
    def read_retweets_for_dates(self, path, dates_to_include):
        """
        Input:
            path: path of the Retweets folder, which should be the /Retweets/ folder
            
            dates_to_include: a list of dates to include, e.g. ["04-13", "04-11", "04-17"]

        Output:
            results: a dictionary of {date: {user: {retweets_id: retweets content}}}
        """
        results = {}
        for date in dates_to_include:
            content = self.read_retweets(path, date)
            results[date] = content
        logging.info("Retweets Data Load Complete for dates: {}".format(dates_to_include))
        return results
    
    def read_tweets_for_dates(self, path, dates_to_include):
        """
        Input: 
            path: tweets folder path, which should be the /Tweets/ folder
            dates_to_include: a list of dates to include, e.g. ["04-13", "04-11", "04-17"]

        Output:
            results: a dictionary of {date: {user: {tweets content related dic}}}
        """
        results = {}
        for date in dates_to_include:
            content = self.read_tweets(path, date)
            results[date] = content
        logging.info("Tweets Data Load Complete for dates: {}".format(dates_to_include))
        return results
    
    def find_language(self, tweet):
        """
        Input: single tweet
        Output: language of the tweet
        """
        try:
            language = detect(tweet)
        except:
            language = "unknown"
        return language

    def generate_language_rate_for_a_dataset(self, dataset):
        """
        Input: a dictionary of tweets read from read_tweets

        Output: a dictionary of {user: {language: count}}
        """
        users_tweets_language = {}
        count = 0
        for user in dataset.keys():
            users_language = {}
            if 'original' in dataset[user].keys():
                for item in dataset[user]['original']:
                    language = self.find_language(item['text'])
                    if language in users_language.keys():
                        users_language[language] += 1
                    else:
                        users_language[language] = 1
            if 'retweets' in dataset[user].keys():
                for tweet in dataset[user]['retweets']:
                    if 'text' in tweet.keys():
                        language = self.find_language(tweet['text'])
                        if language in users_language.keys():
                            users_language[language] += 1
                        else:
                            users_language[language] = 1
            users_tweets_language[user] = users_language
            count += 1
            if count % 500 == 0:
                print("Progress: ", round(count/2057, 2)*100, "%")
        return users_tweets_language
    
    def generate_language_df(self, users_tweets_language):
        """
        Input: dictionary of {user: {language: count}}

        Output: dataframe of {userid, language1, language2, ...} where language1 is the frequency of language1
        """
        df = pd.DataFrame(users_tweets_language).T
        df.fillna(0, inplace=True)
        df.reset_index(inplace=True)
        df.rename(columns={'index':'userid'}, inplace=True)
        df["userid"] = df["userid"].astype(str)
        return df
    
    def find_hashtag(self, tweet):
        """
        Input: single tweet

        Output: list of hashtags all lowercase for this single tweets
        """
        hashtags =  re.findall('(#[A-Za-z]+[A-Za-z0-9-_]+)', tweet)
        if hashtags:
            hashtags = [hashtag.lower() for hashtag in hashtags]
        return hashtags

    def update_dictionary(self, datalist, dictionary):
        """
        Input: datalist, dict to update

        Output: This function will update the dictionary with the datalist to generate a frequency dictionary
        """
        for data in datalist:
            if data in dictionary:
                dictionary[data] += 1
            else:
                dictionary[data] = 1
        return dictionary

    def extract_hashtags_for_tweets(self, dataset_dic):
        """
        Input: dict of datasets

        Output: dictionary of tweets with hashtags
        """
        dict_of_tweets = {}
        for key, value in dataset_dic.items():
            # print dictionary index
            for user, twdict in value.items():
                for id, tweet in twdict.items():
                    hashtags = self.find_hashtag(tweet)
                    hashtags = list(set(hashtags))
                    if hashtags:
                        dict_of_tweets[id] = hashtags
        logging.info("Hashtags Extracted for Tweets")
        return dict_of_tweets
    
    def generate_hashtags_set(self, dataset_dic):
        """
        Input: dict of datasets which is {date : {user: {id: tweet}}} format

        Output: hashtags dictionary which is {hashtag: count}
        """
        hashtags_dic = {}
        for key, dictionary in dataset_dic.items():
            for user, twdict in dictionary.items():
                for id, tweet in twdict.items():
                    hashtags = self.find_hashtag(tweet)
                    hashtags = list(set(hashtags))
                    if hashtags:
                        hashtags_dic = self.update_dictionary(hashtags, hashtags_dic)
        logging.info("Hashtags Dict Extracted for Tweets")
        return hashtags_dic
    
    def generate_matrix(self, tweets_hashtags, hashtags_list):
        """
        Input: tweets_hashtags, hashtags_list

        Output: matrix of hashtags where each row is a hashtag and each column is a tweet, number in the matrix is the frequency
        """
        num_hashtags = len(hashtags_list)
        matrix = np.zeros((num_hashtags, len(tweets_hashtags)))

        for i, (_, hashtags) in enumerate(tweets_hashtags.items()):
            col = np.zeros(num_hashtags)
            for hashtag in hashtags:
                if hashtag in hashtags_list:
                    col[hashtags_list.index(hashtag)] = 1
            matrix[:, i] = col
        return matrix
    
    def generate_topics_clusters(self, array, hashtags_list):
        """
        Input: clustering result and hashtags_list

        Output: dictionary of {group: [hashtags]}
        """
        groups = {}
        for i in range(len(array)):
            group = "group" + str(array[i])
            if group in groups:
                groups[group].append(hashtags_list[i])
            else:
                groups[group] = [hashtags_list[i]]
        return groups
    
    def generate_vector_for_hashtags_group(self, hashtags_group, hashtags_list):
        """
        Input: hashtags_group, hashtags_list

        Output: vector of hashtags_group
        """
        vector = np.zeros(len(hashtags_list))
        for hashtag in hashtags_group:
            if hashtag in hashtags_list:
                vector[hashtags_list.index(hashtag)] = 1
        return vector

    def generate_vector_groups(self, groups, hashtags_list):
        """
        Input
        """
        vectors_groups = {}
        for key, hashtags_group in groups.items():
            vector = self.generate_vector_for_hashtags_group(hashtags_group, hashtags_list)
            vectors_groups[key] = vector
        return vectors_groups
    
    def extract_hashtags_for_tweets_and_users(self, dataset):
        """
        Input: dict of datasets which is {user: {id: tweet}} format
        Output: dict of users which is {user: {id: [hashtags]}} format
        """
        dict_of_users = {}
        for user, twdict in dataset.items():
            dict_of_tweets = {}
            for id, tweet in twdict.items():
                hashtags = self.find_hashtag(tweet)
                hashtags = list(set(hashtags))
                if hashtags:
                    dict_of_tweets[id] = hashtags
            dict_of_users[user] = dict_of_tweets
        return dict_of_users
    
    def cosine_similarity(self, vector1, vector2):
        return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    def find_min_distance_between_vector_and_vectorgroups(self, single_vector, vectors_groups):
        min_distance = -1
        min_group = ""
        for key, vector in vectors_groups.items():
            distance = self.cosine_similarity(single_vector, vector)
            min_distance = max(min_distance, distance)
            if min_distance == distance:
                min_group = key
        return min_distance, min_group

    def generate_users_results(self, valitags, hashtags_list, vectors_groups):
        users_results = {}
        for user, twdict in valitags.items():
            groups_vectors = {}
            for id, hashtags in twdict.items():
                single_vector = self.generate_vector_for_hashtags_group(hashtags, hashtags_list)
                if single_vector.sum() == 0:
                    continue
                min_distance, min_group = self.find_min_distance_between_vector_and_vectorgroups(single_vector, vectors_groups)
                if min_group in groups_vectors:
                    groups_vectors[min_group] += 1
                else:
                    groups_vectors[min_group] = 1
            users_results[user] = groups_vectors
        return users_results
    
    def generate_matrix_for_users_and_groups(self, users_results, groups_list):
        matrix = np.zeros((len(users_results), len(groups_list)))
        for i, (user, groups) in enumerate(users_results.items()):
            for group, count in groups.items():
                matrix[i][groups_list.index(group)] = count
        return matrix

    
if  __name__ == "__main__":
    ## Test read_retwees
    parser = ContentParser()
    # content_dict = parser.read_retweets("./Retweets/", "04-13")

    ## Test read_retweets_for_dates
    # content_dict = parser.read_retweets_for_dates("./Retweets/", ["04-17"])
    # print(len(content_dict["04-17"].keys()))

    ## Test read_tweets
    content_dict = parser.read_tweets("./Tweets/", "04-13")
    print(len(content_dict.keys()))

    ## Test read_tweets_for_dates
    # content_dict = parser.read_tweets_for_dates("./Tweets/", ["04-17"])
    # print(len(content_dict["04-17"].keys()))

    ## Test generate_language_rate_for_a_dataset
    language_dict = parser.generate_language_rate_for_a_dataset(content_dict)
    print(language_dict)


    

