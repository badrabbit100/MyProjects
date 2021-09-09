Description:

This is application to demonstrate how to use Django Channels and websocket to create local game

**Installation:**


#### 1. Download repository and open the main folder
Please download repository and save it. Than follow the project folder

`https://github.com/badrabbit100/public.git`
`cd public/seeab`

#### 2. Start Redis server in docker using next command:
Before startin Docker please install it Docker service

`sudo docker run -p 6379:6379 -d redis:5`

#### 3. Check IP address of your Redis server in seeab.settings.py:
In my case IP address of redis server is 172.17.0.2, Port 6379
Please check IP address of your Redis server and change it if neccessary in seeab.settings.py

`CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('172.17.0.2.', 6379)],
        },
    },
}`

#### 4. Check IP address of your local machine which host application in change it seeab.settings.py:
  
`host = '192.168.0.11:8000'`


#### 5. Create Docker Container 

`sudo docker build -t seeab -f Dockerfile .`


#### 6. Run Docker Container 

Run Docker Container

`sudo docker run -it -p 8000:8000 seeab`


#### 7. Finally

To open it please use the latest version of Google Chrome

App will be located here http://0.0.0.0:8000/ from the host machine

From local machines use $HOST-url from seeab.settings.py (in my case http://192.168.0.11:8000)


**Usage:**

Please don't use that code for production purposes.

This app works using developer server only.

If any question feel free to contact me Telegram:

@TonyFreeSec

Cheers
