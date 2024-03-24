from web_scraper import WebScraper, Element, ElementSequence, Selector



username_textbox = Element(name="Username textbox", selectors="#Ecom_User_ID", action="send", send_values="s4003020")
with open("C:\\Users\\sandr\\OneDrive\\Programming\\Selenium\\test.txt", 'r') as f:
    output = f.read()
password_textbox = Element(name="Password textbox", selectors="#Ecom_Password", action="send", send_values=output)
login_button = Element(name="Login button", selectors="#loginButton2", action="click")


sign_in_sequence = ElementSequence(elements=[username_textbox, password_textbox, login_button])

AA_scraper = WebScraper(
    name="Algorithms and analysis",
    url="https://rmit.instructure.com/courses/125079/pages/week-1-overview-read-me-first?module_item_id=5924235",
    sign_in_url="https://rmit.instructure.com/",
    sequences=sign_in_sequence,
    sign_in_sequence=sign_in_sequence
)

AA_scraper.sign_in()


# AA_scraper.start()
