# Generalised Web Scraper
A python framework that allows for easy creation and modification of web scrapers. 
This is essentially a wrapper for selenium webdriver interactions, but with genericisation built for iterative extraction of web elements. 
I built this to automate the collation of all the content in a university course.

The [web scraper](WebScraper.py) contains many

[element sequences](ElementSequence.py) which contain many

[elements](Element.py) which contain many 

[selectors](Selector.py)


Features
- Dynamic and reliable capturing of html elements (depending on user's code)
- Easy to edit flags and selectors of Elements
- Capturing of source iframe html
- Multiple selectors per element
- Dynamic delays and handling of element loading times
- Negative elements (make sure an element doesn't exist)
- Pre-defined sequences of element interactions and extractions
- Flag for headless operation
