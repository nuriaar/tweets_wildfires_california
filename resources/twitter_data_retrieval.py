from resources.twitter_api import extract_calfire_tweets, extract_tweets_info

def retrieve_all_tweets(starting_year, n_years):
    '''
    For a starting year and a number of years, retrieve twitter data and write
    csv files with its date names. 

    Input:
        starting_year (int)
        n_years (int)

    Output:
        Writes CSV files in data/twitter_data/
    '''

    #Create list to make different queries of six-month periods
    start_day = "01"
    end_dates = ["30", "31"]*(n_years*2)
    start_month_name = ["Jan", "July"]*(n_years*2)
    start_month = ["01", "07"]*(n_years*2)

    years = []
    for i in range(n_years):
        year = starting_year + i
        years.append(str(year))
        years.append(str(year))

    end_month_name = ["June", "Dec"]*(n_years*2)
    end_month = ["06", "12"]*(n_years*2)

    #Extract tweets for each period and write csv file
    for i in range(i, len(years)):
        print(i, "out of", len(years))

        start_date = years[i] + "-" + start_month[i] + "-" + start_day + "T00:00:00Z"
        end_date = years[i] + "-" + end_month[i]  + "-" + end_dates[i] + "T00:00:00Z"
        output_name = years[i] + "_" + start_month_name[i] + "_" + end_month_name[i] + ".csv"
        
        responses_list = extract_calfire_tweets(start_date, end_date)
        extract_tweets_info(responses_list, output_name)
        print("completed")


def api_simulation(start_date, end_date):
    '''
    Simulation of API interaction using shorter period of time. Use this 
    function to avoid retrieving too many tweets.

    Inputs:
        Start date: (str) YYYY-MM-DD
        End date: (str) YYYY-MM-DD
    
    Outputs: 
        CSV file in data/twitter_data/
    '''

    tmp_start_date = start_date + "T00:00:00Z"
    tmp_end_date = end_date + "T00:00:00Z"
    output_name = "simulation.csv"

    responses_list = extract_calfire_tweets(tmp_start_date, tmp_end_date)
    extract_tweets_info(responses_list, output_name)
