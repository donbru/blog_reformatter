'''
Test BlogEntry class initializer
'''

from  blog_entry import BlogEntry

def test_initializer():
    ''' test of class initializer, make sure data stored and date format is correct'''
    entry = BlogEntry("titleTest", "contentTest", "2010-01-07T22:28:00.007Z")
    assert entry.post_title == "titleTest"
    assert entry.formatted_date == "2010-01-07"
