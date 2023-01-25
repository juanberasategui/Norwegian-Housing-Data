#Import libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date

#Make empty list to store data
boliger = []

#Get the interest rates
page=requests.get("https://www.norges-bank.no/tema/pengepolitikk/Styringsrenten/")
soup = BeautifulSoup(page.content, 'html.parser')
interest_rate = soup.find('p', class_="key-number__nbr")
interest_rate = interest_rate.text

#Loop over all available pages
for x in range(1, 50):
    #Set URL
    URL = "https://www.finn.no/realestate/homes/search.html?is_new_property=false&page="+str(x) +"&published=1&sort=PUBLISHED_DESC"
    #Get page
    page = requests.get(URL)
    #Get the html content of the page
    soup = BeautifulSoup(page.content, 'html.parser')
    #Find all links to the individual properties
    items = soup.find_all('a', class_='link link--dark sf-ad-link sf-realestate-heading')
    #Convert items to list
    items = list(items)
    #Make empty list to store links
    links = []
    #Loop over all links and append to links list
    for item in items:
        links.append(item.get('href'))
    #Get a variable with today's date
    date_today = date.today()

    #GET INTEREST RATE
    page=requests.get("https://www.norges-bank.no/tema/pengepolitikk/Styringsrenten/")
    soup = BeautifulSoup(page.content, 'html.parser')
    interest_rate = soup.find('p', class_="key-number__nbr")
    interest_rate = interest_rate.text
    
    for i in range(0, len(links)):
        page=requests.get(links[i])
        soup = BeautifulSoup(page.content, 'html.parser')
        

        id = soup.find('td', class_="pl-8")
        id = id.text
        

        total_price = soup.find('div', attrs={'data-testid': 'pricing-total-price'})
        if total_price is None:
            total_price = total_price
        else:
            total_price = total_price.text
            total_price = ''.join([i for i in total_price if i.isdigit()])
            total_price = int(total_price)

        charges = soup.find('div', attrs={'data-testid': 'pricing-registration-charge'})
        if charges is None:
            charges = charges
        else:
            charges = charges.text
            charges = ''.join([i for i in charges if i.isdigit()])
            charges = int(charges)

        address = soup.find('span', class_='pl-4')
        address = address.text
        postal_code = address[address.find(',')+1:]
        city = ''.join([i for i in postal_code if not i.isdigit()])
        #make city first letter uppercase
        city = city.title()
        #delete spaces in city
        city = city.replace(" ", "")

        if postal_code == '':
            postal_code = 0
        else:
            #select only the numbers in postal_code
            postal_code = ''.join([i for i in postal_code if i.isdigit()])

        home_address = address[:address.find(',')]
        home_address = home_address.title()
        home_address = home_address.replace(city, '')



        bedrooms = soup.find('div', attrs={'data-testid': 'info-bedrooms'})
        if bedrooms is None:
            bedrooms = bedrooms
        else:
            bedrooms = bedrooms.text
            bedrooms = ''.join([i for i in bedrooms if i.isdigit()])
            bedrooms = int(bedrooms)

        area = soup.find('div', attrs={'data-testid': 'info-primary-area'})
        if area is None:
            area = area
        else:
            area = area.text
            area = ''.join([i for i in area if i.isdigit()])
            area = area[:-1]
            area = int(area)

        type_of_property = soup.find('div', attrs={'data-testid': 'info-property-type'})
        if type_of_property is None:
            type_of_property = type_of_property
        else:
            type_of_property = type_of_property.text
            type_of_property = type_of_property[9:]

        construction_year = soup.find('div', attrs={'data-testid': 'info-construction-year'})
        if construction_year is None:
            construction_year = construction_year
        else:
            construction_year = construction_year.text
            construction_year = construction_year[7:]

        floor = soup.find('div', attrs={'data-testid': 'info-floor'})
        if floor is None:
            floor = floor
        else:
            floor = floor.text
            floor = floor[6:]
        
        bolig = (links[i], id, home_address, city, postal_code, total_price, date_today, charges, area, bedrooms, type_of_property, construction_year, floor)
        boliger.append(bolig)
        print(x)

housing = pd.DataFrame(boliger, columns=['URL', 'ID', 'Address', 'City', 'Postal_code', 'Total_price', 'Date', 'Charges', 'Area', 'Bedrooms', 'Type_of_property', 'Construction_year', 'Floor'])

housing = housing.dropna()

data= pd.read_csv('housing.csv')

data = data.append(housing, ignore_index=True)
data.drop_duplicates(subset=['ID'], keep='first', inplace=True)
data.to_csv('housing.csv', index=False)

