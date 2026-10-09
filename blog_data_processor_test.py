'''
BlogDataProcessor tests
'''
from  blog_data_processor import BlogDataProcessor

def test_adjust_image_reference():
    ''' 
    test image reference path adjustment
    '''
    bdp = BlogDataProcessor()
    input_href = "https://blogger.googleusercontent.com/img/b/R29vZ/4PsCfY/s1600-h/19720601.jpg"
    expected_output = bdp.config_values['local_image_path'] + '/19720601.jpg'

    assert bdp.adjust_image_reference(input_href) == expected_output
