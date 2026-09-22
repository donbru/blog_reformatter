import os
from datetime import datetime

class BlogEntry:
    def __init__(self, post_title, content, date_published):
        self.post_title = post_title        
        self.content = content
        self.date_published = date_published,
        self.formatted_date = self.FormatDateForOutput(date_published)

    def FormatDateForOutput(self, date_published):
        date_only = date_published[:date_published.find('T')]
        dt = datetime.fromisoformat(date_only)
        #return dt.year + '-' + dt.month + '-' + dt.day
        return ('{0}-{1}-{2}'.format(dt.year, dt.month, dt.day))

    '''
    Get the HTML output file name
    '''
    def GetOutputFileName(self):
        return  'C:/Users/dbrue/Documents/GitHub/blog_reformatter/blog_reformatter/output/' + \
                    self.formatted_date + \
                    ' - ' + self.SanitizeFileNameSegment(self.post_title) + \
                    '.html'
    
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
        outerHtml = '<!DOCTYPE html><html><body><h1>placeholder_title</h1><p>placeholder_content</p></body></html>'

        #replace the placeholders with content from original blog markup
        complete_html = outerHtml.replace('placeholder_title', self.post_title).replace('placeholder_content', self.content)

        #TODO move this somewhere else, use config values
        if not os.path.exists('C:/Users/dbrue/Documents/GitHub/blog_reformatter/blog_reformatter/output'):
            os.mkdir('C:/Users/dbrue/Documents/GitHub/blog_reformatter/blog_reformatter/output')

        #write the HTML file
        with open(self.GetOutputFileName(), "w", encoding="utf-8") as f:
            f.write(complete_html)
                

        
