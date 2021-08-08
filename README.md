# NBA Project

## V1.0

This project is aimed towards creating a reliable tool to predict the outcome of NBA matches during the regular season.<br>
The end goal of this project is to use a few Machine Learning techiniques to conduct sentiment analysis of Tweets that mention the teams that will play and use this data to feed another Machine Learning model, which will in turn predict the final outcome.<br>
In order to acomplish this goal, a few different kinds of processes and technologies will be applied. They are:
<br>
<br>

### Mining of NBA game results from official sources
Inside the file <code>create_databases.py</code> is a script designed to extract all the results from NBA matches since season 96-97. The code is strongly based on an article written by John Mannelly.
<br>
<br>

### Transformation of mined data
The dataset mined from the NBA website must be prepared before it can be used as a base for the Twitter scraping tool.
<br>
<br>

### Scraping Twitter
Since this is a undergrad student project, no budget is available for the use of Twitter's Full Archive API.<br>
Instead, the tool chosen as a scraper is Twint, which is an open-source Twitter Intelligence Project. <br>
Using Twint, a twitter-scraping-pipeline was built in order to get a set number of tweets from each regular season NBA match played since 2010. 
<br>
<br>

### Sentiment Analysis
<br>
<br>

### Aditional Feature Engineering 
<br>
<br>

### Final Model Creation
<br>
<br>

### Model Deployment
<br>
<br>
