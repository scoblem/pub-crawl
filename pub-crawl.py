
import os, sys, time, json, glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

BASE_DIR = os.path.join(os.getcwd(), 'ebooks')
DOWNLOADING = os.path.join(BASE_DIR, '*.part')
DOwNLOADED_BOOKS = os.listdir(BASE_DIR)

# set firefox preferences to avoid save dialog and set download directory
FP = webdriver.FirefoxProfile()
FP.set_preference("pdfjs.disabled", True)
FP.set_preference("browser.download.folderList", 2)
FP.set_preference("browser.download.manager.showWhenStarting", False)
FP.set_preference("browser.download.dir", BASE_DIR)
FP.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

URL = "https://www.packtpub.com/packt/offers/free-learning"
BROWSER = webdriver.Firefox(firefox_profile=FP)
BROWSER.get(URL)


# get user and password from json file "credentials.json"
def get_login(user='packt_pub'):
    with open('credentials.json', 'r') as f:
        user_dict = json.load(f)
    return (user_dict[user][0], user_dict[user][1])


# login to packt pub
def login():
    username, passwd = get_login()
    BROWSER.find_element_by_xpath("//*[@id='account-bar-login-register']/a[1]/div").click()
    actions = ActionChains(BROWSER)
    actions.send_keys(username, Keys.TAB, passwd, Keys.ENTER)
    actions.perform()


# claim daily free ebook
def claim_ebook():
    BROWSER.find_element_by_css_selector("div.float-left.free-ebook").click()


# download new ebooks
def download():
    ebooks = BROWSER.find_elements_by_css_selector("div.product-line.unseen")

    for item in ebooks:
        item.click()
        title = item.get_attribute("title")
        book_id = item.get_attribute("nid")
        link = "https://www.packtpub.com/ebook_download/{ID}/pdf".format(ID=book_id)

        if "{TITLE}.pdf".format(TITLE=title) not in DOwNLOADED_BOOKS:
            BROWSER.get(link)
            print("Downloading '{}'".format(title))


# sync ebook to google drive ebooks
def sync():
    pass


# wait for downloads to finsih and close the browser
def shutdown():
    while glob.glob(DOWNLOADING):
        for i in [".", "..", "...",  "   "]:
            time.sleep(1)
            sys.stdout.write("\rDownloading{}".format(i))
            sys.stdout.flush()

    print("\n Job Done!")
    BROWSER.close()


login()
claim_ebook()
download()
shutdown()
