import urllib2
import json
import pandas as pd
import csv

#listPos = ['AIzaSyDJARlQLszlHqp6vqNM7MLLItoGlSV2-hM', 'AIzaSyAtiZfGfLXwmtyNTIxTbtPit2RSoDiqm8M', 'AIzaSyBOah437FtOW5HHxDOsFL-m5WD_-RUF-Nk', 'AIzaSyBlvjO-P8tkqqDwrrzMpWpgUP0dh4nIbTA']
listPos = ['AIzaSyCLY2HT3qgE9_PhVUl35FaUkSYWzMVmjM4','AIzaSyBSYyzSRcTP16vB30DUN2_O_kJaQ2oAs94','AIzaSyAVa5jMGnsIrtceEFUa94ImCV9b46php3U','AIzaSyCD_4pFB_BUt4XngIHu1inHRALYiu9N2s0','AIzaSyCW1d1_mQb9j9Q2XzOmLErRvP6spLmg0Vw','AIzaSyBJ_zCryWVex8kux31cckLQru9ZcvXuegQ','AIzaSyB8OGyZL2R4lGjDgwqL6bUdQYql7d2_4qY','AIzaSyAObHihBNcDacNnMbKukQTtQQ1S-ny-e_w']
def waitUntilSucced(listPos, dire, district, options = len(listPos)) :
    if options > 0:
        direc = urllib2.quote(dire+", "+district)
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&region=pe&key=" % direc
        response = urllib2.urlopen(url + listPos[options-1])
        data = json.load(response)
        if data["status"] == "OK":
            return data
        if data["status"] == "ZERO_RESULTS":
            return waitUntilSucced(listPos,cleanDir(dire),distrito)
        else :
            return waitUntilSucced(listPos[:len(listPos)-1],dire, district,options = len(listPos)-1)
    else:
        return None
def cleanDir(direccion):
    direccion = direccion.split(',')
    direccion = direccion[:len(direccion)-1]
    direccion= ' '.join(direccion)
    return direccion

data = pd.read_csv("data_clean.csv")
data['lat'] = 0.0
data["lng"] = 0.0
data = data.drop('index', 1)
data = data.drop('Unnamed: 0', 1)
data.reset_index()
data_test = data[:10]
progress = 0.0
end_progress = len(data_test.index)
filename = "data_lat_lng.csv"
with open(filename, 'a') as file:
    w = csv.writer(file)
    for index, row in data_test.iterrows():
        direction = row["direccion"]
        distrito = row["distrito"]
        response = waitUntilSucced(listPos,direction,distrito)
        print response["results"][0]["geometry"]["location"]["lat"],response["results"][0]["geometry"]["location"]["lng"]
        row['lat'] =response["results"][0]["geometry"]["location"]["lat"]
        row['lng'] = response["results"][0]["geometry"]["location"]["lng"]
        print index, progress/end_progress
        w.writerow(row)
        progress +=1



#response = waitUntilSucced(listPos,direction,distrito)
#print response["results"][0]["geometry"]["location"]["lat"],response["results"][0]["geometry"]["location"]["lng"]
