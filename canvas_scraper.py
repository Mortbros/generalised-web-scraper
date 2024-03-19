from web_scraper import WebScraper, Element


user_id = Element(name="User id field", selectors=[], action="click")

AA_scraper = WebScraper(
    name="Algorithms and analysis",
    url="https://rmit.instructure.com/courses/125079/pages/week-1-overview-read-me-first?module_item_id=5924235",
    sign_in_url="https://rmit.instructure.com/",
)

AA_scraper.start()
