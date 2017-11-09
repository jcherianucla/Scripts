from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import getpass
import re
import urllib
import requests
import shutil
import os

# URL to TestBank
url = "https://upe.seas.ucla.edu/testbank/"
# Selenium Setup
driver = webdriver.Chrome("/Users/jahancherian/Downloads/chromedriver")
driver.get(url)
user = raw_input("Please enter UPE username: ")
# Login information
password = getpass.getpass()
user_field_id, pass_field_id = "id_username", "id_password"

# Selenium log in
user_field_elem = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(user_field_id))
pass_field_elem = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(pass_field_id))
user_field_elem.clear()
user_field_elem.send_keys(user)
pass_field_elem.clear()
pass_field_elem.send_keys(password)
pass_field_elem.send_keys(Keys.RETURN)

# Go to requested link post login
driver.get(url)

html_content = driver.page_source

# Grab all HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Retrieve the tests user wants
tests = raw_input("Please enter all the tests you want, comma delimited: ")
testList = tests.split(",")

# Look within the only table on the site
tables = soup.findChildren('table')
test_table = tables[0]

# Find the table headers and rows
rows = test_table.findChildren(['th', 'tr'])
tests_and_links = []
# Fill up with all class names and their tests
for row in rows:
    row_s = str(row)
    if row_s.find("href") == -1:
        tests_and_links.append(re.sub('<[^>]*>', '', row_s))
    else:
        tests_and_links.append(re.findall(r'(?<=<a href=")[^"]*', row_s)[0])
size = len(tests_and_links)
d_links = []
# Grab the relevant download links based on requested tests
for i in xrange(size):
    if tests_and_links[i] in testList:
        if i < size - 1:
            i += 1
            while tests_and_links[i][:10] == "/testbank/" and i < size: d_links.append("https://upe.seas.ucla.edu" + tests_and_links[i]); i+=1

dir_name = raw_input("Please input the name of the folder you would like to save the files to: ")
# Create the directory to save the file in if it doesn't exist
if not os.path.exists(dir_name): os.makedirs(dir_name)
#for link in d_links:
link = d_links[0]
print("link: %s" % (link))
# Download files
filename = link.rsplit('/', 1)[-1]
fullfilename = os.path.join(dir_name, filename)
if not os.path.isfile(fullfilename):
    r = requests.get(link, auth=(user, password), verify=False,stream=True)
    r.raw.decode_content = True
    with open(fullfilename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    #urllib.urlretrieve(link, fullfilename) 
# Close the web driver opened by Selenium
#driver.quit()

