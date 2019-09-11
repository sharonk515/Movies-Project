#!/usr/bin/env python
# coding: utf-8

# ### Functions


def turn_to_int(data, column):
    data[column] = data[column].apply(lambda x: x.replace("$", ""))
    data[column] = data[column].apply(lambda x: x.replace(",", ""))
    data[column] = data[column].astype(int)


def turn_to_obj(data, column):
    data[column] = data[column].astype(str)


def drop_columns(data, column):
    data.drop(column, inplace=True, axis=1)


def merge_dataframes(df_1, df_2):
    df_movies = pd.merge(df_1, df_2, how="left", on="title")
    return df_movies


def calculate_interquartile_range(data, column):
    return data[column].describe().iloc[6] - data[column].describe().iloc[4]


def drop_outliers(data, column):
    lower_outlier = [data[column].describe().loc["25%"]
                     - (1.5 * calculate_interquartile_range(data, column))]
    upper_outlier = [data[column].describe().loc["75%"]
                     + (1.5 * calculate_interquartile_range(data, column))]
    return data[(data[column] > lower_outlier)
                & (data[column] < upper_outlier)]


def calculate_mean(data, column, genres):
    mean_list = []
    df_without_outlier = drop_outliers(data, column)
    for genre in genres:
        mean = round(df_without_outlier[df_without_outlier["genres"].str.contains(genre)==True].mean(),2)
        mean_list.append(mean[column])
    return mean_list


def conservative_ranking(genre, col1, col2):
    weighted_output = []
    for film in genre:
        weighted_sum = [(0.4 * df_mean.loc[film, col1])
                        + (0.6 * df_mean.loc[film, col2])]
        weighted_output.append(weighted_sum)
    return weighted_output


def compromised_ranking(genre, col1, col2, col3):
    weighted_output = []
    for film in genre:
        weighted_sum = [(0.2 * df_mean.loc[film, col1])
                        + (0.4 * df_mean.loc[film, col2])
                        + (0.4 * df_mean.loc[film, col3])]
        weighted_output.append(weighted_sum)
    return weighted_output


def aggressive_ranking(genre, col1, col2, col3):
    weighted_output = []
    for film in genre:
        weighted_sum = [(0.3 * df_mean.loc[film, col1])
                        + (0.4 * df_mean.loc[film, col2])
                        + (0.3 * df_mean.loc[film, col3])]
        weighted_output.append(weighted_sum)
    return weighted_output


def min_and_max_values(data, column):
    return data.loc[(data[column] == data[column].min())
                    | (data[column] == data[column].max())][column]