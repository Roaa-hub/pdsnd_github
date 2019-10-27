import pandas as pd
import numpy as np
import time

CITY_DATA = {'chicago':'chicago.csv','washington':'washington.csv',
             'new_york':'new_york_city.csv'}
CITIES = ['chicago', 'new_york', 'washington']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS =   ['sunday', 'monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n'
                 '\n-------------------------------------------------\n'
                 '\n Which city would you like to preview its data:\n\n 1-Chicago. '
                  '\n 2-New_York.'
                  '\n 3-Washington. \n'
                  '---------------------------------------------------\n')
# TO DO: get user input for city (chicago, new york city, washington).
# HINT: Use a while loop to handle invalid inputs.
    while True:
        city = input('Enter city name >>> ').lower()

        if city in CITIES:
            break
        else:
            print('\nWrong entered data. Please try again.\n')

# TO DO: get user input for month(January, February, March, April, May, June, all)
    while True:
        month = input('\nEnter a month name (January, February, March, April, May, June) or type all >>> ').lower()

        if month in MONTHS:
            break
        else:
            print('\nWrong entered data. Please try again.\n')

# TO DO: get user input for day of week (monday, tuesday, ... sunday, all)
    while True:
        day = input('\nEnter a day name(Saturday, Sunday, Monday, Wednesday, Thursday, Friday) or type all >>> ').lower()

        if day in DAYS:
            break
        else:
            print('\nWrong entered data. Please try again.\n')

    print('-'*50)
    return city,month,day

def load_data(city,month,day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    #Convert start time into standard time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Get the month value from start time
    df['month'] = df['Start Time'].dt.month

    #Get the day_of_week value from start time
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    print('-'*50)
    return df

def time_stats(df):

    #Displays statistics on the most frequent times of travel.
    print("\nCalculating the peak times of travel...")
    start_time = time.time()

    #Common month from the data set
    common_month = df['Start Time'].dt.month.mode()[0]

    #Common day from the data set
    common_day = df['Start Time'].dt.weekday_name.mode()[0]

    #Common hour from the data set
    common_hour = df['Start Time'].dt.hour.mode()[0]


    print("\nThe Most Common Month is %s " % (common_month))
    print("\nThe Most Common Day is %s " % (common_day))
    print("\nThe Most Common Hour is %s " % (common_hour))

    #Calculate the total time took for processing above results
    print("\nThis took %s seconds" % (time.time() - start_time))
    print('-'*50)


def station_stats(df):

    #Displays statistics on the most popular stations and trip.
    print("\nFinding the most common travel path between the stations...")
    start_time = time.time()

    #Common start station from the data set
    common_start_station = df['Start Station'].mode()[0]
    print('\nMost commonly used start station:\n',
          common_start_station)

    #Common end station from the data set
    common_end_station = df['End Station'].mode()[0]
    print('\nMost commonly used start station:\n',
          common_end_station)

    #Common Trip Route from the data set
    frequent_trip = df.groupby(['Start Station','End Station']).size().reset_index(name = 'trips')
    sort_trips = frequent_trip.sort_values('trips', ascending = False)
    start_trip = sort_trips['Start Station'].iloc[0]
    end_trip = sort_trips['End Station'].iloc[0]

    print("\nMost Common trip is from %s to %s " % (start_trip,end_trip))

    #Calculate the total time took for processing above results
    print("\nThis took %s seconds" % (time.time() - start_time))
    print('-'*50)


def trip_duration_stats(df):

    #Displays statistics on the total and average trip duration.
    print("Calculating Trip Duration...!")
    start_time = time.time()

    #Total trip time
    total_trip_time = df['Trip Duration'].sum()

    #Mean trip time
    mean_trip_time = df['Trip Duration'].mean()

    print("\nTotal Travel Time is %s in seconds " % (total_trip_time))
    print("\nMean Travel Time is %s in seconds " % (mean_trip_time))

    #Calculate the total time took for processing above results
    print("This took %s seconds" % (time.time() - start_time))
    print('-'*50)


def user_stats(df,city):

    #Displays statistics on bikeshare users.
    print("\nProcessing Users stats..!")
    start_time = time.time()

    print("\nCounts of Users Type ")

    #To handle exception if User Type data is unavailable in the dataset
    if 'User Type' in df.columns:
        print(df['User Type'].value_counts())

    else:
        print("\nOops..! for %s User Type data is not available " % (city))
        print("\nCount's of Gender ")

    #To handle exception if Gender data is unavailable in the dataset
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())

    else:
        print("\nOops..! for %s Gender data is not available " % (city))
        print("\nStats regarding Birth Year data ")

    #To handle exception if Birth Year data is unavailable in the dataset
    if 'Birth Year' in df.columns:

        rec_birth_year = df['Birth Year'].max()
        print("\nMost Recent Birth Year is %s " % (rec_birth_year))

        old_birth_year = df['Birth Year'].min()
        print("\nMost Earliest Birth Year is %s " % (old_birth_year))

        common_birth_year = df['Birth Year'].mode()[0]
        print("\nMost Common Birth Year is %s " % (common_birth_year))

    else:
        print("\nOops..! for %s Birth Year data is not available " % (city))
        print('-'*50)

def main():
    while True:
        city,month,day = get_filters()
        df = load_data(city,month,day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        print("\nWould you like to preview sample set of the data ?? Enter yes or no >> ")
        display_data = input()
        display_data = display_data.lower()

        #To display few rows of data for user view
        x = 5
        while display_data == 'yes':
            print(df[:x])
            print("\nWould you like to see five more rows of data ?? Enter yes or no >> ")
            x += 5
            display_data = input()
            display_data = display_data.lower()

        restart = input('\nWould you like to restart the programm? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
