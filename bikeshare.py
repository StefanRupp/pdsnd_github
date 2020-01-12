import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
valid_input_month = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
valid_input_day = ['all', 'monday', 'tuesday', 'wensday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city=0
    month=0
    day=0
    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    while city not in CITY_DATA:
        try:
            city = input('\nWhich city do you want to explore: chicago, new york city, washington?\n').lower()
            if city in CITY_DATA:
                print("Let's explore the data given for {}!" .format(city))
            else:
                print('\nNo valid input, please try again!\n')
        except:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while month not in valid_input_month:
        try:
            month = input('\nWhich month do you want to explore: all, january, february, ... , june?\n').lower()
            if month in valid_input_month:
                print("Let's explore the data given for {}!" .format(month))
            else:
                print('\nNo valid input, please try again!\n')
        except:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in valid_input_day:
        try:
            day = input('\nWhich day do you want to explore: all, monday, tuesday, ... sunday?\n').lower()
            if day in valid_input_day:
                print("Let's explore the data given for {}!" .format(day))
            else:
                print('\nNo valid input, please try again!\n')
        except:
            break

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
   
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common_month = df['month'].mode()[0]
    most_commom_month_name = months[most_common_month-1].title()
    print('The most frequent month: {}\n' .format(most_commom_month_name))

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most frequent day of the week: {}\n' .format(most_common_day))
    
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour: {}\n' .format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most frequent start station: {}\n' .format(most_common_start_station))
    
    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most frequent end station: {}\n' .format(most_common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start - End combination'] = 'starts at ' + df['Start Station'] + ' and goes to ' + df['End Station']
    most_common_combination = df['Start - End combination'].mode()[0]
    print('The most frequent combination {}\n' .format(most_common_combination))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def seconds_readability(timespan_in):
    """
    Transform time in seconds in readable time periods

    Args:
            (int) timespan_in - timespan in seconds
    Returns:
            travel_weeks - time period weeks
            travel_days - time period days
            travel_hours - time period hours
            travel_minutes - time period minutes
            travel_seconds - time period seconds
    """
    travel_weeks = timespan_in // (7*24*60*60)
    travel_days = (timespan_in % (7*24*60*60)) // (24*60*60)
    travel_hours = (timespan_in % (24*60*60)) // (60*60)
    travel_minutes = (timespan_in % (60*60)) // 60
    travel_seconds = timespan_in % 60
        
    return travel_weeks, travel_days, travel_hours, travel_minutes, travel_seconds
    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()
    print('The total travel time is {} Seconds' .format(total_travel))

    readable_time = seconds_readability(total_travel)
    print('Or\nThe total travel time is {} Weeks {} days {} hours {} minutes and {} seconds\n\n' \
          .format(readable_time[0],readable_time[1],readable_time[2],readable_time[3],readable_time[4]))
    
    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('The mean travel time is {} Seconds' .format(mean_travel))
    
    readable_time = seconds_readability(mean_travel)
    print('Or\nThe mean travel time is {} Weeks {} days {} hours {} minutes and {} seconds\n' \
          .format(readable_time[0],readable_time[1],readable_time[2],readable_time[3],readable_time[4]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print('User Types...\n')
        print(user_types)
    else:
        print('\nNo information for User Type')

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\nGender...\n')
        print(gender)
    else:
        print('\nNo information for Gender')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        print('\nThe earliest year of birth is {}' .format(earliest_year))
        most_recent = df['Birth Year'].max()
        print('\nThe most recent year of birth is {}' .format(most_recent))
        most_common_year = df['Birth Year'].mode()[0]
        print('\nThe most common year of birth is {}' .format(most_common_year))
    else:
        print('\nNo information for the year of birth')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        #if raw_data.lower() == 'yes':
            #print(df.head())
        i=0
        while raw_data.lower() == 'yes':
            print(df.iloc[i:i+5])
            i += 5
            raw_data = input('\nWould you like to see 5 more lines of raw data? Enter yes or no.\n')
            
        print('-'*40)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        print('-'*40)
        print('-'*40)

if __name__ == "__main__":
	main()
