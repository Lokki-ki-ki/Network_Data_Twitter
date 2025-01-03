# Network Data Collection

## Introduction
This repository comprises the conclusive outcomes of a network data collection project. In this project, a user network was constructed, encompassing 2057 users, and data was gathered spanning from April 2023 to June 2023. The data includes details about users' retweet relationships and the content of tweets that pique their interest.

## Data
The final cleaned adjacancy matrix data can be found at [Adjacancy_Matrix](./Adjacancy_Matrix/) Folder, and the final covariates data can be found at [Final_Covariates](./Final_Covariates/) Folder. 
Each folder contains 18 files that were collected on the 18 timepoints from April 2023 to June 2023. Each file contains a matrix with 2057 rows, representing 2057 users in the network. 

The adjacency matrix dataset depicts the retweet relationships among users, whereas the final covariate dataset contains information related to hashtag topics (which covariates?), tweet language rates (which covariates?), and other essential user data including #original tweets,  #retweets, #replies, #quotes, #followers, #following, #tweets, account verified or not (which covariates?). The file "location.json" gives the location of users according to their announcement. 

Over time, users who have closed their public pages (denoted as 6) or been closed by tweets (denoted by 9) are identified in the adjacency matrix.

## Raw Data Introduction
There are three folders for raw data, which is [Tweets](./Retweets/), [Retweets](./Retweets/) and [Users](./Users/).

Users table contains 19 columns, which includes: 

`'id', 'name', 'username', 'numberOfFollowers', 'numberOfFollowing','numberOfTweets', 'created_at', 'verified', 'description', 'location', 'numberOfOriginalTweets', 'numberOfRetweets', 'numberOfReplies', 'numberOfQuotes', 'retweet_ids', 'retweet_users', 'reply_users', 'quote_users', 'tweets_id'`

Tweets json file contains the tweets, retweets and replies information for users. The key for json file is the userid (which is id in Users table). Take one user `'1146549086872408069'` from [tweets_content_one_2023-04-22]('./Tweets/tweets_content_one_2023-04-22.json') as an example:


    {'original': [],

    'retweets': [
        {'referenced_tweets': [{'type': 'retweeted',
            'id': '1649595756515586049'}],
        'text': 'RT @shutupmikeginn: you’ve got to fuck up so bad to not get $8 out of me. i’m stupid, i’ll spend $8 on anything',
        'author_id': '1146549086872408069',
        'id': '1649797446187520003'},
        {'referenced_tweets': [{'type': 'retweeted', 'id': '1649545443951386626'}],
        'text': 'RT @SoccerMouaz: As the Assad regime blocked aid and bombed earthquake victims @syrianetf took @60Minutes to Syria for two days to intervie…',
        'author_id': '1146549086872408069',
        'id': '1649796787690172424'}
    ],

    'replies': [
        {'referenced_tweets': [{'type': 'replied_to',
        'id': '1649488337290559488'}],
        'text': '@majornelson #XboxFreeCodeFriday I’d stay where I was and fortify it. Would make periodic runs for food, fuel, and medicine.',
        'author_id': '1146549086872408069',
        'id': '1649515699600232448'}
    ],

    'quotes': []

    }

As some of the retweets information has been truncated due to the API limitation, additional full retweets information has been collected inside Retweets folder. Take the same user as an example:

    {'1649595756515586049': 'you’ve got to fuck up so bad to not get $8 out of me. i’m stupid, i’ll spend $8 on anything',
    '1649545443951386626': 'As the Assad regime blocked aid and bombed earthquake victims @syrianetf took @60Minutes to Syria for two days to interview SAMS and @SyriaCivilDef please tune in this Sunday https://t.co/4G7EBXJTgw',
    '1649552095182483456': 'Ramadan is difficult for a lot of people, especially those suffering in Palestine. It’s Eid, but they have little reason to celebrate. If you can, join me and donate that $8 Elon wants for Blue to MAP, which is helping Palestinians with medical aid. https://t.co/4ylCMbUzCj https://t.co/xQWp3XMD5r',
    '1649589562992099328': 'Playoff hockey https://t.co/vNDWN9KFGj',
    ...} 

* Notice: due to time range and API limitation issues, some of the retweets in Tweets json files might not be able to be collected at the time we conducted additional fetching. Hence, please use the truncated content in original json file instead.

## Data Preprocessing and Output Format

Inside [Codes](./Codes/) folder contains the data preprocessing scripts for processing the above raw data. Two helper class have been developed, which are [DataParser](./Codes/DataParser.py) and [ContentParser](./Codes/ContentParser.py). DataParser is for processing the csv data while ContentParsr is for processing the json file.

The details of usage has been written in [CodesReadme](./Codes/Codes.md). And the jupyter notebook in Codes folder contain the notebook for how to preprocessing the whole raw dataset using these two helper class.

- The [adjacancy_matrix](./Codes/adjacancy_matrix.ipynb) is used to generate the adjacancy matrix based on information using retweets relation between users.

- The [fundamental_covariate.ipynb](./Codes/fundamental_covariates.ipynb) is used to generate the fundamental covariates in [Fundamental_Covariate](./Fundamental_Covariates/) Folder and language rates in [Language_Covariates](./Language_Covariates/) Folder.

- The [hashtags_generation.ipynb](./Codes/hashtags_generation.ipynb) is used to generate hashtags groups reference and hashtags covariates in [Hashtags_Covariates](./Hashtags_Covariates/).

- The [location_generation.ipynb](./Codes/location_generation.ipynb) is used for generating the locations for the users using GPT model.

- Then [aggregate_covarites.ipynb](./Codes/aggregate_covariates.ipynb) helps to aggregate the hashtags, language covariates together into one csv file stored in [Final_Covariates](./Final_Covariates/) Folder.

The steps of generating each covariates have been ellaborated inside the jupyter notebook.
