import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent 
import time
import re
import os
import random
import sys
import subprocess
import block_solve
import combine_files

# Need to change as per your requirement - city name
# Match with 99acers site like for chandighars flats data site is : https://www.99acres.com/flats-in-chandigarh-ffid
# Taking value of city as 'Ahmedabad'
City = 'ahmedabad'

# user agent to avoid blocking requests
# headers sey like below :
headers = {
    'User-Agent': UserAgent().random, # generates a random user agent string
    'accept-encoding': 'gzip, deflate, br', # is used to specify the encoding types that the client can understand
    'authority': 'www.99acres.com', # is used to specify the domain name of the server that the client is trying to connect to
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache', # is used to tell the server that the client does not want to use cached data
    'pragma': 'no-cache', # is used to tell the server that the client does not want to use cached data
    'dnt' : '1', # Do Not Track request header, indicating the user's preference not to be tracked
    'referer' : f'https://www.99acres.com/flats-in-{City}-ffid', # is used to specify the URL of the page that linked to the resource being requested
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="123", "Google Chrome";v="123"', # is used to specify the user agent string of the browser making the request
    'sec-ch-ua-mobile': '?0', # is used to specify whether the request is being made from a mobile device or not
    'sec-ch-ua-platform': '"Windows"', # is used to specify the platform on which the browser is running
    'sec-fetch-dest': 'document', # is used to specify the destination of the request
    'sec-fetch-mode': 'navigate', # is used to specify the mode of the request
    'sec-fetch-site': 'same-origin', # is used to specify the origin of the request
    'sec-fetch-user': '?1', # is used to indicate that the request is being made by a user
    'upgrade-insecure-requests': '1' # is used to indicate that the client supports upgrading insecure requests to secure requests
}

# Put start page number and end page number.
# Page number to start extraction data

if os.path.exists("last_page.txt"):
    with open("last_page.txt", "r") as f:
        start = int(f.read())
        print(f"Resuming from page {start}")
else:
    start = int(input("Enter page number where you got error in last run.\nEnter page number to start from:"))

end = 400 # Ending Page

flats = pd.DataFrame()

page_no = start
req = 0
pages_processed = 0
batch_start = start
count = 0

try:
        while page_no < end:
                headers['User-Agent'] = UserAgent().random  # Rotate user-agent for each request
                url = f'https://www.99acres.com/flats-in-{City}-ffid?page={page_no}'
                page = requests.get(url, headers=headers, timeout=20)
                pagesoup = BeautifulSoup(page.content, 'lxml')
                req += 1
                count = 0

                for soup in pagesoup.select_one('div[data-label="SEARCH"]').select('section[data-hydration-on-demand="true"]'):
                        # here it first selects the whole page(search result page) which contains all the container of seperate properties
                        # then after it selects each property container one by one using ('section[data-hydration-on-demand="true"]')
                        try:
                                print(count)
                                p_link = soup.select_one('a', class_="resBuy__propertyHeading")['href']
                                # print(p_link)
                        except Exception as e:
                                # print(name1)
                                continue

                        # price per sqft
                        try:
                                price_per_sqft = ''
                                if (price_per_sqft := soup.find("div", class_="resBuy__area2Type ellipsis")):
                                        price_per_sqft = price_per_sqft.get_text(strip=True)
                        except Exception as e:
                                price_per_sqft = ''

                        # price
                        try:
                                price_tag = soup.select_one('div.configs__ccl2')
                                if price_tag:
                                        price = price_tag.get_text(strip=True)
                                else:
                                        price_tag = soup.select_one('div.resBuy__priceValWrap')
                                if price_tag:
                                        # Extract price after '₹'
                                        price_text = price_tag.get_text(strip=True)
                                        if '₹' in price_text:
                                                price = price_text.split('₹', 1)[1].strip()
                                        else:
                                                price = price_text
                        except Exception as e:
                                price = ''

                        # how many BHK
                        try:
                                BHK = soup.select_one("div", class_="PseudoTupleRevamp__subHeading PseudoTupleRevamp__projectHeading").find("h2").find(string=True, recursive=False)
                        except Exception as e:
                                BHK = ''

                        # property status : resale or new booking
                        try:
                                if (P_status := soup.find("div", class_="PseudoTupleRevamp__ribbon")):
                                        P_status = P_status.find("div").get_text(strip=True)
                                elif (P_status := soup.find("div", class_="resBuy__contentTags")):
                                        P_status = P_status.get_text(strip=True)
                                elif (C_status == 'Under Construction'):
                                        P_status = 'New Booking'
                                else:
                                        P_status = 'not available'
                        except Exception as e:
                                P_status = ''

                        # Description
                        try:
                                description = soup.select_one("#srp_tuple_description").get_text(strip=True)
                        except Exception as e:
                                description = ''

                        page2 = requests.get(p_link, headers=headers, timeout=20)
                        soup2 = BeautifulSoup(page2.content, 'lxml')
                        req += 1
                    
                        # Sleep to avoid hitting the server too hard
                        time.sleep(random.uniform(1, 5))

                        # property Address
                        try:
                                if (address := soup2.find("div", class_="aboutProject___99aboutProjCont body_med")):
                                        address = address.get_text(strip=True).split('\n')[0]
                                else:
                                        if (address := soup.find("span", class_="resBuy__propLocation")):
                                                pass
                                                # address = address.get_text(strip=True).replace('in', '', 1).strip(' ,')
                                        else:
                                                address = soup.find("span", class_="PseudoTupleRevamp__w400Ml4")
                                        address = address.get_text(strip=True).replace('in', '', 1).strip(' ,')
                        except Exception as e:
                                address = ''

                        # extract the property name
                        try:
                                project_name = "n/a"  # Default value in case all attempts fail

                                h1 = soup2.find("h1", class_="title_bold ellipsis")
                                if h1:
                                        project_name = h1.find(string=True, recursive=False).strip()
                                else:
                                        h1 = soup2.select_one('div.banner__projectName')
                                        if h1:
                                                project_name = h1.text.strip()
                                        else:
                                                address_div = soup2.select_one("div.component__details")
                                                if address_div:
                                                        lines = list(address_div.stripped_strings)
                                                        if lines:
                                                                project_name = lines[0]
                                                else:
                                                        # Try resale/flat page structure
                                                        alt_address = soup2.select_one("div.locInfo__sLine.list_header_bold")
                                                        if alt_address:
                                                                project_name = alt_address.find(string=True, recursive=False).strip()
                                                        else:
                                                                alt_address2 = soup2.select_one("div.locInfo__sLine.list_header_bold")
                                                                if alt_address2:
                                                                        project_name = alt_address2.get_text(strip=True)
                                project_name = project_name.split(',')[0]  # Get only the first part before any comma

                        except Exception as e:
                                print("Error extracting project_name:", e)
                                project_name = "n/a"
                        if project_name == "n/a":
                                raise ValueError("Project name could not be extracted (N/A)")
                        elif "Super Built" in project_name or "Carpet area" in project_name:
                                raise ValueError("Project name could not be extracted")

                        # Area with Type :
                        try:
                                super_built = ''
                                carpet = ''
                                if (table := soup2.find("table", class_="pd__tableWrap")):
                                        if (super_built := table.find("tr", id="Super-builtup Area")):
                                                super_built = super_built.find("div", class_="").get_text(strip=True)
                                        else:
                                                super_built = ''
                                        if (carpet := table.find("tr", id="Carpet Area")):
                                                carpet = carpet.find("div", class_="").get_text(strip=True)
                                        else:
                                                carpet = ''
                                        a_type = "Super Built up area " + super_built + " Carpet Area " + carpet
                                elif (type := soup2.find("span", class_="caption_subdued_medium SummaryConfigurationCards__cardAreaTypeStyle false")):
                                        type = type.get_text(strip=True)

                                        area = soup2.select_one('div[class="SummaryConfigurationCards__cardAreaHeading"]')
                                        if area:
                                                area = area.text.strip()
                                        a_type = type + " " + area
                                elif (area := soup2.find("div", class_="card__dropdownWrap")):
                                        area = area.get_text(strip=True)

                                        type = soup2.select_one('div[class="caption_subdued_small undefined"]')
                                        type = type.get_text(strip=True)
                                        a_type = type + " " + area
                                else:
                                        a_type = 'not available'
                        except Exception as e:
                                a_type = ''

                        # Floor Number
                        try:
                                if (div1 := soup2.find_all("div", class_="caption_strong_small_semi")):
                                        for div in div1:
                                                text = div.get_text(strip=True)
                                                if 'floors' in text.lower() or 'floor' in text.lower():
                                                        floor = text
                                                        break
                                elif (tr := soup2.find("table", class_="AboutProjectDetail__specificTable").find_all('tr')):
                                        for div in tr:
                                                text = div.get_text(strip=True)
                                                if 'floors' in text.lower() or 'floor' in text.lower():
                                                        floor = text
                                                        break
                        except Exception as e:
                                floor = ''

                        # Facing
                        try:
                                if (div := soup2.find('tr', id="Facing")):
                                        facing = div.find('div', class_="").get_text(strip=True)
                                else:
                                        facing = ""
                        except Exception as e:
                                facing = ''

                        # Construction Status
                        try:
                                if (div := soup.find("div", class_="resBuy__possessionBy")):
                                        C_status = div.get_text(strip=True)
                                elif (p := soup2.find("span", class_="list_header_semiBold")):
                                        C_status = p.get_text(strip=True)
                                else:
                                        C_status = ''
                        except Exception as e:
                                C_status = ''

                        # Age Possession
                        try:
                                age_possession = ''
                                completion_date = ''
                                if (C_status == 'Ready To Move'):
                                        if (div := soup2.find_all("div", class_="caption_strong_small_semi")):
                                                for line in div:
                                                        text = line.get_text(strip=True)
                                                        if 'year' in text.lower():
                                                                age_possession = text
                                                                break
                                        elif (div := soup2.find("div", class_="SummaryPossessionCard__txtDiv")):
                                                age_possession = div.find("span", class_="caption_subdued_medium").get_text(strip=True)
                                        else:
                                                age_possession = 'not available'
                                else:
                                        if (div := soup2.find("div", class_="SummaryPossessionCard__txtDiv")):
                                                completion_date = div.find("span", class_="caption_subdued_medium").get_text(strip=True)
                                        elif (div := soup2.find_all("div", class_="null", attrs={"data-sstheme": "_BADGE_CHILD"})):
                                                for line in div:
                                                        text = line.get_text(strip=True)
                                                        if 'possession' in text.lower():
                                                                completion_date = text
                                                                break
                                                        elif 'Under Construction' in text.lower():
                                                                completion_date = 'Under Construction'
                                        else:
                                                completion_date = 'not available'
                        except Exception as e:
                                age_possession = ''

                        # RERA id :
                        try:
                                pattern = r'PR/GJ/[A-Z]+/[A-Za-z0-9 ]+/[A-Za-z0-9 ]+/[A-Za-z0-9/]*/[0-9]+'
                                rera_id = 'not available'

                                rera_row = soup2.find("tr", class_="pd__hide", id="RERA")
                                if rera_row:
                                        rera_id = rera_row.find("div", class_="pd__wrap").get_text(strip=True)

                                if (rera_id == 'not available'):
                                        about_div = soup2.find_all("span", class_="ReadMoreLess__hide")
                                        for div in about_div:
                                                text = div.get_text(strip=True)
                                                if (match := re.search(pattern, text)):
                                                        rera_id = match.group()
                                                        break
                                                else:
                                                        rera_id = "not available"

                                if (rera_id == 'not available'):
                                        about_div = soup2.find_all("script", charset="UTF-8")
                                        for div in about_div:
                                                text = div.get_text(strip=True)
                                                if (match := re.search(pattern, text)):
                                                        rera_id = match.group()
                                                        break
                                                else:
                                                        rera_id = "not available"
                        except Exception as e:
                                rera_id = ''

                        # Nearby Landmarks
                        try:
                                nearby_landmarks = []
                                if (landmark := soup2.find_all("div", class_="tags-and-chips__textOnly NearByLocation__gradientWrap pageComponent")):
                                        for line in landmark:
                                                text = line.get_text(strip=True)
                                                if text:
                                                        nearby_landmarks.append(text)
                                elif (landmark := soup2.find_all("div", class_="list_header_semiBold spacer2 ellipsis")):
                                        for line in landmark:
                                                text = line.get_text(strip=True)
                                                if text:
                                                        nearby_landmarks.append(text)
                        except Exception as e:
                                nearby_landmarks = ''

                        # Furnish details
                        try:
                                furnish = []
                                if (div := soup2.find("div", class_="FurnishingSection__FacitiesSlider")):
                                        for line in div.find_all("div", class_="caption_strong_small_semi"):
                                                text = line.get_text(strip=True)
                                                if text:
                                                        furnish.append(text)
                                else:
                                        furnish = 'Unfurnished'
                        except Exception as e:
                                furnish = ''

                        # Features
                        try:
                                features = []
                                if (div := soup2.select_one("#facilities")):
                                        for line in div.find_all("li"):
                                                text = line.get_text(strip=True)
                                                if text:
                                                        features.append(text)
                                        for line in div.find_all("div", class_="amenities__xidFacilitiesCard"):
                                                text = line.get_text(strip=True)
                                                if text:
                                                        features.append(text)
                                elif not features:
                                        div = soup2.find_all("div", class_="UniquesFacilities__xidFacilitiesCard")
                                        for line in div:
                                                text = line.get_text(strip=True)
                                                if text:
                                                        features.append(text)
                                else:
                                        features = 'not available'
                        except Exception as e:
                                features = ''

                        # Ratings
                        try:
                                ratings = []
                                div = soup2.find_all("div", class_="ratingByFeature__contWrap")
                                for line in div:
                                        text = line.get_text(strip=True)
                                        if text:
                                                ratings.append(text)
                        except Exception as e:
                                ratings = ''

                        # Propety Id
                        if 'spid-' in p_link:
                                property_id = p_link.split('spid-')[1]
                        else:
                                property_id = 'not available'

                        # no. of bedrooms, bathrooms, balconies etc.
                        try:
                                bedroom = 0
                                bathroom = 0
                                balcony = 0
                                additionalRoom = ''
                                div = soup2.select_one("#Layout").text.strip().split("Layout")[1]
                                bedroom = div.split(",")[0].strip().split(" ")[0]
                                bathroom = div.split(",")[1].strip().split(" ")[0]
                                additionalRoom = div.split(",")[2:]

                                for script in soup2.find_all('script'):
                                        txt = script.get_text(strip=True)
                                        pattern = r'"balconyNum":( *)"(\d+)"'
                                        match = re.search(pattern, txt)  # "balconyNum": "2"
                                        if match:
                                                balcony = match.group().split(':')[1].replace('"', '')
                                                break
                        except Exception as e:
                                bedroom = ''
                                bathroom = ''
                                balcony = ''
                                additionalRoom = ''

                        # key highlights
                        try:
                                key_highlights = []
                                if (div := soup2.find("div", class_="keyh__keyhWrap")):
                                        for line in div.find_all("span", class_="caption_strong_medium"):
                                                text = line.get_text(strip=True)
                                                if text:
                                                        key_highlights.append(text)
                                else:
                                        key_highlights = ' '
                        except Exception as e:
                                key_highlights = ' '

                        # open space
                        try:
                                open_space = ''
                                units = ''
                                if (div := soup2.find("div", class_="sl__badgesWrap")):
                                        for line in div.find_all("div", class_="null"):
                                                text = line.get_text(strip=True)
                                                if 'open space' in text.lower():
                                                        open_space = text.split(" ")[0].strip()
                                                if 'units' in text.lower():
                                                        units = text.split(" ")[0].strip()
                        except Exception as e:
                                open_space = ''
                                units = ''

                        # create a dictionary with the given variables
                        property_data = {
                                'Project Name': project_name,  # society name
                                'p_link': p_link,  # property link
                                'BHK': BHK,
                                'Price': price,
                                'Price per Sqft': price_per_sqft,
                                'Area with Type': a_type,
                                'Bedrooms': bedroom,
                                'Bathrooms': bathroom,
                                'Balconies': balcony,
                                'Additional Room(s)': additionalRoom if additionalRoom else '',
                                'Floor Number': floor,
                                'Address': address,  # address
                                'Facing': facing,
                                'Construction Status': C_status,  # under construction or ready to move
                                'Age Possession/completion date': age_possession if age_possession else completion_date,
                                'Property Status': P_status,  # for resale or new booking
                                'RERA ID': rera_id,
                                'Property ID': property_id,
                                'Furnish Details': furnish,
                                'Nearby Landmarks': nearby_landmarks,
                                'Features': features,
                                'Key Highlights': key_highlights if key_highlights else '',
                                'Open Space (in %)': open_space if open_space else '',
                                'Units Available': units if units else '',
                                'Description': description,
                                'Ratings': ratings if ratings else ''
                        }

                        temp_df = pd.DataFrame.from_records([property_data])
                        # print(temp_df)
                        flats = pd.concat([flats, temp_df], ignore_index=True)
                        count += 1

                        if req % 4 == 0:
                                time.sleep(random.uniform(5, 15))
                        if req % 15 == 0:
                                time.sleep(random.uniform(15, 40))

                print(f'{page_no} -> {count}')
                page_no += 1
                with open("last_page.txt", "w") as f:
                        f.write(str(page_no))
                pages_processed += 1
            
                # Save after every 5 pages
                if pages_processed % 5 == 0:
                        batch_end = batch_start + 5
                        csv_file_path = f'C:/Users/Data_Gathering/Data/{City}/Flats/flats_{City}_page_{batch_start}_to_{batch_end}.csv'
                        if not flats.empty:
                                if os.path.isfile(csv_file_path):
                                        flats.to_csv(csv_file_path, mode='a', header=False, index=False)
                                else:
                                        flats.to_csv(csv_file_path, mode='a', header=True, index=False)
                                flats = pd.DataFrame()
                        batch_start = batch_end
                     
        # Final save for any remaining data (if total pages is not a multiple of 5)
        if not flats.empty:
                csv_file_path = f'C:/Users/Data_Gathering/Data/{City}/Flats/flats_{City}_page_{batch_start}_to_{page_no}.csv'
                os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
                if os.path.isfile(csv_file_path):
                        flats.to_csv(csv_file_path, mode='a', header=False, index=False)
                else:
                        flats.to_csv(csv_file_path, mode='a', header=True, index=False)

except KeyboardInterrupt:
        print("Interrupted by user, saving progress...")
        csv_file_path = f'C:/Users/Data_Gathering/Data/{City}/Flats/flats_{City}_page_{batch_start}_to_{page_no}_interrupted.csv'
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        if not flats.empty:
                if os.path.isfile(csv_file_path):
                        flats.to_csv(csv_file_path, mode='a', header=False, index=False)
                else:
                        flats.to_csv(csv_file_path, mode='a', header=True, index=False)
        raise
except Exception as e:
        print(e)
        print(f'{page_no} -> {count}')
        print("----------------")
        print("""Your IP might have blocked. Delete Runitme and reconnect again with updating start page number.""")
        
        csv_file_path = f'C:/Users/Data_Gathering/Data/{City}/Flats/flats_{City}_page_{batch_start}_to_{page_no}.csv'
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        # This file will be new every time if start page will chnage, but still taking here mode as append
        if os.path.isfile(csv_file_path):
                # Append DataFrame to the existing file without header
                flats.to_csv(csv_file_path, mode='a', header=False, index=False)
        else:
                # Write DataFrame to the file with header - first time write
                flats.to_csv(csv_file_path, mode='a', header=True, index=False)
       
        print("running block solve")
        block_solve.reset_wifi()

        wait_time = random.randint(60, 180)
        print(f"Waiting for {wait_time // 60} minutes...")
        time.sleep(wait_time)
        
        # Re-run the script from the last successful page
        script_path = os.path.abspath(sys.argv[0])
        print("Restarting script with:", [sys.executable, script_path] + sys.argv[1:])
        subprocess.run([sys.executable, script_path] + sys.argv[1:])
        sys.exit()

# Replace with the actual folder path
folder_path = 'C:/Users/Data_Gathering/Data/Ahmedabad/Flats' 

# Replace with the desired combined file path
combined_file_path = 'C:/Users/Data_Gathering/Data/Ahmedabad/Flats/combined_flats_ahmedabad.csv'

combine_files.combine_csv_files(folder_path, combined_file_path)

