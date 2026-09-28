""" BlogEntry """

from datetime import datetime
from blog_data_processor_config import BlogDataProcessorConfig


class BlogEntry:
    """ BlogEntry object - contains details of a complete blog entry """

    def __init__(self, post_title, content, date_published):
        self.post_title = post_title
        self.content = content
        self.date_published = date_published
        self.previous_post_link = None
        self.next_post_link = None
        self.formatted_date = self.format_date_for_output(date_published)
        self.config_values = BlogDataProcessorConfig().config_values
        self.current_post_link = self.get_output_file_name()

    def format_date_for_output(self, date_published):
        """ Reformat the date to be in YYYY-MM-DD format """
        date_only = date_published[:date_published.find('T')]
        dt = datetime.fromisoformat(date_only)
        return dt.strftime('%Y-%m-%d')

    def get_output_file_name(self):
        """ construct file name to be used to write result HTML file"""
        target_directory = self.config_values['local_output_path']

        sanitized_filename = self.sanitize_file_name_segment(self.post_title)
        full_filename = f"{target_directory}{self.formatted_date} - {sanitized_filename}.html"

        return full_filename

    def sanitize_file_name_segment(self, segment):
        """ replace disallowed Windows file name characters with 
            underscores before writing a file """
        replacements = str.maketrans({"/": "_", ":": "_", "<": "_", ">": "_", \
                                      "\"": "_", "|": "_", "?": "_", "*": "_", })
        return segment.translate(replacements)

    def construct_html_file(self):
        """ TODO improve by by strictly writing tags with element functions on 
        XML classes (iteration 2) """

        #outer HTML - generic HTML with some placeholder text
        outer_html = '<!DOCTYPE html><html><body><h1>placeholder_title</h1>\
            <p>placeholder_content</p><div>placeholder_previous</div><div>\
                placeholder_next</div></body></html>'

        #replace the placeholders with content from original blog markup
        complete_html = outer_html.replace('placeholder_title', self.post_title).\
            replace('placeholder_content', self.content)

        if self.previous_post_link is not None:
            complete_html = complete_html.replace(\
                'placeholder_previous', f"<a href=\"{self.previous_post_link}\">Previous</a>")
        else:
            complete_html = complete_html.replace('placeholder_previous', '')

        if self.next_post_link is not None:
            complete_html = complete_html.replace(\
                'placeholder_next', f"<a href=\"{self.next_post_link}\">Next</a>")
        else:
            complete_html = complete_html.replace('placeholder_next', '')

        #write the HTML file
        with open(self.get_output_file_name(), "w", encoding="utf-8") as f:
            f.write(complete_html)
