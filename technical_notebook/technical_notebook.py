#!/usr/bin/env python
# coding: utf-8

# ### Plan
#
# 1. Data cleanup
#     - Formatting issues
#     - Missing values
#
#
# 2. Exploration
#     - Visualizations
#
#
# 3. Evaluation

# ### Import Packages

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ### Functions

# In[2]:


def turn_to_int(data, column):
    data[column] = data[column].apply(lambda x: x.replace("$", ""))
    data[column] = data[column].apply(lambda x: x.replace(",", ""))
    data[column] = data[column].astype(int)


# In[3]:


def turn_to_obj(data, column):
    data[column] = data[column].astype(str)


# In[4]:


def drop_columns(data, column):
    data.drop(column, inplace=True, axis=1)


# In[5]:


def merge_dataframes(df_1, df_2):
    df_movies = pd.merge(df_1, df_2, how="left", on="title")
    return df_movies


# In[6]:


def calculate_interquartile_range(data, column):
    return data[column].describe().iloc[6] - data[column].describe().iloc[4]


# In[7]:


def drop_outliers(data, column):
    lower_outlier = [data[column].describe().loc["25%"]
                    - (1.5 * calculate_interquartile_range(data, column))]
    upper_outlier = [data[column].describe().loc["75%"]
                    + (1.5 * calculate_interquartile_range(data, column))]
    return data[(data[column] > lower_outlier)
                & (data[column] < upper_outlier)]


# In[43]:


def calculate_mean(data, column, genres):
    mean_list = []
    df_without_outlier = drop_outliers(data, column)
    for genre in genres:
        mean = round(df_without_outlier[df_without_outlier["genres"].str.contains(genre) == True].mean(), 2)
        mean_list.append(mean[column])
    return mean_list


# In[34]:


def conservative_ranking(genre, col1, col2):
    weighted_output = []
    for film in genre:
        weighted_sum = [(0.4 * df_mean.loc[film, col1])
                        + (0.6 * df_mean.loc[film, col2])]
        weighted_output.append(weighted_sum)
    return weighted_output


# In[35]:


def compromised_ranking(genre, col1, col2, col3):
    weighted_output = []
    for film in genre:
        weighted_sum = [(0.2 * df_mean.loc[film, col1])
                        + (0.4 * df_mean.loc[film, col2])
                        + (0.4 * df_mean.loc[film, col3])]
        weighted_output.append(weighted_sum)
    return weighted_output


# In[36]:


def aggressive_ranking(genre, col1, col2, col3):
    weighted_output = []
    for film in genre:
        weighted_sum = [(0.3 * df_mean.loc[film, col1])
                        + (0.4 * df_mean.loc[film, col2])
                        + (0.3 * df_mean.loc[film, col3])]
        weighted_output.append(weighted_sum)
    return weighted_output


# In[12]:


def min_and_max_values(data, column):
    return data.loc[(data[column] == data[column].min())
                    | (data[column] == data[column].max())][column]


# ### 1. Data Cleanup

# ### Read data

# In[13]:


df_budgets = pd.read_csv("files/tn.movie_budgets.csv")
df_popularity = pd.read_csv("files/tmdb.movies.csv")
df_basics = pd.read_csv("files/imdb.title.basics.csv")


# ### Update Formats

# ##### 1) Turn numeric object from string to integer

# In[14]:


turn_to_int(df_budgets, "production_budget")
turn_to_int(df_budgets, "domestic_gross")
turn_to_int(df_budgets, "worldwide_gross")


# ##### 2) Turn non-numeric object from integer to string

# In[15]:


turn_to_obj(df_basics, "start_year")


# ### Drop Columns
#

# In[16]:


drop_columns(df_popularity, ["id", "Unnamed: 0", "genre_ids",
                             "original_title", "original_language"])


# In[17]:


drop_columns(df_budgets, ["id", "release_date"])


# In[18]:


drop_columns(df_basics, ["tconst", "runtime_minutes", "original_title"])


# ### Merge datasets
#
# ##### 1) Rename

# In[19]:


df_budgets.rename(columns= {"movie": "title"}, inplace=True)


# In[20]:


df_basics.rename(columns= {"primary_title": "title"}, inplace=True)


# ##### 2) Merge

# In[21]:


df_movie = merge_dataframes(df_popularity, df_budgets)
df_movies_final = merge_dataframes(df_basics, df_movie)


# ### Missing Values

# In[22]:


df_movies_final.release_date.fillna(df_movies_final.start_year, inplace=True)


# In[23]:


drop_columns(df_movies_final, "start_year")


# ### New Columns

# In[24]:


df_movies_final["foreign_gross"] = (df_movies_final.worldwide_gross
                                    - df_movies_final.domestic_gross)


# In[25]:


df_movies_final["net_profit"] = (df_movies_final.worldwide_gross
                                 - df_movies_final.production_budget)


# ### 2. Exploration

# ##### Calculate Mean of DataFrame without Outliers

# 1) Find Interquartile Range to calculate Outliers

# In[26]:


calculate_interquartile_range(df_movies_final,
                              ["popularity", "vote_average", "vote_count"])


# In[44]:


genre = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama",
         "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi", "Thriller"]


# 2) Create new DataFrame of Means for each column based on Genre

# In[28]:


df_mean = pd.DataFrame(genre, columns=['genres'])
df_mean.set_index('genres', inplace=True)


# In[29]:


df_mean["production_budget"] = calculate_mean(df_movies_final, "production_budget", genre)

df_mean["domestic_gross"] = calculate_mean(df_movies_final, "domestic_gross", genre)

df_mean["foreign_gross"] = calculate_mean(df_movies_final, "foreign_gross", genre)

df_mean["worldwide_gross"] = calculate_mean(df_movies_final, "worldwide_gross", genre)

df_mean["net_profit"] = calculate_mean(df_movies_final, "net_profit", genre)

df_mean["popularity"] = calculate_mean(df_movies_final, "popularity", genre)

df_mean["vote_average"] = calculate_mean(df_movies_final, "vote_average", genre)

df_mean["vote_count"] = calculate_mean(df_movies_final, "vote_count", genre)

df_mean


# ##### Calculate weighted rankings for each genre
# 
#     - Conservative: 
#     - Compromised: 
#     - Aggressive: 

# In[30]:


df_rankings = pd.DataFrame(genre, columns=["genres"])
df_rankings.set_index('genres', inplace=True)


# In[45]:


df_rankings["conservative"] = conservative_ranking(df_rankings.index,
                                "production_budget", "domestic_gross")
df_rankings["compromised"] = compromised_ranking(df_rankings.index,
                                "production_budget", "domestic_gross",
                                "foreign_gross")
df_rankings["aggressive"] = aggressive_ranking(df_rankings.index,
                                "popularity", "vote_average", "vote_count")
df_rankings


# ##### Visualizations

# In[ ]:


#Graph 1


# In[ ]:


#Graph 2


# In[ ]:


#Graph 3


# In[ ]:


#Graph 4


# ### 3. Evaluation: Our recommended movie genres

# ##### - Conservative:

# In[39]:


min_and_max_values(df_rankings, 'conservative')


# ##### - Compromised:

# In[40]:


min_and_max_values(df_rankings, 'compromised')


# ##### - Aggressive:

# In[41]:


min_and_max_values(df_rankings, 'aggressive')

