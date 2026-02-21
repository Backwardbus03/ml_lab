import numpy as np

def medal_tally(athlete):
    medal_tally = athlete.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medal_tally = medal_tally.groupby("NOC").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold", ascending=False)
    medal_tally["Total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]
    return medal_tally

def country_year_list(athlete):
    year = athlete["Year"].unique().tolist()
    year.sort()
    year.insert(0, "Overall")

    Country = np.unique(athlete["region"].dropna().values).tolist()
    Country.sort()
    Country.insert(0, "Overall")

    return Country, year

def year_and_countrywise_medal_tally(df, year, country):
    flag = False
    if year == "Overall" and country == "Overall":
        pass
    if year == "Overall" and country != "Overall":
        df = df[df["region"] == country]
    if year != "Overall" and country == "Overall":
        flag = True
        df = df[df["Year"] == year]
    if year != "Overall" and country != "Overall":
        df = df[(df["Year"] == year) & (df["region"] == country)]

    if flag:
        medal_tally = df.groupby("Year").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold", ascending=False).reset_index()
    else:
        medal_tally = df.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values("Gold", ascending=False).reset_index()

    
    medal_tally["Total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]
    return medal_tally

def data_over_time(df, col):
    data = df.drop_duplicates(["Year", col])["Year"].value_counts().reset_index().sort_values("Year")
    return data

def most_successful_athletes(df, sport):
    df = df.dropna(subset=["Medal"])
    if sport != "Overall":
        df = df[df["Sport"] == sport]
    x = df["Name"].value_counts().reset_index().head(15).merge(df, left_on="Name", right_on="Name", how="left")[["Name", "count", "Sport", "region"]].drop_duplicates("Name")
    return x


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'count']

    x = x.head(10).merge(df, on='Name', how='left')[
        ['Name', 'count', 'Sport']
    ].drop_duplicates('Name')
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final