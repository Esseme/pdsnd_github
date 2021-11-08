import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_city(city):
    while (city.title() != "Chicago" and city.title() != "New York" and city.title() != "Washington"):
        city = input("Which city would you like to explore? Options: chicago, new york, washington\n")
        city = city.lower()
    return city


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    city = get_city(city)
    print("Looks like you want to learn more about {}! If this is not true, restart the program".format(city.title()))
    
    # get user input for filter to use
    filter_type = ""
    filter_types = ("none", "month", "day", "both")
    while (filter_type.lower() not in filter_types):
        filter_type = input("Would you like to filter by month, day, both or no filter at all? Type \"none\" for no filter.\n")
        

    # get user input for month (options: all, january, february, ... , june)
    if (filter_type == "month" or filter_type == "both"):
        if (filter_type == "month"):
            day = "all"
        month = ""
        months = ("all", "january", "february", "march", "april", "may", "june")
        while (month.lower() not in months):
            month = input("For which month? Options: january, february, march, april, may, june?\n")
            month = month.lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    if (filter_type == "day" or filter_type == "both"):
        if (filter_type == "day"):
            month = "all"
        day = "no"
        days = ("all", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        while (day.lower() != "all" and (not any(day.title() in d for d in days) or (day.upper() == 'T' or day.upper() == 'S'))):
            day = input("For which day? Please type a day: M, Tu, W, Th, F, Sa, Su\n")
        day = [d for d in days if d.startswith(day.title())][0]
     
    if (filter_type == "none"):
        month = "all"
        day = "all"
             
            
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from start time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # filter by month and create new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    
    popular_month = df['month'].mode().values[0]
    
    print('Most Frequent Start Month:', popular_month)


    # display the most common day of week
    df['day of week'] = df['Start Time'].dt.day_name()
    
    popular_day = df['day of week'].mode().values[0]
    
    print('Most Frequent Start Day Of The Week is:', popular_day)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    
    popular_hour = df['hour'].mode().values[0]
    
    print('Most Frequent Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Frequent Start Station:', df['Start Station'].mode().values[0])


    # display most commonly used end station
    print('Most Frequent Trip:', df['End Station'].mode().values[0])


    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' -> ' + df['End Station']
    print('Most Frequent Trip:', df['Trip'].mode().values[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time:", df['Trip Duration'].sum())


    # display mean travel time
    print("Mean travel time:", df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("What is the breakdown of users?")
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    if user_types is None:
        print("No user type data to share.")
    else:
        print(user_types)
        
        
    
    # Display counts of gender
    print("\nWhat is the breakdown of gender?")
    # print value counts for each gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        if gender is None:
            print("No gender data to share.")
        else:
            print(gender)
    else:
        print("No gender data to share.")
            

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nEarliest Year Of Birth:", df['Birth Year'].min())
        print("\nMost Recent Year Of Birth:", df['Birth Year'].max())
        print("\nMost Common Year Of Birth:", df['Birth Year'].mode().values[0])
    else:
        print("\nNo birth year data to share.")
        
    print("\nThis took %s seconds." % (time.time() - start_time))   
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        view_data = input('\nWould you like to view individual trip data? Enter yes or no.\n')
        if view_data.lower() == 'yes' and city != 'washington':
            for i in range(5):
                data = "{'': '" + str(i) + "',\
                        'Start Station': '" + str(df.iloc[[i]]['Start Station'].values[0]) + "',\
                        'Start Time': '" + str(df.iloc[[i]]['Start Time'].values[0]) + "',\
                        'End Station': '" + str(df.iloc[[i]]['End Station'].values[0]) + "',\
                        'End Time': '" + str(df.iloc[[i]]['End Time'].values[0]) + "',\
                        'Trip Duration': '" + str(df.iloc[[i]]['Trip Duration'].values[0]) + "',\
                        'User Type': '" + str(df.iloc[[i]]['User Type'].values[0]) + "',\
                        'Gender': '" + str(df.iloc[[i]]['Gender'].values[0]) + "',\
                        'Birth Year': '" + str(df.iloc[[i]]['Birth Year'].values[0]) + "'}"
                data = data.replace("'", "\"")
                parsed = json.loads(data)
                print(json.dumps(parsed))
            j = 0
            see_next = input('\nSee next? Type yes or no.\n')
            while see_next.lower() == 'yes' and city != 'washington':
                j += 1
                for i in range(j*5,j*5+5):
                    data = "{'': '" + str(i) + "',\
                        'Start Station': '" + str(df.iloc[[i]]['Start Station'].values[0]) + "',\
                        'Start Time': '" + str(df.iloc[[i]]['Start Time'].values[0]) + "',\
                        'End Station': '" + str(df.iloc[[i]]['End Station'].values[0]) + "',\
                        'End Time': '" + str(df.iloc[[i]]['End Time'].values[0]) + "',\
                        'Trip Duration': '" + str(df.iloc[[i]]['Trip Duration'].values[0]) + "',\
                        'User Type': '" + str(df.iloc[[i]]['User Type'].values[0]) + "',\
                        'Gender': '" + str(df.iloc[[i]]['Gender'].values[0]) + "',\
                        'Birth Year': '" + str(df.iloc[[i]]['Birth Year'].values[0]) + "'}"
                    data = data.replace("'", "\"")
                    parsed = json.loads(data)
                    print(json.dumps(parsed))
                see_next = input('\nSee next? Enter yes or no.\n ')  
        elif city == 'washington' and view_data.lower() == 'yes':
            print("\nSorry, Gender and Birth year are not applicable to washington city\n")
                

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

