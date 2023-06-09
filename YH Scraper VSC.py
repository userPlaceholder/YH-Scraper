from types import NoneType
from bs4 import BeautifulSoup
import requests
from csv import writer

def main():
    main_lst = scrape_programme_list()
    languages_lst = languages(main_lst)

    print(main_lst)
    print(languages_lst)

    joined_lst = main_lst
    counter = 0

    for item in languages_lst :
        joined_lst[counter].append(item)
        counter += 1

    # Declares the header for each sub-list item:
    header = ["Link", "Title", "Field of study", "Description", "Next opportunity", "Credits & Nominal length", "Stydy pace", "Location", "School", "Languages"]

    # For testing. Makes sure the len of the header list == len of the sub-lists in main list:
    #counter = 0
    #for sub_list in joined_lst:
    #    counter += 1
    #    if len(sub_list) != len(header):
    #        raise Exception(f"The length of sub-list number {counter} does not match the length of the header.")

    # print(joined_lst)

    write_csv(header, joined_lst)


def scrape_programme_list():
    # This URL includes details of all relevant YH programmes
    URL = "https://www.yrkeshogskolan.se/hitta-utbildning/sok/pages/0-3?add=1&area=data&place=2&start=638237664000000000&rate=4&sort=name&query="
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Indicates the relevant section of the URL
    programme_list = soup.find_all("article")

    # Parses the relevant section of the URL to extract and process the data
    lst = []
    prefix = "https://www.yrkeshogskolan.se/hitta-utbildning/sok/utbildning/?id="
    
    for item in programme_list:
        sub_lst = []
        id = ((str(item).splitlines()[1])[-6:-2]) # Exctracts the programme ID
        sub_lst.append(prefix + id) # Creates a link to the programme page
        sub_lst.append(item.find("h1", class_="h-byline").get_text()) # Title
        sub_lst.append(item.find("p", class_="area smaller").get_text().strip()) # Field of study
        sub_lst.append(item.find("p", class_="search-description smaller")) # Description
        # Handles cases with no description:
        if type(sub_lst[3]) != NoneType:
            # print(type((sub_lst[3]))) # Testing functionality
            sub_lst[3] = sub_lst[3].get_text().strip()
        # The following items share the same tag, and include a header
        for sub_item in item.find_all("dl", class_="smaller layout-inline"):
            sub_item = sub_item.get_text().strip()
            sub_item = sub_item.splitlines()[1]
            sub_lst.append(sub_item)
        lst.append(sub_lst)

    return lst

# Checks each program page against a list of programming languages/frameworks.
def languages(lst):

    # lst = lst[0:20] # For testing, limiting number of requests

    languages_lst = []
    counter = 0
    for sub_list in lst:
        counter += 1 # For testing
        URL = sub_list[0]
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        # Indicaes the "about" section on the programme page
        page_content_about = soup.find("div", class_="rte max-height-toggleable")
        result_str = ""
        # Handles cases with no about section:
        if type(page_content_about) != NoneType:
            about_text = page_content_about.get_text()
            if about_text.lower().find("python") != -1:
                result_str += "Python; "
            if about_text.lower().find("c++") != -1:
                result_str += "C++; "
            if about_text.lower().find("javascript") != -1:
                result_str += "JavaScript; "
            if about_text.lower().find("cobol") != -1:
                result_str += "COBOL; "
            if about_text.lower().find("java ") != -1:
                result_str += "Java; "
            if about_text.lower().find("java.") != -1:
                result_str += "Java; "
        languages_lst.append(result_str)
        # print(counter) # For testing

    return languages_lst

def write_csv(header, lst):
    with open("yh_table.csv", "w", encoding="utf-16", newline="" ) as f:
        csv_writer = writer(f)
        csv_writer.writerow(header)
        for sub_lst in lst:
            csv_writer.writerow(sub_lst)

main()

#print(lst)
#print(len(lst))

# -------------------------- OLD -------------------------- #

#for sub_lst in lst:
#    for item in sub_lst:
#        if type(item) != NoneType:
#            if len(item.splitlines()) == 2:
#                #print(item)
#                #print(item.splitlines()[1])
#                item = item.splitlines()[1]
#                print(item)

    #print(sub_lst[4].splitlines()[1])
    #print(sub_lst[5].splitlines()[1])
    #print(sub_lst[6].splitlines()[1])
    #print(sub_lst[7].splitlines()[1])
    #print(sub_lst[8].splitlines()[1])

#for item in lst:
#    for i in item:
#        print(type(i))

#print(lst[-9])
#print(type(lst[-9][2]) == NoneType)


# title = soup.find(id="main-content")
# title = soup.find(id="search-list") #.get_text()

#programme_list = soup.find("a", class_="search-item layout-display-flex")

# print(items)

#    programme_list.find("", class_="")

#for item in programme_list:
#    programme_name = programme_list.find("h1", class_="h-byline")
#    programme_field = programme_list.find("p", class_="area smaller")
#    programme_description = programme_list.find("p", class_="search-description smaller")
#    next_opportunity = programme_list.find("dl", class_="smaller layout-inline")
#    programme_credits = programme_list.find("dl", class_="smaller layout-inline")
#    programme_pace = programme_list.find("dl", class_="smaller layout-inline")
#    programme_location = programme_list.find("dl", class_="smaller layout-inline")
#    school = programme_list.find("dl", class_="smaller layout-inline")
#    info = [programme_name, programme_field, programme_description, next_opportunity, programme_credits, programme_pace, programme_location, school]
#    print(info)