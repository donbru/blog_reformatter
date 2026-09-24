import os
from datetime import datetime
from blog_data_processor_config import BlogDataProcessorConfig

class BlogEntry:
    def __init__(self, post_title, content, date_published):
        self.post_title = post_title        
        self.content = content
        self.date_published = date_published
        self.previous_post_link = None
        self.next_post_link = None
        self.formatted_date = self.FormatDateForOutput(date_published)
        self.config_values = BlogDataProcessorConfig().config_values
        self.current_post_link = self.GetOutputFileName()

    def FormatDateForOutput(self, date_published):
        date_only = date_published[:date_published.find('T')]
        dt = datetime.fromisoformat(date_only)
        return dt.strftime('%Y-%m-%d')

    '''
    Get the HTML output file name
    '''
    def GetOutputFileName(self):
        target_directory = self.config_values['local_output_path']

        sanitized_filename = self.SanitizeFileNameSegment(self.post_title)
        full_filename = f"{target_directory}{self.formatted_date} - {sanitized_filename}.html"

        return full_filename
    
    '''
    replace any disallowed Windows file name characters with underscores before writing a file
    '''
    def SanitizeFileNameSegment(self, segment):
        replacements = str.maketrans({"/": "_", ":": "_", "<": "_", ">": "_", "\"": "_", "|": "_", "?": "_", "*": "_", })
        return segment.translate(replacements)

    '''
    TODO improve by by strictly writing tags with element functions on XML classes (iteration 2)
    '''
    def ConstructHtmlFile(self):
        #outer HTML - generic HTML with some placeholder text
        outerHtml = '<!DOCTYPE html><html><body><h1>placeholder_title</h1><p>placeholder_content</p><div>placeholder_previous</div><div>placeholder_next</div></body></html>'

        #replace the placeholders with content from original blog markup
        complete_html = outerHtml.replace('placeholder_title', self.post_title).\
            replace('placeholder_content', self.content)

        if (self.previous_post_link != None):
            complete_html = complete_html.replace('placeholder_previous', f"<a href=\"{self.previous_post_link}\">Previous</a>")
        else:
            complete_html = complete_html.replace('placeholder_previous', '')

        if (self.next_post_link != None):
            complete_html = complete_html.replace('placeholder_next', f"<a href=\"{self.next_post_link}\">Next</a>")
        else:
            complete_html = complete_html.replace('placeholder_next', '')

        #write the HTML file
        with open(self.GetOutputFileName(), "w", encoding="utf-8") as f:
            f.write(complete_html)
                

        
