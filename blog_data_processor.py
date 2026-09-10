import requests
from bs4 import BeautifulSoup
from blog_entry import BlogEntry
from pprint import pprint

def ProcessBlogArchive(blog_path):
    #print("Processing path " + blog_path)
    
    with open(blog_path, 'r', encoding="UTF-8") as f:
        data = f.read()

    all_entries = []

    bs_data = BeautifulSoup(data, "xml")

    feed_element = bs_data.find('feed')

    entries = feed_element.find_all('entry')
    for entr in entries:
        try:
            content = entr.content.text
            title = entr.title.text
            date_published = entr.published.text
            all_entries.append(BlogEntry(title, content, date_published))
        except: #was except: TypeError, removed to help debugging
            continue

    for en in all_entries:
        en.ConstructHtmlFile()

def main():
 
    ProcessBlogArchive("C:/Users/dbrue/Documents/GitHub/blog_downloader/FullBlogDownload_Sept2026/Takeout/Blogger/Blogs/TheDEBLog/feed.xml")

if __name__ == "__main__":
    main()

