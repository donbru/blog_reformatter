import requests
from bs4 import BeautifulSoup
from blog_entry import BlogEntry
from blog_data_processor_config import BlogDataProcessorConfig
from pprint import pprint
import os

class BlogDataProcessor:

    '''
    Read configuration values from config file. These identify the location of the 
    exported blog content and images
    '''
    # def ReadConfigValues(self):
    #     config = configparser.ConfigParser()
    #     config.read('blog_data_processor.config')
    #     user_profile_path = os.environ["USERPROFILE"] + "/"
    #     user_profile_path = user_profile_path.replace("\\", "/")

    #     return {
    #         'local_feed_xml_path' : user_profile_path + config.get('Files', 'local_feed_xml_path'),
    #         'local_feed_xml_filename' : config.get('Files', 'local_feed_xml_filename'),
    #         'local_image_path' : user_profile_path + config.get('Files', 'local_image_path'),
    #         'feed_xml_encoding' : config.get('Input', 'feed_xml_encoding'),
    #         'feed_xml_root_element_name' : config.get('Input', 'feed_xml_root_element_name'),
    #         'feed_xml_child_element_name' : config.get('Input', 'feed_xml_child_element_name'),
    #         'feed_xml_entry_element_name' : config.get('Input', 'feed_xml_entry_element_name'),
    #     }

    def __init__(self):
        self.config_values = BlogDataProcessorConfig().config_values

    '''
    Find tags, given the tag name and the attribute containing a possible jpg file reference
    Replace the jpg file URI with a local filename and return that value
    '''
    def FindAndReplaceImageReference(self, tag, image_tag_attribute_names):
        for attrib_name in image_tag_attribute_names:

            # extract the name of any attributes of the current tag 
            # that match the given attribute name
            image_reference = tag.get(attrib_name)

            if image_reference == None:
                continue

            # if the attribute's value ends with an image type, get its URI
            # and change it to point to a local file instead
            if image_reference.endswith('jpg'):
                #get file name from end, work backwards to find the last /
                last_slash_index = image_reference.rfind('/')
                new_file_name = self.config_values['local_image_path'] + image_reference[last_slash_index:len(image_reference)] 
                return True, image_reference, new_file_name

        # didn't do anything above or we would have returned already    
        return False, '', ''

    '''
    Get all <entry> elements from the input feed.xml file.
    This a fixed format, no need to try to parameterize or make this configurable
    '''
    def GetEntries(self, blog_path):
        with open(blog_path, 'r', 
                  encoding=self.config_values['feed_xml_encoding']) as f:
            data = f.read()

        # extract root and first child elements
        bs_data = BeautifulSoup(data, self.config_values['feed_xml_root_element_name'])
        feed_element = bs_data.find(self.config_values['feed_xml_child_element_name'])

        # this list will contain valid entries once COMMENTs are filtered out
        valid_entries = []

        # return a list of all <entry> elements, exclude any comment entries
        # I wanted to use a parameter to find_all to filter out comments automatically
        # but had trouble figuring out the parameters to do so, and online searches
        # didn't produce much, so I took the simpler route on the collection
        # that find_all returned. There aren't so many blog posts that this approach would
        # be problematic from a performance perspective.
        for entry in feed_element.find_all(self.config_values['feed_xml_entry_element_name']):
            #skip any COMMENT entries, they will not be preserved
            if (entry.find_all('blogger:type')[0].text == 'COMMENT'):
                continue; 
            
            valid_entries.append(entry)

        return valid_entries


    '''
    Replace certain markup in the original content with content that points to the local file system
    rather than Google online storage
    Use paths in the config file to decide where the local image files reside
    '''
    def ReplaceImageTags(self, content):

        # read the XML file into an object using BeautifulSoup
        soup = BeautifulSoup(content, features='lxml')

        #if any <a> or <img> tags in the content, replace the hrefs/src of the image files
        relevant_tags = soup.find_all('a') + soup.find_all('img')

        # pass each found tag into a method to locate image references, if any, and pass back the
        # appropriate local file name
        # sort by published date so they're ordered oldest to newest
        for a_tag in relevant_tags:
            modified, image_reference, new_reference = self.FindAndReplaceImageReference(a_tag, ['href', 'src'])
            if modified:
                content = content.replace(image_reference, new_reference)

        return content

    def ConstructHtmlFiles(self, prepared_entries):
        for en in sorted(prepared_entries, key=lambda e : e.date_published):
            en.ConstructHtmlFile()

    def ProcessBlogArchiveFiles(self, blog_path):
 
        prepared_entries = []

        input_entries = self.GetEntries(blog_path)

        for entr in input_entries:
            # replace any img or a tags with image references to point to local storage
            reformatted_content = self.ReplaceImageTags(entr.content.text)

            # store blog post to be written in the next steps
            prepared_entries.append(BlogEntry(entr.title.text, reformatted_content, entr.published.text))

        #TODO refactor this out of this method
        if not os.path.exists(self.config_values['local_output_path']):
            os.mkdir(self.config_values['local_output_path'])

        self.ConstructHtmlFiles(prepared_entries)

    def ProcessBlogArchive(self):
        self.ProcessBlogArchiveFiles(self.config_values['local_feed_xml_path'] + "/" + self.config_values['local_feed_xml_filename'])



