# Analyzing the influence of American conversation on Nepali conversation 
## Motivation 
My motivation for pursuing this project is two fold. First, it is common knowledge that westernization is pervasive in Nepal, especially among Nepali youths. It is a topic of interest to see how exactly westernization influences people's behavior. While cultlural westernization mostly influences the youth, I will focus on the influence on all Nepali people because of limitations on filtering tweets by age. Similarly, while the source of westernization is the western world in general, I will focus on the influence of America because it is a big cultural influencer and it also holds some personal connections to me. This leads me to my second motivation -- my personal experiences. I grew up in Nepal, completed high school there and then came to the US for college. While in the States, I couldn't help but notice my friends from back in high school (and other Nepali youths in general) employ techniques of call-out culture to bring forth controversial issues form the past. Since call-out culture started around the US, I immediately attributed this trend as moving from the US to Nepal. I then grew interested in finding out if this movement of conversation manifests itself more generally. This led to my research question on whether American conversation influences Nepali conversation.
## Approach 
I have incorporated three main approaches to analyzing my research question. 
1.  Identify most frequent words in the American dataset and perform time series regression to see how those words compare in frequency to the Nepali dataset. 
2.  Perform time series regression for frequency of American slang usage in America vs in Nepal. 
3.  Do LDA topic modelling on both datasets to get insights into conversation topics in each place. 
## Data collection 
I used Twitter's streaming API to collect timestamped geotagged tweets from the US and Nepal separately. I used a bounding box for each country to do this. Since bounding box also includes tweets from some parts of neighboring countries, I filtered the tweets by the 'country_code' attribute associated with the tweets. 
Geotagged tweets are very sparse, and in my case it was much more sparse for Nepal than for the US. So, I also tracked ~200 keywords to get more tweets from Nepal (these were then filtered by checking against the 'country_code' to ensure the tweets were from Nepal). 
* I tracked tweets from October 26th until Nov 26th for a total of 31 days.  
* On average I had ~1700 tweets from Nepal and ~8000 tweets from the US per day. 
## Results 
This is a work in progress and I will update this README as I move forward. 
## Files 
- `stream.py` is the script that I used for streaming tweets. 
- `nepalTracker.py` is the list of keywords I used to track tweets from Nepal (this is in addition to the geotagged tweets)
- `slangs.py` is the list of American slangs whose usage I analyze in the Nepali and the American dataset. 
- `process.py` is the file where I do all the preprocessing. It contains functions that perform some specialized tasks. 
## Limitations 
* The tweets I have are mostly geotagged tweets and they might not be representative of the whole populations. 
## Project Extension Ideas
* It will be a matter of interest to just focus the analysis on certain demographics like the Nepali youths instead of focusing on the general population. One idea could be to build a machine learning classifier that predicts if a tweet is from a Nepali youth or not. While there are big uncertainties in following this route, it would be intriguing to see this tried. 
