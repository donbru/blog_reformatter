import configparser
import os

class BlogDataProcessorConfig:

    def ReadConfigValues(self):
        config = configparser.ConfigParser()
        config.read('blog_data_processor.config')
        user_profile_path = os.environ["USERPROFILE"] + "/"
        user_profile_path = user_profile_path.replace("\\", "/")
    
        return {
            'local_feed_xml_path' : user_profile_path + config.get('Files', 'local_feed_xml_path'),
            'local_feed_xml_filename' : config.get('Files', 'local_feed_xml_filename'),
            'local_image_path' : user_profile_path + config.get('Files', 'local_image_path'),
            'local_output_path' : user_profile_path + config.get('Files', 'local_output_path'),
            'feed_xml_encoding' : config.get('Input', 'feed_xml_encoding'),
            'feed_xml_root_element_name' : config.get('Input', 'feed_xml_root_element_name'),
            'feed_xml_child_element_name' : config.get('Input', 'feed_xml_child_element_name'),
            'feed_xml_entry_element_name' : config.get('Input', 'feed_xml_entry_element_name'),
        }
    
    def __init__(self):
        self.config_values = self.ReadConfigValues()

    def GetConfigValues(self):
        return self.config_values