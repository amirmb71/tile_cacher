from flask import Flask
from flask import send_file
from datetime import date
import mysql.connector
import os
import pycurl
import time

#tiles_path = "/home/chista/My-files/Pythhon Practice/miscellaneous/test_image"
DATA_BASE = ""
TABLE =""

### mysql connetions
cnx = mysql.connector.connect(user='root', password='Chista@2020', host='127.0.0.1', database='tile_cache')
cursor = cnx.cursor()
cnx2 = mysql.connector.connect(user='root', password='Chista@2020', host='127.0.0.1', database='tile_cache')
cursor2 = cnx2.cursor()
cnx3 = mysql.connector.connect(user='root', password='Chista@2020', host='127.0.0.1', database='tile_cache')
cursor3 = cnx3.cursor()
cnx4 = mysql.connector.connect(user='root', password='Chista@2020', host='127.0.0.1', database='tile_cache')
cursor4 = cnx4.cursor()


def sql_db(x,y,z):
    #### default names and paths
    name = '{}-{}-{}'.format(x, y, z)

    tiles_path = "/home/tomcat/josm/image/{}".format(z)
    if not os.path.exists(tiles_path ):
        os.mkdir(tiles_path )




    ### check if files exist or not!
    count_querry = ('SELECT COUNT(*) FROM google_tiles where name="{}"'.format(name))
    cursor.execute(count_querry)
    count = cursor.fetchall()
    print(count)
    print("ok")


    if count[0][0] == 0:

        ### Downloading images
        with open('{}/{}-{}-{}.jpg'.format(tiles_path, x, y, z), 'wb') as f:
            tile_cache_tile = "https://mt1.tile_cache.com/vt/lyrs=s@110&hl=pl&x={}&y={}&z={}".format(x, y, z)
            c = pycurl.Curl()
            c.setopt(c.URL, tile_cache_tile)
            c.setopt(c.WRITEDATA, f)
            c.setopt(pycurl.HTTPHEADER, ['User-Agent: JOSM/1.5 (14760 Debian en) Linux Ubuntu 19.04 Java/11.0.5'])
            c.perform()
            f.close()



        ### inserting indexes into database

        if int(c.getinfo(c.RESPONSE_CODE)) == 200:
            req_number = 1
            statuse = 1
            modif_date = date.today()
            resp_time = c.getinfo(c.TOTAL_TIME)
            insert = ('INSERT INTO google_tiles (name, modif_date, req_counter ,resp_time, statuse) VALUES ("{}", "{}" , "{}" , "{}" , "{}" )'.format(name , modif_date , req_number ,resp_time ,statuse))
            cursor2.execute(insert)
            cnx2.commit()


    else:

        ### updating request numbers
        req = ('SELECT req_counter from google_tiles WHERE name = "{}" '.format(name))
        cursor3.execute(req)
        req_number = cursor3.fetchall()
        req_number = req_number[0][0] +1
        update = ('UPDATE google_tiles SET req_counter = "{}" WHERE name = "{}"'.format(req_number , name))
        cursor4.execute(update)
        cnx4.commit()




app = Flask(__name__)

@app.route('/ChistaMap/<string:z>/<string:x>/<string:y>.png')
def post_tile(x, y, z):
    sql_db(x,y,z)
    # tiles_path = "/home/chista/My-files/Pythhon Practice/miscellaneous/test_image/{}".format(z)
    tiles_path = "/home/tomcat/josm/image/{}".format(z)

    img = open('{}/{}-{}-{}.jpg'.format(tiles_path, x, y, z), 'rb')
    return send_file(img, mimetype='image/jpg')
    img.close()



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='1515')
