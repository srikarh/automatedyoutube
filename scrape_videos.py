import datetime
import dateutil.relativedelta
from instalooter.looters import InstaLooter, ProfileLooter
import instaloader
from instalooter.cli.login import login
from itertools import dropwhile, takewhile


# scrape_videos.py scrapes all the videos from pages we are following
def scrapeVideos(username = "",
                 password = "",
                 output_folder = "",
                 days = 1, hours = 0):
        
    print("Starting Scraping")

    L = instaloader.Instaloader(dirname_pattern=output_folder)

    # Login or load session for loader
    L.login(username, password)
    profile = instaloader.Profile.from_username(L.context, username)
    following = profile.get_followees()
    today = datetime.datetime.now()
    yesterday = today - dateutil.relativedelta.relativedelta(days=days, hours=hours)

    for profile in following:
        acc = profile.username
        print("Scraping From Account: " + acc)
        try:
            posts = instaloader.Profile.from_username(L.context, acc).get_posts()
            numDownloaded = 0
            for post in takewhile(lambda p: p.date > yesterday, dropwhile(lambda p: p.date > today, posts)):
                if post.is_video:
                    print(post.date)
                    L.download_post(post, acc)
                    numDownloaded += 1
            print("Downloaded " + str(numDownloaded) + " videos successfully")
            print("")
        except Exception as e:
            print("Skipped acc " + acc + "because of");
            print(e);


if __name__ == "__main__":
    scrapeVideos(username = "scraper2023",
                 password = "Srikar$$2003",
                 output_folder = "test")
