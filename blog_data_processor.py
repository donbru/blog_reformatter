import requests
from bs4 import BeautifulSoup
from blog_entry import BlogEntry
from pprint import pprint

local_feed_xml_path = "C:/Users/dbrue/Documents/GitHub/blog_reformatter/FullBlogDownload_Sept2026/Takeout/Blogger/Blogs/TheDEBLog"
local_feed_xml_filename = "feed.xml"
local_image_path = "C:/Users/dbrue/Documents/GitHub/blog_reformatter/FullBlogDownload_Sept2026/Takeout/Blogger/Albums/The DEB Log"


'''
Find tags, given the tag name and the attribute containing a possible jpg file reference
Replace the jpg file URI with a local filename and return that value
'''
def FindAndReplaceImageReference(tag, image_tag_attribute_names):
    for attrib_name in image_tag_attribute_names:

        image_reference = tag.get(attrib_name)

        if image_reference.endswith('jpg'):
            #get file name from end, work backwards to find last /
            last_slash_index = image_reference.rfind('/')
            new_file_name = local_image_path + image_reference[last_slash_index:len(image_reference)] 
            return True, image_reference, new_file_name

    # didn't do anything above or we would have returned already    
    return False, '', ''

'''
method comment
'''
def GetEntries(blog_path):
    with open(blog_path, 'r', encoding="UTF-8") as f:
        data = f.read()

    bs_data = BeautifulSoup(data, "xml")
    feed_element = bs_data.find('feed')

    return feed_element.find_all('entry')


'''
Replace certain markup in the original content with content that points to the local file system
rather than Google online storage
'''
def ReplaceImageTags(content):
    ''' 
    images can be found here: 
    C:/Users/dbrue/Documents/GitHub/blog_reformatter/FullBlogDownload_Sept2026/Takeout/Blogger/Albums/The DEB Log
    Replace image names/paths/urls
        with this path and the final image name
     input content <a> tags look like this: 
    <a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhAQXGYT0ioQlTgPx3wpPmiBmiBW57QFXyl-GH_daQ1x0OgXbtMAaO_AOKAEa1soIJ4G6FXMm173hHmqs6mL2gjlbwfDVGMUvadQy5flBCo7DIT-Ow4Zky8YNetnEKQWQ875yn7WUkK_fM/s1600/familyAugust2014.jpg" imageanchor="1" >
    '''

    #find an image name, extract the file name from the end of the href string, then replace
    #that string with the local file path. 
    #Find and following to the end of the double quotes "<a href =/""

    soup = BeautifulSoup(content, features='lxml')

    #if any <a> or <img> tags in the content, replace the hrefs/src of the image files
    relevant_tags = soup.find_all('a') + soup.find_all('img')
    for a_tag in relevant_tags:
        modified, image_reference, new_reference = FindAndReplaceImageReference(a_tag, ['href', 'src'])
        if modified:
            content = content.replace(image_reference, new_reference)

    return content

def ProcessBlogArchive(blog_path):
   
    all_entries = []

    for entr in GetEntries(blog_path)
        try:
            content = entr.content.text
            title = entr.title.text
            date_published = entr.published.text
            reformatted_content = ReplaceImageTags(content)

            all_entries.append(BlogEntry(title, reformatted_content, date_published))
        except: #was except: TypeError, removed to help debugging
            continue

    for en in all_entries:
        en.ConstructHtmlFile()

def main():
 
    ProcessBlogArchive(local_feed_xml_path + "/" + local_feed_xml_filename)

if __name__ == "__main__":
    main()

