 #import libraries

import string 
import folium
import pandas as pd
import xlrd 
import json
  
# Give the location of the file 
loc = ("worldcities.xlsx") 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 

sheet.cell_value(0, 0)

Location = []

for line in open('CS_data.json', 'r'):
    Location.append(json.loads(line))

clear_location = []
m = folium.Map(location=[20, 0], tiles="Mapbox Bright", zoom_start=3)

#location = []
for i in range (0, len(Location)):
    if Location[i]['Location'] != None:
        location = Location[i]['Location']
        clear_location = location.split()
        for row_num in range(sheet.nrows):
                row_value = sheet.row_values(row_num)
                if row_value[1] == clear_location[0]:
                        lat = row_value[2]
                        lon = row_value[3]
                        tweet_text = Location[i]['tweet_text']
                        username = Location[i]['user_name']
                        print username
                        folium.Marker([lat, lon], "%s: %s "%(tweet_text,username)).add_to(m)

m.save('map1.html')

