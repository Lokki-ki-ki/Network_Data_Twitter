# Table of Contents
The helper functions inside following DataParser and ContentParser are used to generate the adjacancy matrix and covariates. The whole preprocessing steos can be found from these notebooks:

1. The notebook[fundamental_covariate.ipynb](./Codes/fundamental_covariates.ipynb) is used to generate the fundamental covariates in [Fundamental_Covariate](./Fundamental_Covariates/) Folder and language rates in [Language_Covariates](./Language_Covariates/) Folder.
2. The [hashtags_generation.ipynb](./Codes/hashtags_generation.ipynb) is used to generate hashtags groups reference and hashtags covariates in [Hashtags_Covariates](./Hashtags_Covariates/).
3. The [location_generation.ipynb](./Codes/location_generation.ipynb) is used for generating the locations for the users using GPT model.
4. Then [aggregate_covarites.ipynb](./Codes/aggregate_covariates.ipynb) helps to aggregate the hashtags, language covariates together into one csv file stored in [Final_Covariates](./Final_Covariates/) Folder.

If you wish to obtain intermediate results from the data preprocessing, please refer to the function's introduction within the subsequent sections.


* [DataParser](#..DataParser)
  * [DataParser](#..DataParser.DataParser)
    * [read\_data](#..DataParser.DataParser.read_data)
    * [read\_single\_csv](#..DataParser.DataParser.read_single_csv)
    * [generate\_adjacancy\_matrix](#..DataParser.DataParser.generate_adjacancy_matrix)
    * [generate\_adjacancy\_matrix\_with\_adjustment](#..DataParser.DataParser.generate_adjacancy_matrix_with_adjustment)
    * [get\_private\_users](#..DataParser.DataParser.get_private_users)
    * [get\_deleted\_users](#..DataParser.DataParser.get_deleted_users)
    * [adjacancy\_matrix\_validation](#..DataParser.DataParser.adjacancy_matrix_validation)
    * [generate\_fundamental\_covariates](#..DataParser.DataParser.generate_fundamental_covariates)
* [ContentParser](#..ContentParser)
  * [ContentParser](#..ContentParser.ContentParser)
    * [read\_retweets](#..ContentParser.ContentParser.read_retweets)
    * [read\_tweets](#..ContentParser.ContentParser.read_tweets)
    * [read\_retweets\_for\_dates](#..ContentParser.ContentParser.read_retweets_for_dates)
    * [read\_tweets\_for\_dates](#..ContentParser.ContentParser.read_tweets_for_dates)
    * [find\_language](#..ContentParser.ContentParser.find_language)
    * [generate\_language\_rate\_for\_a\_dataset](#..ContentParser.ContentParser.generate_language_rate_for_a_dataset)
    * [generate\_language\_df](#..ContentParser.ContentParser.generate_language_df)
    * [find\_hashtag](#..ContentParser.ContentParser.find_hashtag)
    * [update\_dictionary](#..ContentParser.ContentParser.update_dictionary)
    * [extract\_hashtags\_for\_tweets](#..ContentParser.ContentParser.extract_hashtags_for_tweets)
    * [generate\_hashtags\_set](#..ContentParser.ContentParser.generate_hashtags_set)
    * [generate\_matrix](#..ContentParser.ContentParser.generate_matrix)
    * [generate\_topics\_clusters](#..ContentParser.ContentParser.generate_topics_clusters)
    * [generate\_vector\_for\_hashtags\_group](#..ContentParser.ContentParser.generate_vector_for_hashtags_group)
    * [generate\_vector\_groups](#..ContentParser.ContentParser.generate_vector_groups)
    * [extract\_hashtags\_for\_tweets\_and\_users](#..ContentParser.ContentParser.extract_hashtags_for_tweets_and_users)

<a id="..DataParser"></a>
# DataParser

This DataParser contains the helper functions for adjacancy matrix generation

<a id="..DataParser.DataParser"></a>

## DataParser Objects

```python
class DataParser()
```

<a id="..DataParser.DataParser.read_data"></a>

#### read\_data

```python
def read_data(path, dates_to_include)
```

Input: \
    path: path of the data folder, which should be the /Users/ folder\
    dates_to_include: a list of dates to include, e.g. ["04-13", "04-11", "04-17"]

Output: \
    results: a dictionary of {date: dataframe}, e.g. {"04-13": df, "04-11": df, "04-17": df}
    each df contains the information for whole network

<a id="..DataParser.DataParser.read_single_csv"></a>

#### read\_single\_csv

```python
def read_single_csv(path, date)
```

Input:\
    path: path of the data folder, which should be the /Users/ folder\
    date: date of the data, e.g. "04-13"

Output:\
    df: dataframe of the data for the date containing the information for whole network

<a id="..DataParser.DataParser.generate_adjacancy_matrix"></a>

#### generate\_adjacancy\_matrix

```python
def generate_adjacancy_matrix(df, date)
```

Input:\
    df: dataframe of the data for the date containing the information for whole network\
    date: date of the data, e.g. "04-13"

Output:\
    index_to_users: a dictionary of {index: user}\
    users_to_index: a dictionary of {user: index}\
    adjacency_matrix: a numpy array of the adjacancy matrix

<a id="..DataParser.DataParser.generate_adjacancy_matrix_with_adjustment"></a>

#### generate\_adjacancy\_matrix\_with\_adjustment

```python
def generate_adjacancy_matrix_with_adjustment(df, date)
```

Input:\
    df: dataframe of the data for the date containing the information for whole network\
    date: date of the data, e.g. "04-13"

Output:\
    index_to_users: a dictionary of {index: user}\
    users_to_index: a dictionary of {user: index}\
    adjacency_matrix: a numpy array of the adjacancy matrix where 6 represents private users and 9 represents deleted users

<a id="..DataParser.DataParser.get_private_users"></a>

#### get\_private\_users

```python
def get_private_users(df)
```

Input: \
    df: dataframe of the data for the date containing the information for whole network

Output:\
    a list of private users

<a id="..DataParser.DataParser.get_deleted_users"></a>

#### get\_deleted\_users

```python
def get_deleted_users(df)
```

Input: \
    df: dataframe of the data for the date containing the information for whole network

Output: \
    a list of deleted users

<a id="..DataParser.DataParser.adjacancy_matrix_validation"></a>

#### adjacancy\_matrix\_validation

```python
def adjacancy_matrix_validation(matrix)
```

Input: \
adjacancy matrix

Output: \
plots of eigenvalues, frequency of eigenvalues and first 2 eigenvectors

<a id="..DataParser.DataParser.generate_fundamental_covariates"></a>

#### generate\_fundamental\_covariates

```python
def generate_fundamental_covariates(df)
```

Input: \
dataframe of the data for the date containing the information for whole network
  
Output: \
dataframe of the fundamental covariates

<a id="..ContentParser"></a>

# ContentParser

<a id="..ContentParser.ContentParser"></a>

## ContentParser Objects

```python
class ContentParser()
```

<a id="..ContentParser.ContentParser.read_retweets"></a>

#### read\_retweets

```python
def read_retweets(path, date)
```

Input:\
    path: path of the Retweets folder, which should be the /Retweets/ folder\
    date: date of the data, e.g. "04-13"

Output:\
    content_dict: a dictionary of {user: {retweets_id: retweets content}}

<a id="..ContentParser.ContentParser.read_tweets"></a>

#### read\_tweets

```python
def read_tweets(path, date)
```

Input:\
    path: path of the Tweets folder, which should be the /Tweets/ folder\
    date: date of the data, e.g. "04-13"

Output:\
    content_dict: a dictionary of {user: {tweets content related dic}}

<a id="..ContentParser.ContentParser.read_retweets_for_dates"></a>

#### read\_retweets\_for\_dates

```python
def read_retweets_for_dates(path, dates_to_include)
```

Input:\
    path: path of the Retweets folder, which should be the /Retweets/ folder\
    dates_to_include: a list of dates to include, e.g. ["04-13", "04-11", "04-17"]

Output:\
    results: a dictionary of {date: {user: {retweets_id: retweets content}}}

<a id="..ContentParser.ContentParser.read_tweets_for_dates"></a>

#### read\_tweets\_for\_dates

```python
def read_tweets_for_dates(path, dates_to_include)
```

Input:\
    path: tweets folder path, which should be the /Tweets/ folder\
    dates_to_include: a list of dates to include, e.g. ["04-13", "04-11", "04-17"]

Output:\
    results: a dictionary of {date: {user: {tweets content related dic}}}

<a id="..ContentParser.ContentParser.find_language"></a>

#### find\_language

```python
def find_language(tweet)
```

Input:\
single tweet

Output:\
language of the tweet

<a id="..ContentParser.ContentParser.generate_language_rate_for_a_dataset"></a>

#### generate\_language\_rate\_for\_a\_dataset

```python
def generate_language_rate_for_a_dataset(dataset)
```

Input:\
A dictionary of tweets read from read_tweets

Output:\
A dictionary of {user: {language: count}}

<a id="..ContentParser.ContentParser.generate_language_df"></a>

#### generate\_language\_df

```python
def generate_language_df(users_tweets_language)
```

Input:\
dictionary of {user: {language: count}}

Output:\
dataframe of {userid, language1, language2, ...} where language1 is the frequency of language1

<a id="..ContentParser.ContentParser.find_hashtag"></a>

#### find\_hashtag

```python
def find_hashtag(tweet)
```

Input:\
single tweet

Output:\
list of hashtags all lowercase for this single tweets

<a id="..ContentParser.ContentParser.update_dictionary"></a>

#### update\_dictionary

```python
def update_dictionary(datalist, dictionary)
```

Input:\
datalist, dict to update

Output:\
This function will update the dictionary with the datalist to generate a frequency dictionary

<a id="..ContentParser.ContentParser.extract_hashtags_for_tweets"></a>

#### extract\_hashtags\_for\_tweets

```python
def extract_hashtags_for_tweets(dataset_dic)
```

Input:\
dict of datasets

Output:\
dictionary of tweets with hashtags

<a id="..ContentParser.ContentParser.generate_hashtags_set"></a>

#### generate\_hashtags\_set

```python
def generate_hashtags_set(dataset_dic)
```

Input:\
dict of datasets which is {date : {user: {id: tweet}}} format

Output:\
hashtags dictionary which is {hashtag: count}

<a id="..ContentParser.ContentParser.generate_matrix"></a>

#### generate\_matrix

```python
def generate_matrix(tweets_hashtags, hashtags_list)
```

Input:\
tweets_hashtags, hashtags_list

Output:\
matrix of hashtags where each row is a hashtag and each column is a tweet, number in the matrix is the frequency

<a id="..ContentParser.ContentParser.generate_topics_clusters"></a>

#### generate\_topics\_clusters

```python
def generate_topics_clusters(array, hashtags_list)
```

Input:\
clustering result and hashtags_list

Output:\
dictionary of {group: [hashtags]}

<a id="..ContentParser.ContentParser.generate_vector_for_hashtags_group"></a>

#### generate\_vector\_for\_hashtags\_group

```python
def generate_vector_for_hashtags_group(hashtags_group, hashtags_list)
```

Input:\
hashtags_group, hashtags_list

Output:\
vector of hashtags_group

<a id="..ContentParser.ContentParser.generate_vector_groups"></a>

#### generate\_vector\_groups

```python
def generate_vector_groups(groups, hashtags_list)
```

Input

<a id="..ContentParser.ContentParser.extract_hashtags_for_tweets_and_users"></a>

#### extract\_hashtags\_for\_tweets\_and\_users

```python
def extract_hashtags_for_tweets_and_users(dataset)
```

Input:\
dict of datasets which is {user: {id: tweet}} format
Output:\

dict of users which is {user: {id: [hashtags]}} format

