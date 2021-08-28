import time
import pandas as pd
import numpy as np

#Sources: https://docs.python.org/3/library/stdtypes.html#dict-views
#         https://stackoverflow.com/questions/55719762/how-to-calculate-mode-over-two-columns-in-a-python-dataframe
#         https://stackoverflow.com/questions/51528579/python-missing-1-required-positional-argument
#         Practice problems 1, 2, and 3
#         Review from first submission

#Possible city selections and associated data file
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'new york': 'new_york_city.csv'}

#Possible month selections
MONTH_DATA = ('january', 'february', 'march', 'april', 'may', 'june', 'all')

#Possible day selections
DAY_DATA = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please select Chicago, New York City or Washington: ').lower()

    while city not in CITY_DATA:
        city = input('Please select Chicago, New York City or Washington: ').lower()

    if city in ['chicago', 'new york city', 'new york', 'washington']:
        print ('Thank you for your input! You have selected ' + city.capitalize() + '.')

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Please select a month or "all" for unfiltered data: ').lower()

    while month not in MONTH_DATA:
        month = input('Sorry, we don\'t have data for that month, please select a month from January through June or "all": ').lower()

    if month != 'all':
        print('Thank you, your data will come from ' + month.capitalize() + '.')

    else:
        print('Thank you, your data will not be filtered by month.')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please select a day of the week or type "all" for unfiltered data: ').lower()

    while day not in DAY_DATA:
        day = input('Sorry, I don\'t recognize that day. Please select a day of the week (ex. Monday) or "all" for no filter: ').lower()

    if day != 'all':
        print('Thank you, your data will come from ' + day.capitalize() + '.')

    else:
        print('Thank you, your data will not be filtered by day.')

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
    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert the 'Start Time' colume to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month & day of the week from 'Start Time' to cerate new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filter by month if applicable
    if month != 'all':
        #use index of months to get corresponding int
        month = MONTH_DATA.index(month) + 1

        #filter by month to create new data frame
        df = df[df['month'] == month]

    #filter by day of week if applicable
    if day != 'all':
        #filter by day of week to creat new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    if common_month == '1':
        print('The most common month in {} is January.'.format(city.capitalize()))

    elif common_month == '2':
        print('The most common month in {} is February.'.format(city.capitalize()))

    elif common_month == '3':
        print('The most common month in {} is March.'.format(city.capitalize()))

    elif common_month == '4':
        print('The most common month in {} is May.'.format(city.capitalize()))

    else:
        print('The most common month in {} is June.'.format(city.capitalize()))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]

    print('The most common day with your chosen filters is ' + common_day.capitalize() + '.')

    #Extract hour from 'Start Time' column to create an hour colume
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour with your chosen filters is {}.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station with your chosen filters is {}.'.format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station with your chosen filters is {}.'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    popular_station_combo = (df['Start Station'] + ' ----> ' + df['End Station']).mode()[0]
    print('The most popular start and end station combination with your chosen filters is {}.'.format(popular_station_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_travel_min = sum(df['Trip Duration'])
    tot_travel_hr = tot_travel_min/60
    tot_travel_day = tot_travel_hr/24
    print('Total travel time for your filters is {} minutes or {} hours or {} days.'.format(tot_travel_min, tot_travel_hr, tot_travel_day))

    # TO DO: display mean travel time
    mean_travel_min = df['Trip Duration'].mean()
    mean_travel_hr = mean_travel_min/60
    print('The mean trip duration for your filters is {} minutes or {} hours'.format(mean_travel_min, mean_travel_hr))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User type counts for your filters are as follows: \n')
    print(user_types)

    # TO DO: Display counts of gender
    if city == 'washington':
        print('Washington does not collect gender data.')

    else:
        user_gender = df['Gender'].value_counts()
        print('User genders for your filters are as follows: \n')
        print(user_gender)


    # TO DO: Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('Washington does not collect birth year data.')

    else:
        user_birth_early = min(df['Birth Year'])
        print('Earliest birth year is: {}'.format(user_birth_early))
        user_birth_recent = max(df['Birth Year'])
        print('Most recent birth year is: {}'.format(user_birth_recent))
        user_birth_early = df['Birth Year'].mode()[0]
        print('Most frequent birth year: {}'.format(user_birth_early))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        view_data = input('\nWould you like to view 5 rows of individual trip data with your filters? Enter yes or no: ').lower()
        start_loc = 0

        while view_data != 'no':
            if (view_data != 'yes'):
                view_data = input('Sorry, I don\'t recognize your answer. Do you wish to see the next five 5 rows of individual trip data with your filters? Enter yes or no: ').lower()

            if (view_data == 'yes'):
                print(df.iloc[start_loc:start_loc+5])
                start_loc += 5
                view_data = input('Do you wish to see the next five 5 rows of individual trip data with your filters? Enter yes or no: ').lower()

        restart = input('Would you like to restart? Enter yes or no: ')

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
