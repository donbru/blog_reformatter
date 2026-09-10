class BlogEntry:
    def __init__(self, post_title, content, date_published):
        self.post_title = post_title        
        self.content = content
        self.date_published = date_published


    # could make this better by strictly writing tags with element functions on 
    # xml classes but not for iteration 1
    def ConstructHtmlFile(self):
        outerHtml = '<!DOCTYPE html><html><body><h1>placeholder_title</h1><p>placeholder_content</p></body></html>'
        completeHtml = outerHtml.replace('placeholder_title', self.post_title).replace('placeholder_content', self.content)

        print(completeHtml)


        
