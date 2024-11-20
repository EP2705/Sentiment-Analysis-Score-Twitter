# # Eliandro Pizzonia
# nov 17 2023
# this file asks the user for the file names of the keyword file and tweet file to
# write call the functions from the sentiment_analysis file to write the final report

# importing the sentiment_analysis file
from sentiment_analysis import *


# asks the user for the file names of the keyword file and tweet file to
# write call the functions from the sentiment_analysis
def main():

    # asking the user for the file names of the keyword file and raising
    # an exception if the file doesn't end with .TSV
    keyword_file_name = input("Input keyword filename (.tsv file): ")
    if not keyword_file_name.endswith(".tsv"):
        raise Exception("Must have tsv file extension")

    # asking the user for the file names of the tweet file and raising
    # an exception if the file doesn't end with .CSV
    tweet_file_name = input("Input tweet filename: ")
    if not tweet_file_name.endswith(".csv"):
        raise Exception("Must have csv file extension")

    # asking the user for the file names of the report file and raising
    # an exception if the file doesn't end with .TXT
    filename_to_report = input("Input filename to output report in (.txt file):")
    if not filename_to_report.endswith(".txt"):
        raise Exception("Must have txt file extension")

    # checking and raising an exception if the read_keywords function is an empty list or dictionary
    if read_keywords(keyword_file_name) == {} or read_keywords(keyword_file_name) == []:
        raise Exception("Tweet list or keyword dictionary is empty!")

    # checking and raising an exception if the read_tweets function is an empty list or dictionary
    elif read_tweets(tweet_file_name) == {} or read_tweets(tweet_file_name) == []:
        raise Exception("Tweet list or keyword dictionary is empty!")

    # calling the functions to output the report
    calling_read_keywords = read_keywords(keyword_file_name)
    calling_read_tweets = read_tweets(tweet_file_name)
    calling_make_report = make_report(calling_read_tweets, calling_read_keywords)
    calling_write_report = write_report(calling_make_report, filename_to_report)

    print(calling_write_report)


main()
