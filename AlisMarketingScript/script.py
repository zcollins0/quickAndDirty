"""
Kurt Lewis
Reads information like likes, followers, subscribers, and etc from popular social media pages from inputted urls

Written for the specific use case of Ali needed to pull information from companies. This code is fragile, and not intended to be easily modifiable.
If it was, it wouldn't be in the https://github.com/kurtlewis/quickanddirty repo.

"""
import urllib.request
import csv
import re
import time
import os.path
"""
Get's HTML of page for parsing
"""
def getHtml(url, trys=0):
    try:
        return str(urllib.request.urlopen(url).read())
    except:
        print("Error occured while reading " + url)
        if trys < 3:
            print("Trying again")
            return getHtml(url, trys=trys+1)
        else:
            return ""
"""
Searches string using the given compiled regex and str
Returns only the first matching group
"""
def searchStr(regex, string):
    try:
        return regex.search(string).group(1)
    except AttributeError:
        print("Could not find Regex!")
        return "ERROR"


"""
Appends to CSV of data
"""
def writeToCsv(company, outputRow):
    csvFile = company+"Output.csv"
    header = ['Date', 'Twitter Followers', 'Twitter Tweets', 'Facebook Likes', 'Facebook Followers', 'Facebook Posts', 'Instagram Followers', 'Instagram Posts', 'Youtube Subscribers', 'Youtube Videos', 'Pinterest Followers']
    if not os.path.exists(csvFile):
        with open(csvFile, 'w') as output:
            outputWriter = csv.writer(output, delimiter=',', quotechar='"')
            outputWriter.writerow(header)
    
    with open(csvFile, 'a') as output:
        outputWriter = csv.writer(output, delimiter=',', quotechar='"')
        outputWriter.writerow(outputRow)

def main():
    twitterFollowers = re.compile("title=\"([\d,]*) Followers")
    twitterTweets = re.compile("title=\"([\d,]*) Tweets")
    facebookLikes = re.compile(">([\d,]*) people like this<")
    facebookFollowers = re.compile("<div>([\d,]*) people follow this</div>")
    instagramFollowers = re.compile("([\d,.km]*) Followers")
    instagramPosts = re.compile("Following, ([\d,.k]*) Posts")
    youtubeSubscribers = re.compile("=\"([\d,]*) subscribers")
    pinterestFollowers = re.compile("name=\"pinterestapp:followers\" content=\"([\d,]*)\"")
    #pinterestFollowers = re.compile(">([\d,]*)</span> <span class='label '>Followers") # Doesn't work?
    with open('websites.csv', 'r') as csvfile:
        websiteReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(websiteReader) # skip header row
        for row in websiteReader:
            output = list()
            company = row[0]
            print("Now scraping for " + company)
            output.append(time.strftime('%d %b %Y, %H:%M', time.gmtime()))
            for url in row[1:]:
                page = getHtml(url)
                if 'twitter' in url:
                    followers = searchStr(twitterFollowers, page)
                    tweets = searchStr(twitterTweets, page)
                    output.append(followers)
                    output.append(tweets)
                if 'facebook' in url:
                    likes = searchStr(facebookLikes, page)
                    followers = searchStr(facebookFollowers, page)
                    output.append(likes)
                    output.append(followers)
                    output.append("NO DATA") # No data for facebook post numbers
                if 'instagram' in url:
                    followers = searchStr(instagramFollowers, page)
                    posts = searchStr(instagramPosts, page)
                    output.append(followers)
                    output.append(posts)
                if 'youtube' in url:
                    subscribers = searchStr(youtubeSubscribers, page)
                    output.append(subscribers)
                    output.append("NO DATA") # No data for youtube video numbers
                if 'pinterest' in url:
                    followers = searchStr(pinterestFollowers, page)
                    output.append(followers)
            writeToCsv(company, output)


if __name__ == "__main__":
    main()
