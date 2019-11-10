# sqlalchemy-challenge
In this challenge, we were given precipitation and temperature observations in Hawaii across nine weather stations. The data set included daily measurements over a span of 8-9 years.

I used an ORM ([SQLAlchemy](https://www.sqlalchemy.org/)) to automap a SQLite database into Python scripts and query from it. For analysis, I used Pandas, Matplotlib, and the Python datetime library extensively.

1. Starting from the last date available, I queried for one full year of precipitation data and created a line chart.
2. I joined tables via SQLAlchemy to query for the station with the most data and create a bar chart of the most frequent temperature observations at this station.
3. Using a function, I queried for min temperature (tmin), average temperature (tavg) and max temperature (tmax) for a specified date range. Then I plotted a bar chart with average temperature for the date range including an error bar.
4. I also plotted tmin, tavg and tmax in a stacked area line chart to view temperature changes over the same date range in all previous years.
5. In another fuction, I used datetime and a SQLAlchemy query to calculate the temperature stats for June and December in all previous years. Then I used a SciPy Independent T-test to see if the mean temperatures in June and December were statistically significant. To further illustrate their difference, I plotted them in boxplots.

I also created a Flask API using SQLAlchemy so that a user could retrieve JSON data for station info, daily precipitation data, one year of temperature data, and search specific dates for tmin, tavg and tmax. The API would return a 404 error if the date was not in the database. 