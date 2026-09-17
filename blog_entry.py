import os

class BlogEntry:
    def __init__(self, post_title, content, date_published):
        self.post_title = post_title        
        self.content = content
        self.date_published = date_published


    # replace any disallowed Windows file name characters with underscores before writing a file
    def SanitizeFileNameSegment(self, segment):
        replacements = str.maketrans({"/": "_", ":": "_", "<": "_", ">": "_", "\"": "_", "|": "_", "?": "_", "*": "_", })
        return segment.translate(replacements)


    # could make this better by strictly writing tags with element functions on 
    # xml classes but not for iteration 1
    def ConstructHtmlFile(self):
        outerHtml = '<!DOCTYPE html><html><body><h1>placeholder_title</h1><p>placeholder_content</p></body></html>'
        complete_html = outerHtml.replace('placeholder_title', self.post_title).replace('placeholder_content', self.content)

        print(complete_html)

        file_name = 'C:/Users/dbrue/Documents/GitHub/blog_reformatter/blog_reformatter/output/' + \
            self.date_published.replace(':', '') + \
                '_' + self.SanitizeFileNameSegment(self.post_title) + '.html'

        if not os.path.exists('C:/Users/dbrue/Documents/GitHub/blog_reformatter/blog_reformatter/output'):
            os.mkdir('C:/Users/dbrue/Documents/GitHub/blog_reformatter/blog_reformatter/output')

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(complete_html)
                

        
