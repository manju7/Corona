# Exam:
# Reto Kernen, zks252
# Part 2: Data preprocessing in Python
# Q1:
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def read_data_1(filename):
    '''Return a dictionary (keys: country_names --> str / value: list of tuple(date,new_cases) --> str)'''
    with open(filename) as input_file:
        # Read in the input_file and split the strings
        file = input_file.read().splitlines()
        # Skip header row
        data = file[1:]
        # Create empty dictionary
        dict = {}
        # Iterate over each line in data
        for line in data:
            # Split lines
            lineX = line.split(",")
            # Checks if the corresponding country_name already exists
            if lineX[2] not in dict:
                # If not in dictionary, create new country_name key with list
                dict[lineX[2]] = []
            # Create the tuple
            tuple = (lineX[3],lineX[5])
            # Append the tuple to country_name key list
            dict[lineX[2]].append(tuple)
        return dict

# Q2:
def read_data_2(filename):
    '''Identical to the function above but now only include countries with valid iso-code'''
    with open(filename) as input_file:
        # Read in the input_file and split the strings
        file = input_file.read().splitlines()
        # Skip header row
        data = file[1:]
        # Create empty dictionary
        dict = {}
        # Create regular expression pattern
        pattern = re.compile("^[A-Z]{3},")
        # Iterate over each line in data
        for line in data:
            # Make attempt to match
            match = pattern.match(line)
            # Check if successful
            if match:
                # Split lines
                lineX = line.split(",")
                # Checks if the corresponding country_name already exists
                if lineX[2] not in dict:
                    # If not in dictionary, create new country_name key with list
                    dict[lineX[2]] = []
                # Create the tuple
                tuple = (lineX[3],lineX[5])
                # Append the tuple to country_name key list
                dict[lineX[2]].append(tuple)
        return dict

# Q3:
def read_data_3(filename):
    '''Identical to the function above but now replace the inner-tuples by a dictionary of dictionaries for all columns'''
    with open(filename) as input_file:
        # Read in the input_file and split the strings
        file = input_file.read().splitlines()
        # Create empty dictionary
        dict = {}
        # Define header
        header = file[0]
        # Split header
        headerX = header.split(",")
        # Skip header row
        data = file[1:]
        # Create regular expression pattern
        pattern = re.compile("^[A-Z]{3},")
        # Iterate over each line in data
        for line in data:
            # Make attempt to match
            match = pattern.match(line)
            # Check if successful
            if match:
                # Split lines
                lineX = line.split(",")
                # Create a variable called location
                location = lineX[2]
                # Create a variable called date
                date = lineX[3]
                # Create an inner dictionary
                inner_dict = {}
                # Use enumerate to get current index i
                for i,element in enumerate(lineX):
                    # Create the inner dictionary with all elements
                    inner_dict[headerX[i]] = element
                # Checks if the corresponding country_name already exists
                if location not in dict:
                    # If not in dictionary, create new country_name key
                    dict[location] = {}
                # Create the dictionary with the inner dictionary
                dict[location][date] = inner_dict
        return dict

# Part 3: Analyses 1
# Q1:
def get_weekly_per_100k_for_country_date(dict, location, date):
    '''Return the estimate number of cases per week (float) --> new_cases_smoothed_per_million * 0.7, Exception when called on dates and countries for which no data is available'''
    try:
        # Look up the new_cases_smoothed_per_million
        new_cases_million = dict[location][date]["new_cases_smoothed_per_million"]
        # Calculate new weekly cases per 100'000 inhabitants
        weekly_new_cases_100k = float(new_cases_million) * 0.7
        return weekly_new_cases_100k
    # Create the exception: Exception covers NameError
    except Exception:
        print("No data for " + location + " on the " + date)

# Q2:
def get_weekly_per_100k_for_country(dict, location):
    '''Return two lists: 1. list of dates (datetime), 2. list of weekly-per-100k-values (floats --> 3.1)'''
    # Create empty list of dates
    list_of_dates = []
    # Create empty list of weekly per 100k values
    list_of_weekly_per_100k_values = []
    # Loop over every key in the inner dictionary (date)
    for i in dict[location].keys():
        # Look for the corresponding value (weekly-per-100k)
        value = get_weekly_per_100k_for_country_date(dict, location, i)
        # Add value to the corresponding list
        list_of_weekly_per_100k_values.append(value)
        # Convert the date-string to a datetime object
        date = datetime.datetime.strptime(i, "%Y-%m-%d")
        # Add date to the corresponding list
        list_of_dates.append(date)
    return list_of_dates, list_of_weekly_per_100k_values

# Q3:
def plot_weekly_per_100k_for_country(dict, location):
    '''Call get_weekly_per_100k_for_country function and create a line plot with several features'''
    # Call the function from Q2 for a specific country_name and save it in a variable called data
    data = get_weekly_per_100k_for_country(dict, location)
    # Initialize a dates variable with all the corresponding date values
    dates = data[0]
    # Initialize a values variable with all the corresponding new_cases values
    values = data[1]
    # Create the line plot
    plt.plot(dates, values)
    fig, ax = plt.subplots()
    ax.plot(dates, values)
    # Use MonthLocator
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    # Improve layout of x-axis
    fig.autofmt_xdate()
    # Set title and title-axes
    ax.set_xlabel("time")
    ax.set_ylabel("new weekly cases (per 100k)")
    ax.set_title("Weekly cases per 100k for " + location)
    # Add a horizontal line across the axis
    plt.axhline(y=20, linestyle='dotted')

# Part 4: Analyses 2 - pandas
# Q1:
def read_into_dataframe(filename, countries=None):
    '''Read data into dataframe, only take dataframe lines with correct iso_code, convert date column to be type datetime64 and if countries argument is provided, just filter the corresponding lines '''
    # Read the data into a dataframe
    df = pd.read_csv(filename)
    # Takes only the lines with valid iso-code
    df = df.loc[df["iso_code"].str.len() == 3]
    # Convert date column to be of type datetime64
    df["date"] = df["date"].astype("datetime64")
    # If no countries argument is provided, return full dataframe
    if countries is None:
        return df
    # If countries argument is provided, return dataframe of specific countries
    else:
        specific_countries = df["location"].isin(countries)
        return df[specific_countries]

# Q2:
def get_weekly_per_100k(dataframe):
    '''Return a new dataframe which only contains entries for one day per week (Sundays) as a sum over the entire week'''
    # Set the date column as index of the dataframe
    df = dataframe.set_index("date")
    # Reduce the dataframe to only weekly entries, group them by country_name and calculate the average cases per week
    weekly_cases_df = df.groupby("location").resample('W').mean() * 0.7
    # Corresponding to the calculation above, rename the column to the right measurement
    renamed_df = weekly_cases_df.rename({"new_cases_per_million":"weekly_new_cases_per_100k"}, axis=1)
    # Reset the index
    df = renamed_df.reset_index()
    # Return a dataframe that only consists of the columns location, date and weekly_new_cases_per_100k
    final_df = df.loc[:,["location","date","weekly_new_cases_per_100k"]]
    return final_df

# Q3
def get_weekly_per_100k_country_vs_date(dataframe):
    '''Return the pivoted table (row=country-name, column=weekly_new_cases_per_100k'''
    # Reformate the dataframe with values (new_cases_per_100k), index (country-name) and columns (date)
    pivoting_table = pd.DataFrame.pivot_table(dataframe, values="weekly_new_cases_per_100k", index=["location"], columns=["date"])
    return pivoting_table




