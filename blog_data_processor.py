import requests
from bs4 import BeautifulSoup
from blog_entry import BlogEntry
from pprint import pprint
import configparser

# local_feed_xml_path = "C:/Users/dbrue/Documents/GitHub/blog_reformatter/FullBlogDownload_Sept2026/Takeout/Blogger/Blogs/TheDEBLog"
# local_feed_xml_filename = "feed.xml"
# local_image_path = "C:/Users/dbrue/Documents/GitHub/blog_reformatter/FullBlogDownload_Sept2026/Takeout/Blogger/Albums/The DEB Log"

# feed_xml_encoding = "UTF-8"
# feed_xml_root_element_name = "xml"
# feed_xml_child_element_name = "feed"
# feed_xml_entry_element_name = "entry"

def ReadConfigValues():
    config = configparser.ConfigParser()
    config.read('blog_data_processor.config')
    return {
        'local_feed_xml_path' : config.get('Files', 'local_feed_xml_path'),
        'local_feed_xml_filename' : config.get('Files', 'local_feed_xml_filename'),
        'local_image_path' : config.get('Files', 'local_image_path'),
        'feed_xml_encoding' : config.get('Input', 'feed_xml_encoding'),
        'feed_xml_root_element_name' : config.get('Input', 'feed_xml_root_element_name'),
        'feed_xml_child_element_name' : config.get('Input', 'feed_xml_child_element_name'),
        'feed_xml_entry_element_name' : config.get('Input', 'feed_xml_entry_element_name'),
    }

config_values = ReadConfigValues()


'''
Find tags, given the tag name and the attribute containing a possible jpg file reference
Replace the jpg file URI with a local filename and return that value
'''
def FindAndReplaceImageReference(tag, image_tag_attribute_names):
    for attrib_name in image_tag_attribute_names:

        # extract the name of any attributes of the current tag 
        # that match the given attribute name
        image_reference = tag.get(attrib_name)

        if image_reference == None:
            continue

        # if the attribute's value ends with an image type, get its URI
        # and change it to point to a local file instead
        if image_reference.endswith('jpg'):
            #get file name from end, work backwards to find last /
            last_slash_index = image_reference.rfind('/')
            new_file_name = config_values['local_image_path'] + image_reference[last_slash_index:len(image_reference)] 
            return True, image_reference, new_file_name

    # didn't do anything above or we would have returned already    
    return False, '', ''

'''
Get all <entry> elements from the input feed.xml file.
This a fixed format, no need to try to parameterize or make this configurable
'''
def GetEntries(blog_path):
    with open(blog_path, 'r', encoding=config_values['feed_xml_encoding']) as f:
        data = f.read()

    # extract root and first child elements
    bs_data = BeautifulSoup(data, config_values['feed_xml_root_element_name'])
    feed_element = bs_data.find(config_values['feed_xml_child_element_name'])

    # return a list of all <entry> elements
    return feed_element.find_all(config_values['feed_xml_entry_element_name'])



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

    # read the XML file into an object using BeautifulSoup
    soup = BeautifulSoup(content, features='lxml')

    #if any <a> or <img> tags in the content, replace the hrefs/src of the image files
    relevant_tags = soup.find_all('a') + soup.find_all('img')

    # pass each found tag into a method to locate image references, if any, and pass back the
    # appropriate local file name
    for a_tag in relevant_tags:
        modified, image_reference, new_reference = FindAndReplaceImageReference(a_tag, ['href', 'src'])
        if modified:
            content = content.replace(image_reference, new_reference)

    return content

def ProcessBlogArchive(blog_path):
   
    prepared_entries = []

    input_entries = GetEntries(blog_path)

    for index, entr in enumerate(input_entries):
        try:
            # ignore comments
            if (entr.find_all('blogger:type')[0].text == 'COMMENT'):
                continue; 

            # replace any img or a tags with image references to point to local storage
            reformatted_content = ReplaceImageTags(entr.content.text)

            # store blog post to be written in the next steps
            prepared_entries.append(BlogEntry(entr.title.text, reformatted_content, entr.published.text))
        except: #was except: TypeError, removed to help debugging
            print("in exception handler, item: " + str(index))
            continue

    for en in prepared_entries:
        en.ConstructHtmlFile()

def main():
    ProcessBlogArchive(config_values['local_feed_xml_path'] + "/" + config_values['local_feed_xml_filename'])

if __name__ == "__main__":
    main()

