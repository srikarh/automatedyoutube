import datetime
import dateutil.relativedelta
from instalooter.looters import InstaLooter, ProfileLooter
import instaloader
from itertools import dropwhile, takewhile


# scrape_videos.py scrapes all the videos from pages we are following
def scrapeVideos(username = "",
                 password = "",
                 output_folder = "", MAX_CLIP_LENGTH = 20, MIN_CLIP_LENGTH = 2,
                 days = 1, hours = 0):
        
    print("Starting Scraping")

    L = instaloader.Instaloader(dirname_pattern=output_folder)

    # Login or load session for loader
    L.login(username, password)
    profile = instaloader.Profile.from_username(L.context, username)
    following = profile.get_followees()
    today = datetime.datetime.now()
    yesterday = today - dateutil.relativedelta.relativedelta(days=days, hours=hours)
    tags = []
    for profile in following:
        acc = profile.username
        print("Scraping From Account: " + acc)
        try:
            posts = instaloader.Profile.from_username(L.context, acc).get_posts()
            numDownloaded = 0
            for post in takewhile(lambda p: p.date > yesterday, dropwhile(lambda p: p.date > today, posts)):
                if post.is_video and post.video_duration < MAX_CLIP_LENGTH and post.video_duration > MIN_CLIP_LENGTH:
                    print(post.date)
                    tags += post.caption_hashtags
                    L.download_post(post, acc)
                    numDownloaded += 1
            print("Downloaded " + str(numDownloaded) + " videos successfully")
            print("")
        except Exception as e:
            print("Skipped acc " + acc + "because of");
            print(e);
    return tags

if __name__ == "__main__":
    scrapeVideos(username = "",
                 password = "",
                 output_folder = "test")
