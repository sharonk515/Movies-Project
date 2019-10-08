def scale_to_millions(data, column):
    """
    Formats elements into integers (if not already) then scales in millions
    
    Parameters:
    
    data: DataFrame
    
    column: column name of DataFrame
    """
    
    data[column] = data[column].apply(lambda x: x.replace("$", ""))
    data[column] = data[column].apply(lambda x: x.replace(",", ""))
    data[column] = data[column].astype(int)
    data[column] = data[column].apply(lambda x: x / 1000000)
    return data[column]


def turn_to_obj(data, column):
    """
    Formats elements into objects.
    
    Parameters:
    
    data: DataFrame
    
    column: column name of DataFrame
    """    
    
    data[column] = data[column].astype(str)


def drop_columns(data, column):
    """
    Drops columns.
    
    Parameters:
    
    data: DataFrame
    
    column: column name of DataFrame
    """
    
    data.drop(column, inplace=True, axis=1)


def merge_dataframes(df_1, df_2):
    """
    Merges DataFrames.
    
    Parameters:
    
    df_1: Left DataFrame
    
    df_2: Right DataFrame
    """
    
    df_movies = pd.merge(df_1, df_2, how="left", on="title")
    return df_movies


def calculate_interquartile_range(data, column):
    """
    Calculate interquartile range
    
    Parameters:
    
    data: DataFrame
    
    column: column name of DataFrame
    """
    
    q3 = data[column].quantile(0.75)
    q1 = data[column].quantile(0.25)
    return q3 - q1


def drop_outliers(data, column):
    """
    Calculate outliers and drops them from the column. Lower outliers are all the values less than first quartile (25%) - 1.5*Interquartile Range. Upper outliers are all the values greater than the third quartile (75%) + 1.5*Interquartile Range. 
    
    Parameters:
    
    data: DataFrame
    
    column: column name of DataFrame
    """
    
    lower_outlier = (data[column].quantile(0.25)
                     - (1.5 * calculate_interquartile_range(data, column)))
    upper_outlier = (data[column].quantile(0.75)
                     + (1.5 * calculate_interquartile_range(data, column)))
    return data[(data[column] > lower_outlier)
                & (data[column] < upper_outlier)]


def calculate_mean(data, column, genres):
    """
    Calculates means of each column by genres after dropping the outliers.
    
    Parameters:
    
    data: DataFrame
    
    column: column name of DataFrame
    
    genres: genre to find mean for
    
    """
    
    mean_list = []
    df_without_outlier = drop_outliers(data, column)
    for genre in genres:
        mean = round(df_without_outlier[df_without_outlier["genres"].str.contains(genre)==True].mean(),2)
        mean_list.append(mean[column])
    return mean_list


def conservative_ranking(genre, mean, col1, col2):
    """
    Calculates weighted sum for conservative ranking.
    
    Parameters:
    
    genre: genre to calculate sum
    
    col1: first column to weigh
    
    col2: second column to weigh
    
    """
    
    weighted_output = []
    for film in genre:
        weighted_sum = ((0.4 * mean.loc[film, col1])
                        + (0.6 * mean.loc[film, col2]))
        weighted_output.append(weighted_sum)
    return weighted_output


def compromised_ranking(genre, mean, col1, col2, col3):
    """
    Calculates weighted sum for compromised ranking.
    
    Parameters:
    
    genre: genre to calculate sum
    
    col1: first column to weigh
    
    col2: second column to weigh
    
    col3: third column to weigh
    
    """  
    
    weighted_output = []
    for film in genre:
        weighted_sum = ((0.2 * mean.loc[film, col1])
                        + (0.4 * mean.loc[film, col2])
                        + (0.4 * mean.loc[film, col3]))
        weighted_output.append(weighted_sum)
    return weighted_output


def aggressive_ranking(genre, mean, col1, col2, col3):
    """
    Calculates weighted sum for aggressive ranking.
    
    Parameters:
    
    genre: genre to calculate sum
    
    col1: first column to weigh
    
    col2: second column to weigh
    
    col3: third column to weigh
    
    """
    
    weighted_output = []
    for film in genre:
        weighted_sum = ((0.3 * mean.loc[film, col1])
                        + (0.4 * mean.loc[film, col2])
                        + (0.3 * mean.loc[film, col3]))
        weighted_output.append(weighted_sum)
    return weighted_output


def min_and_max_values(data, column):
    """
    Returns min and max values of the column
    
    Parameters:
    
    data: DataFrame
    
    column: column name of DataFrame
    
    """
    
    return data.loc[(data[column] == data[column].min())
                    | (data[column] == data[column].max())][column]


def percent_weight_bar_graph(dataframe, x_value, y_value, hue_value):
    import seaborn as sns
    import matplotlib.pyplot as plt
    g = sns.catplot(x=x_value, y=y_value, hue=hue_value,
                    data=dataframe, kind="bar")
    sns.despine(left=False, bottom=False)

    g.fig.set_size_inches(10, 5)

    plt.ylabel("Weight Percentages")
    plt.xlabel("Ranking Type")
    plt.title("Percent of Weights")

    plt.show()

    
def weighted_ranking_bar_graph(dataframe, column, title):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    plt.figure(figsize=(12,7))

    ordered_rankings = dataframe.sort_values(by=[column])
    values = np.array(ordered_rankings[column]) 
    clrs = ['dodgerblue' if (x < max(values) and x > min(values))
            else 'salmon' for x in values]

    sns.barplot(ordered_rankings.index, values, palette=clrs)
    sns.despine(left=False, bottom=False)

    plt.ylabel("Weighted Sum of Averages")
    plt.xlabel("Genres")
    plt.title(title)

    plt.show()

    
def weighted_ranking_box_plot(dataframe, column, title):
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.boxplot(dataframe[column], color="lightsalmon")
    sns.despine(left=True)

    plt.xlabel("Weighted Sum of Averages")
    plt.title(f"{title} Distribution")

    plt.show()