from web_scraper import WebScraper, Element, ElementSequence, Selector

# Not the biggest fan of the critical=False for this. It is there because of the ensure_absensce in the elementSequence
username_textbox = Element(name="Username textbox", selectors="#Ecom_User_ID", send_values="s4003020", critical=False, timeout=1)
with open("C:\\Users\\sandr\\OneDrive\\Programming\\Selenium\\test.txt", 'r') as f:
    output = f.read()
password_textbox = Element(name="Password textbox", selectors="#Ecom_Password", send_values=output, critical=False, timeout=1)
login_button = Element(name="Login button", selectors="#loginButton2", click=True, critical=False, timeout=1)
absent_login_button = Element(name="Ensure absence login button", selectors="#loginButton2", ensure_absence=True, timeout=1)


sign_in_sequence = ElementSequence(name="Sign In", elements=[username_textbox, password_textbox, login_button, absent_login_button], restart_on_fail=5)


content = Element(
    name="Content",
    selectors=['//*[@id="wiki_page_show"]', '//*[@id="content"]', '/html/body/div[4]/div[2]/div[2]/div[3]/div[1]/div/div[1]', '/html/body/div[4]/div[2]/div[2]/div[3]/div[1]/div'],
    capture_attribute="innerHTML"
)

next_button = Element(
    name="Next button",
    selectors=['//*[@id="sequence_footer"]/div[2]/div/span[2]', '//*[@id="module_navigation_target"]/div/div[2]/div/span[2]/a', '//*[@id="module_navigation_target"]/div/div[2]/div/span/a', '//*[@id="sequence_footer"]/div[2]/div/span[2]/a', '//*[@id="module_navigation_target"]/div/div[2]/div/span[2]', '//*[@id="module_sequence_footer"]/div[2]/div/span[2]', '/html/body/div[4]/div[2]/div[2]/div[3]/div[1]/div/div[2]/div/div[2]/div/span[2]', '/html/body/div[4]/div[2]/div[2]/div[3]/div[1]/div/div[5]/div[2]/div/span[2]'],
    click=True,
    # pageload_wait=5,
    return_on_click=True
)

grab_content_sequence = ElementSequence(name="Grab canvas content", elements=[content, next_button], run_until_fail=True)

def canvas_scraper(name, url):
    scraper = WebScraper(
        name=name,
        url=url,
        sign_in_url="https://rmit.instructure.com/",
        sequences=grab_content_sequence,
        sign_in_sequence=sign_in_sequence
    )
    scraper.run()


canvas_scraper("Algorithms and Analysis", "https://rmit.instructure.com/courses/125079/pages/week-1-overview-read-me-first?module_item_id=5924235")
canvas_scraper("Fullstack Development", "https://rmit.instructure.com/courses/132457/pages/welcome-to-the-course?module_item_id=5888855")
canvas_scraper("Software Engineering Fundamentals", "https://rmit.instructure.com/courses/124890/pages/our-commitment-to-reconciliation?module_item_id=6024511")