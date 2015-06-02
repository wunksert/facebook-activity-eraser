__author__ = 'azim.sonawalla@gmail.com'
from selenium import webdriver
from bs4 import BeautifulSoup
from argparse import ArgumentParser


class Eraser:
    """
    Eraser class to remove Facebook content
    Set this guy up, log in, then repeat:
    - go_to_activity_page()
    - delete_element()
    Don't forget to quit in the end
    """

    def __init__(self, email, password):
        """
        Set up the eraser
        :return: Null
        """
        self.driver = webdriver.Firefox()
        self.email = email
        self.password = password
        self.profile_name = None        # this will end up being the facebook user name

    def quit(self):
        """
        Quit the program (close out the browser)
        :return: Null
        """
        self.driver.quit()

    def login(self):
        """
        Log in to Facebook, set profile name
        :return: Null
        """
        self.driver.get('https://www.facebook.com/login/')
        email_element = self.driver.find_element_by_id('email')
        email_element.send_keys(self.email)
        password_element = self.driver.find_element_by_id('pass')
        password_element.send_keys(self.password)
        password_element.submit()

        soup = BeautifulSoup(self.driver.page_source)
        profile_link = soup.find('a', {'title': 'Profile'})
        self.profile_name = profile_link.get('href')[25:]    # link appears as http://www.facebook.com/PROFILE

    def go_to_activity_page(self):
        """
        Go to the activity page and prepare to start deleting
        :return: Null
        """
        # go to the activity page (filter by 'Your Posts')
        activity_link = 'https://www.facebook.com/' + self.profile_name + '/allactivity?privacy_source=activity_log&log_filter=cluster_11'
        self.driver.get(activity_link)

    def scroll_down(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def delete_element(self):
        """
        Find the first available element and delete it
        :return: Null
        """

        # click hidden from timeline so the delete button shows up
        soup = BeautifulSoup(self.driver.page_source)
        # Priority: highlights, allowed, hidden
        menu_button = soup.find('a', {'aria-label': 'Highlighted on Timeline'})
        if menu_button is None:
            menu_button = soup.find('a', {'aria-label': 'Allowed on Timeline'})
        if menu_button is None:
            menu_button = soup.find('a', {'aria-label': 'Hidden from Timeline'})
        self.driver.find_element_by_id(menu_button.get('id')).click()

        # now that the delete button comes up, find the delete link and click
        self.driver.find_element_by_link_text('Delete').click()

        # click the confirm button
        self.driver.find_element_by_class_name('layerConfirm').click()
        print '[+] Element Deleted'


if __name__ == '__main__':
    """
    Main section of script
    """
    # set up the command line argument parser
    parser = ArgumentParser(description='Delete your Facebook activity.  Requires Firefox')
    parser.add_argument('email', help='Facebook email login')
    parser.add_argument('password', help='Facebook password')
    args = parser.parse_args()

    # execute the script
    eraser = Eraser(email=args.email, password=args.password)
    eraser.login()
    eraser.go_to_activity_page()
    while True:
        try:
            eraser.delete_element()
        except Exception, e:
            print e