
## Project Flowchart

![alt text](https://drive.google.com/open?id=11wEvWtLyW8t2qc8sCsRDir7Tsrb3ILUD)

## Alexa Skill Development

https://developer.amazon.com

Email: demondevil034@gmail.com

password: asr@18fall

## Server

IP: 45.63.10.52  
Domain Name: [https://kksk.biz](https://kksk.biz)  
User & passpword:

```
# DONT SHARE
root s8E,q2!TP*Cb$Zwg
jeff 498079667

# to login via ssh:
# ssh kksk.biz -l jeff
```

Server：nginx. Site conf file location (don't modify)：`/etc/nginx/sites-available/main`  

All request made to `/dogmatcher` will be redirected (via nginx proxy) to localhost:5555 where Flask should be listening on.   

For example: `https://kksk.biz/dogmatcher/abc` will be redirected to `localhost:5555/abc`


API URL (POST): [https://kksk.biz/dogmatcher/](https://kksk.biz/dogmatcher/)

Python Server：flask

To run flask:

```
cd /home/jeff
# created by virutalenv
source dogmatcher/bin/activate
python flask_test.py
```

## Setups

* Install Virtual Env (pip3)
```
pip install virtualenv 
```

* Create your own ENV like
```
virtualenv ENV
```

* Source your ENV
```
source ENV\bin\activate
```

* Install packages by typing
```
pip install -r requirements.txt
```

* Install SQLite3

To be continued...
