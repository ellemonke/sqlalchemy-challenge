# sqlalchemy-challenge
In this challenge, we were given precipitation and temperature observations in Hawaii across nine weather stations. The data set included daily measurements over a span of 8-9 years.

I used a [SQLAlchemy ORM](https://www.sqlalchemy.org/) to automap a SQLite database into Python and query from it. For analysis, I used Pandas, Matplotlib, and Python datetime extensively.

1. Starting from the last date available, I queried for one full year of precipitation data and created a line chart.
2. I joined tables to query for the station with the most data and created a bar chart of the most frequent temperature observations.
3. Using a function, I calculated min temperature (tmin), average temperature (tavg) and max temperature (tmax) for a trip date range. Then I plotted a bar chart with average temperature for the date range.
4. I also plotted a stacked area line chart of tmin, tavg and tmax over the same date range in all previous years.
5. Using another fuction, I calculated temperature stats for June and December in all previous years. Then I performed an independent T-test to see if the temperatures in June and December were statistically significant. To further illustrate, I plotted both months' temperatures in boxplots.

I created a [Flask API](https://www.flaskapi.org/) so that a developer could retrieve JSON data for: 
* Station data
* Daily precipitation data
* Temperature data for the latest year
* Temperature min, average and max for a searched date range 
