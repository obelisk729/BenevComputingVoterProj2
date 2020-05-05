# RESOURCES:https://sites.google.com/a/chromium.org/chromedriver/getting-started
#           http://jonathansoma.com/lede/foundations/classes/friday%20sessions/advanced-scraping-form-submissions-completed/
#           https://www.codementor.io/blog/python-web-scraping-63l2v9sf2q
#           https://realpython.com/beautiful-soup-web-scraper-python/
# NOTES: This program will make a request to gain access through your firewall. As far as I can tell, this doesn't need
#        to be done, so feel free to just cancel any attempts to open a port through your firewall.

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# This is used by the program to help connect to the API. Would not recommend messing around with if you don't have
# a good reason.
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
# Accessing the credentials through the creds.json file. You can rename the creds file whatever you want, just make
# sure to change the line here as well.
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(credentials)
# IMPORTANT: Here you need to list the title of the spreadsheet you are working with. It needs to be exact and is
# case-sensitive.
sheet = client.open('Copy of EST/ISE 339 - Benevolent Computing - SAMPLE Data Sheet ').sheet1
sheetResult = sheet.get_all_records()
# I'm using this as an easy way to keep track of going through each row in the spreadsheet. We begin on row 3, which
# is the first row where student data is listed. If the program is interrupted for whatever reason and you need to start
# somewhere in the middle, feel free to change the 3 to whatever row you want to start from.
counter = 3
# The website is rather annoying in that even though you are only given county names when choosing from the county
# drop-down menu, what you actually need to submit are numbers associated with them. If more counties are added or
# removed from NY you may need to change this list.
CountyDict = {
    "Albany": "01",
    "Allegany": "02",
    "Bronx": "03",
    "Broome": "04",
    "Cattaraugus": "05",
    "Cayuga": "06",
    "Chautauqua": "07",
    "Chemung": "08",
    "Chenango": "09",
    "Clinton": "10",
    "Columbia": "11",
    "Cortland": "12",
    "Delaware": "13",
    "Dutchess": "14",
    "Erie": "15",
    "Essex": "16",
    "Franklin": "17",
    "Fulton": "18",
    "Genesee": "19",
    "Greene": "20",
    "Hamilton": "21",
    "Herkimer": "22",
    "Jefferson": "23",
    "Kings (Brooklyn)": "24",
    "Lewis": "25",
    "Livingston": "26",
    "Madison": "27",
    "Monroe": "28",
    "Montgomery": "29",
    "Nassau": "30",
    "New York (Manhattan)": "31",
    "Niagara": "32",
    "Oneida": "33",
    "Onondaga": "34",
    "Ontario": "35",
    "Orange": "36",
    "Orleans": "37",
    "Oswego": "38",
    "Otsego": "39",
    "Putnam": "40",
    "Queens": "41",
    "Rensselaer": "42",
    "Richmond (Staten Island)": "43",
    "Rockland": "44",
    "Saratoga": "45",
    "Schenectady": "46",
    "Schoharie": "47",
    "Schuyler": "48",
    "Seneca": "49",
    "St.Lawrence": "50",
    "Steuben": "51",
    "Suffolk": "52",
    "Sullivan": "53",
    "Tioga": "54",
    "Tompkins": "55",
    "Ulster": "56",
    "Warren": "57",
    "Washington": "58",
    "Wayne": "59",
    "Westchester": "60",
    "Wyoming": "61",
    "Yates": "62"
}

# Here we begin the actual process. Since we are iterating through the spreadsheet row by row, we will use a loop that
# ends when it finds a row with an empty cell in column A.
while sheet.cell(counter, 1).value != "":
    # Here, we use Selenium to make a new window, go to the website, and start inputting information.
    driver = webdriver.Chrome()
    url = "https://voterlookup.elections.ny.gov/"
    driver.get(url)
    dropdown = Select(driver.find_element_by_name("SelectedCountyId"))
    # Depending on if the spreadsheet is ever changed, you may need to adjust the x and y values in sheet.cell(x, y).
    # x would be the row and y would be the column. (You almost certainly wouldn't need to adjust the row.)
    dropdown.select_by_value(CountyDict[sheet.cell(counter, 13).value])
    text_input = driver.find_element_by_name("Lastname")
    text_input.send_keys(sheet.cell(counter, 7).value)
    text_input = driver.find_element_by_name("Firstname")
    text_input.send_keys(sheet.cell(counter, 6).value)
    text_input = driver.find_element_by_name("DateOfBirth")
    text_input.send_keys(sheet.cell(counter, 5).value)
    text_input = driver.find_element_by_name("Zipcode")
    text_input.send_keys(sheet.cell(counter, 12).value)
    search_button = driver.find_element_by_id("submitbtn")
    search_button.click()
    driver.page_source
    # By now we should have finished inputting information and will now put everything on the page into a
    # BeautifulSoup document to parse at our leisure.
    doc = BeautifulSoup(driver.page_source, "html.parser")
    strongList = []
    # Here we double check and make sure we've been redirected to a result screen. If not, that probably means
    # no voter has been found and we will move on to another row.
    if driver.current_url == url:
        sheet.update_cell(counter, 18, "Not Found")
        counter += 1
        continue
    # Here we go through the document we've made and find all the data we need and put it into a list.
    for strong_tag in doc.find_all('strong'):
        if strong_tag.text == "Name : " or strong_tag.text == "Address : " or \
                strong_tag.text == "Mailing Address (if any) : " or strong_tag.text == "Political Party : "\
                or strong_tag.text == "Voter Status : " or strong_tag.text == "Election District : "\
                or strong_tag.text == "County Legislative District : " or strong_tag.text == "Senate District : "\
                or strong_tag.text == "Assembly District : " or strong_tag.text == "Congressional District : "\
                or strong_tag.text == "Town : " or strong_tag.text == "Ward : ":
            strongList.append(strong_tag.next_sibling)
            strongList[-1] = strongList[-1].strip()
    # Now we update the sheet.
    sheet.update_cell(counter, 18, "Found")
    sheet.update_cell(counter, 19, strongList[0])
    sheet.update_cell(counter, 20, strongList[1])
    sheet.update_cell(counter, 21, strongList[2])
    sheet.update_cell(counter, 22, strongList[3])
    sheet.update_cell(counter, 23, strongList[4])
    sheet.update_cell(counter, 25, strongList[5])
    sheet.update_cell(counter, 26, strongList[6])
    sheet.update_cell(counter, 27, strongList[7])
    sheet.update_cell(counter, 28, strongList[8])
    sheet.update_cell(counter, 29, strongList[9])
    sheet.update_cell(counter, 30, strongList[10])
    sheet.update_cell(counter, 31, strongList[11])
    # Now we close the window and loop around to the beginning. I could have made it so that the program simply pressed
    # the new search button, but from very brief testing this seems to help a little with load times/not getting banned.
    driver.close()
    counter += 1


