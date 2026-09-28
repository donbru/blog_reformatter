""" Configuration object for the blog markup processor """

import configparser
import os

class BlogDataProcessorConfig:
    """ config object/functionality for blog processor """
    def read_config_values(self):
        """ read config files from the given path/file """
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
        self.config_values = self.read_config_values()

    def get_config_values(self):
        """ simple getter of the stored config values collection """
        return self.config_values
