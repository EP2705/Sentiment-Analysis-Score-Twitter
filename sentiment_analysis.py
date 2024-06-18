# # Eliandro Pizzonia
# # 251363956
# # epizzoni
# nov 17 2023
# this file uses functions to produce a report that summarizes the sentiment of the tweets contained in the dataset.


# This function reads the TSV keywords file and returns a dictionary with a key for
# each word and value of each score
def read_keywords(keyword_file_name):
    keyword_dict = {}

    # trying to open the file in read mode and read all the lines
    try:
        read_file = open(keyword_file_name, "r")
        read_file_lines = read_file.readlines()

        # splitting the line tab and removing the whitespaces while extracting the word and its value
        for line in read_file_lines:
            part_of_keywords = line.strip().split('\t')
            word = part_of_keywords[0]
            value = int(part_of_keywords[1])
            keyword_dict[word] = value

        # closing and returning the dictionary containing the keywords and their values
        read_file.close()
        return keyword_dict

    # returning an empty dictionary if there is an issue opening the file
    except IOError:
        print("Could not open file {}".format(keyword_file_name))
        return {}


# this function cleans the tweet by making it lowercase and making sure it only contains English letters and spaces
def clean_tweet_text(tweet_text):
    # converts the tweet to lowercase and initializes an empty list to store the updated characters
    text_in_tweet = list(tweet_text.lower())
    list_updated_tweet_text = []

    # checking if each character is a whitespace or english character and updating it to the list
    for char in text_in_tweet:
        if char.isalpha() or char.isspace():
            list_updated_tweet_text.append(char)

    # joining the characters of the updated list to create the cleaned tweet text
    tweet_text = "".join(list_updated_tweet_text)
    return tweet_text


# this function calculates the sentiment score of a tweet based on the text in the tweet
def calc_sentiment(tweet_text, keyword_dict):
    score = 0

    # splitting the tweet text into a list of words
    tweet_text = tweet_text.split()

    # checking if the words are in the keyword dictionary and if it is,
    # it's corresponding value is added to the score
    for word in tweet_text:
        if word in keyword_dict:
            score += keyword_dict[word]

    return score


# this function takes a sentiment score and classifies it as positive,negative, or neutral
def classify(score):
    # returns "positive" if the score is greater than 0
    if score > 0:
        return "positive"

    # returns "negative if the score is less than 0
    elif score < 0:
        return "negative"

    # returns "neutral if the score is equal to 0
    elif score == 0:
        return "neutral"


# this functions reads the CSV tweets file
def read_tweets(tweet_file_name):
    tweet_list = []

    # try to open the tweet file in read mode and read all lines
    try:
        read_file = open(tweet_file_name, "r")
        read_file_lines = read_file.readlines()

        # stripping the whitespaces and splitting the lines by commas
        for lines in read_file_lines:
            part_of_tweet = lines.strip().split(",")

            # dictionary with corresponding information from tweet
            tweet_file_dict = {
                "date": part_of_tweet[0],
                "text": clean_tweet_text(part_of_tweet[1]),
                "user": part_of_tweet[2],
                "retweet": None,
                "favorite": None,
                "lang": part_of_tweet[5],
                "country": part_of_tweet[6],
                "state": part_of_tweet[7],
                "city": part_of_tweet[8],
                "lat": None,
                "lon": None,
            }

            # trying to convert to appropriate data types
            try:
                tweet_file_dict["retweet"] = int(part_of_tweet[3])
                tweet_file_dict["favorite"] = int(part_of_tweet[4])
                tweet_file_dict["lat"] = float(part_of_tweet[9])
                tweet_file_dict["lon"] = float(part_of_tweet[10])
                tweet_list.append(tweet_file_dict)

            # exception if the data type cannot be converted when equal to "NULL"
            except ValueError:
                if part_of_tweet[3] == "NULL":
                    tweet_file_dict["retweet"] = "NULL"
                if part_of_tweet[4] == "NULL":
                    tweet_file_dict["favorite"] = "NULL"
                if part_of_tweet[9] == "NULL":
                    tweet_file_dict["lat"] = "NULL"
                if part_of_tweet[10] == "NULL":
                    tweet_file_dict["lon"] = "NULL"

                # appending the tweet dictionary to the tweet list
                tweet_list.append(tweet_file_dict)

        read_file.close()
        return tweet_list

    # returning an empty list if there is an issue opening the file
    except IOError:
        print("Could not open file {}".format(tweet_file_name))
        return []


# this function takes the tweets list (created by the read_tweets function) and the
# keyword dictionary (created by the read_keywords function) and performs an analysis
def make_report(tweet_list, keyword_dict):
    # initialising variables to store values
    avg_favorite = 0
    avg_retweet = 0
    avg_sentiment = 0
    num_favorite = 0
    num_negative = 0
    num_neutral = 0
    num_positive = 0
    num_retweet = 0
    num_tweets = len(tweet_list)
    top_five = ""
    sentiment_score = 0
    sentiment_score_list = []
    retweet_number_list_score = []
    favorite_number_list_score = []
    country_list = []

    # calculating the sentiment score for the tweet based off of the keyword dictionary
    for tweet in tweet_list:
        sentiment_score = calc_sentiment(tweet["text"], keyword_dict)
        sentiment_score_list.append(sentiment_score)

        # classifying and updating the sentiment values
        if classify(sentiment_score) == "positive":
            num_positive += 1

        elif classify(sentiment_score) == "negative":
            num_negative += 1

        elif classify(sentiment_score) == "neutral":
            num_neutral += 1

        # updating the retweet counters
        if tweet["retweet"] != "NULL" and tweet["retweet"] > 0:
            num_retweet += 1
            retweet_number_list_score.append(sentiment_score)
        else:
            avg_retweet = "NAN"

        # updating the favourite counters
        if tweet["favorite"] != "NULL" and tweet["favorite"] > 0:
            num_favorite += 1
            favorite_number_list_score.append(sentiment_score)
        else:
            avg_favorite = "NAN"

        # dictionary with the country and it's sentiment score
        country_dict = {
            tweet["country"]: sentiment_score,
        }
        country_list.append(country_dict)

    # calculating the average sentiment of each country
    country_total_sentiment = {}
    country_count = {}
    country_average = {}

    for dict in country_list:
        for country, value in dict.items():
            if country == "NULL":
                pass
            elif country not in country_total_sentiment:
                country_total_sentiment[country] = value
                country_count[country] = 1
            else:
                country_total_sentiment[country] += value
                country_count[country] += 1

    for country, total in country_total_sentiment.items():
        average = total / country_count[country]
        country_average[country] = average

    # sorting the top five countries based on highest average sentiment score
    for country in country_average:
        top_five = sorted(country_average, key=country_average.get, reverse=True)

    # calculating the average of favourites, retweets, and average sentiment scores
    avg_favorite = round(sum(favorite_number_list_score) / len(favorite_number_list_score), 2)
    avg_retweet = round(sum(retweet_number_list_score) / len(retweet_number_list_score), 2)
    avg_sentiment = round(sum(sentiment_score_list) / len(sentiment_score_list), 2)

    # returning a dictionary with the updated information
    report = {
        "avg_favorite": avg_favorite,
        "avg_retweet": avg_retweet,
        "avg_sentiment": avg_sentiment,
        "num_favorite": num_favorite,
        "num_negative": num_negative,
        "num_neutral": num_neutral,
        "num_positive": num_positive,
        "num_retweet": num_retweet,
        "num_tweets": num_tweets,
        "top_five": ", ".join(top_five[:5])

    }

    return report


# this function creates the new report file and prints the report dictionary
def write_report(report, output_file):

    # try to open output file in write mode
    try:
        write_file = open(output_file, "w")
        write_file.write("Average sentiment of all tweets: {}".format(float(report["avg_sentiment"])))
        write_file.write("\nTotal number of tweets: {}".format(int(report["num_tweets"])))
        write_file.write("\nNumber of positive tweets: {}".format(int(report["num_positive"])))
        write_file.write("\nNumber of negative tweets: {}".format(int(report["num_negative"])))
        write_file.write("\nNumber of neutral tweets: {}".format(int(report["num_neutral"])))
        write_file.write("\nNumber of favorited tweets: {}".format(int(report["num_favorite"])))
        write_file.write("\nAverage sentiment of favorited tweets: {}".format(float(report["avg_favorite"])))
        write_file.write("\nNumber of retweeted tweets: {}".format(int(report["num_retweet"])))
        write_file.write("\nAverage sentiment of retweeted tweets: {}".format(float(report["avg_retweet"])))
        write_file.write("\nTop five countries by average sentiment: {}".format(report["top_five"]))
        write_file.close()

    # print error message if error opening file
    except IOError:
        print("Could not open file {}".format(output_file))

    # print a message if writing was successful
    else:
        print("Wrote report to {}".format(output_file))
