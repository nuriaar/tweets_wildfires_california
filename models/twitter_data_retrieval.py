
import twitter_api

n_years = 4
starting_year = 2017

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

for i in range(len(years)):

    start_date = years[i] + "-" + start_month[i] + "-" + start_day + "T00:00:00Z"
    end_date = years[i] + "-" + end_month[i]  + "-" + end_dates[i] + "T00:00:00Z"

    output_name = years[i] + "_" + start_month_name[i] + "_" + end_month_name[i] + ".csv"
    
    responses_list = twitter_api.extract_calfire_tweets(start_date, end_date)
    twitter_api.extract_tweets_info(responses_list, output_name)
    print(i)