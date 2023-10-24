"""
This DataParser contains the helper functions for adjacancy matrix generation
"""
import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
class DataParser:
    def __init__(self):
        pass

    def read_data(self, path, dates_to_include):
        results = {}
        for date in dates_to_include:
            df = self.read_single_csv(path, date)
            results[date] = df
        logging.info("Data Load Complete for dates: {}".format(dates_to_include))
        return results

    def read_single_csv(self, path, date):
        df1 = pd.read_csv(f'{path}users_data_one_2023-{date}.csv', engine='python')
        df2 = pd.read_csv(f'{path}users_data_two_2023-{date}.csv', engine='python')
        df2.drop([228, 229], inplace=True)
        df = pd.concat([df1, df2], ignore_index=True)
        df.reset_index(drop=True, inplace=True)
        df["id"] = df["id"].astype(str)
        return df
    
    def generate_adjacancy_matrix(self, df, date):
        # Construct a dictionary of {user: index} and {index: user}
        users_to_index = {}
        index_to_users = {}
        count = 0
        for index, row in df.iterrows():
            users_to_index[row["id"]] = count
            index_to_users[count] = row["id"]
            count += 1
        df["retweet_users"] = df["retweet_users"].astype(str)
        retweets_dict = {}
        # If retweet the same tweet, there is relationship between two users
        for index, row in df.iterrows():
            retweets = row["retweet_users"].split(";")
            for retweet in retweets:
                if retweet in retweets_dict.keys():
                    retweets_dict[retweet].append(row["id"])
                else:
                    retweets_dict[retweet] = [row["id"]]
        
        adjacency_matrix = np.zeros((df.shape[0], df.shape[0]))
        for key, value in retweets_dict.items():
            for i in range(len(value)):
                for j in range(i+1, len(value)):
                    adjacency_matrix[users_to_index[value[i]], users_to_index[value[j]]] = 1
                    adjacency_matrix[users_to_index[value[j]], users_to_index[value[i]]] = 1
        logging.info("Adjacency Matrix Generated for date: {}".format(date))
        return index_to_users, users_to_index, adjacency_matrix
    
    def generate_adjacancy_matrix_with_adjustment(self, df, date):
        index_to_users, users_to_index, adjacency_matrix = self.generate_adjacancy_matrix(df, date)
        # Get the list of private users and deleted users
        private_users = self.get_private_users(df)
        deleted_users = self.get_deleted_users(df)
        # use 6 to replace the relationship for private users
        for user in private_users:
            adjacency_matrix[users_to_index[user], :] = 6
            adjacency_matrix[:, users_to_index[user]] = 6
        # use 9 to replace the relationship for deleted users
        for user in deleted_users:
            adjacency_matrix[users_to_index[user], :] = 9
            adjacency_matrix[:, users_to_index[user]] = 9
        logging.info("Adjacency Matrix Generated with Adjustment for date: {}".format(date))
        return index_to_users, users_to_index, adjacency_matrix

    def get_private_users(self, df):
        private = df[df["numberOfRetweets"].isnull() & df["numberOfFollowers"].notnull()]
        return private["id"].tolist()

    def get_deleted_users(self, df):
        delete = df[df["numberOfRetweets"].isnull() & df["numberOfFollowers"].isnull()]
        return delete["id"].tolist()
    
    def adjacancy_matrix_validation(self, matrix):
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        eigenvalues_freq = eigenvalues / eigenvalues.sum()
        sorted_eigenvalues_freq = sorted(eigenvalues_freq, reverse=True)[:50]
        ## Plot the frequency of eigenvalues
        plt.plot(sorted_eigenvalues_freq)
        plt.xlabel('Eigenvalue')
        plt.ylabel('Frequency')
        plt.title('Scree Plot')
        plt.show()

        ## Plot first 2 eigenvectors scatter plot
        sorted_eigenvectors = eigenvectors[:, eigenvalues.argsort()[::-1]]
        plt.scatter(sorted_eigenvectors[:, 0], sorted_eigenvectors[:, 1])
        plt.xlabel('First Eigenvector')
        plt.ylabel('Second Eigenvector')
        plt.title('First 2 Eigenvectors Scatter Plot')
        plt.show()

        ## Degree Validation
        degree = matrix.sum(axis=0)
        plt.hist(degree, bins=200)
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.title('Degree Distribution')
        plt.show()

    def generate_fundamental_covariates(self, df):
        columns_to_include = ['id', 'numberOfOriginalTweets', 'numberOfRetweets',
        'numberOfReplies', 'numberOfQuotes', 'numberOfFollowers',
        'numberOfFollowing', 'numberOfTweets', 'verified']
        df["verified"] = np.where(df["verified"] == True, 1, 0)
        final_df = df[columns_to_include]
        return final_df
    
if __name__ == "__main__":
    parser = DataParser()
    ## Test read_single_csv
    df = parser.read_single_csv("./Users/", "04-11")
    print(df.shape)

    ## Test read_data
    dates_to_include = ["04-13", "04-11", "04-17"]
    results = parser.read_data("./Users/", dates_to_include)
    print(results["04-13"].shape)

    ## Test generate_adjacancy_matrix
    # df = results["04-13"]
    # index_to_users, users_to_index, adjacency_matrix = parser.generate_adjacancy_matrix(df, "04-13")

    ## Test generate_adjacancy_matrix_with_adjustment
    # df = results["04-13"]
    # index_to_users, users_to_index, adjacency_matrix = parser.generate_adjacancy_matrix_with_adjustment(df, "04-13")

    ## Test adjacancy_matrix_validation
    # parser.adjacancy_matrix_validation(adjacency_matrix)

    ## Test generate_fundamental_covariates
    df = results["04-13"]
    final_df = parser.generate_fundamental_covariates(df)
    print(final_df.shape)
    print(final_df.head())


