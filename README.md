# A chatbot called Betsy designed for Fresh Feast Restaurant on the basis of RASA(Course Assignment).
The domain name is **Betsy.cf**. Tip: **The chatbot may be delayed or unresponsive because of network speed when you send first message to chatbot. Just try to wait for a few seconds or refresh page. If the website is unable to be accessed, please send one email to ykk1912@gmail.com to let me know.**
# The turtoral of how to use Betsy in the local below is in the Linux Operating System(Ubuntu20.04).
## 1. Make sure you have installed Python3 in your computer
## 2. Create virtual environment in the rasa project cloned
### 1. install python3-venv
``` sudo apt-get install python3-venv ```
### 2. Create one virtual environment
``` python3 -m venv venv ```
### 3. Activate the virtual environment
``` source venv/bin/activate ```
## 3. Install Rasa Open Source
``` sudo pip install rasa ```
### Check the version of rasa
``` rasa --version ```
## 4. Train one model of this Rasa project
``` rasa train ```
### And you will see one new model trained successfully in folder called models.
## 5. Run rasa server and action server
#### 1. In one terminal run command: ``` rasa run --cors --enable-api --port 5005 ```
#### 2. Open another terminal and run command: ``` rasa run actions ```
## 6. Download the fronted webpage project in your local
The project is in another repository of this account called **Betsy-WEB**. Just git clone it.
## 7. Install and Configure Nginx
#### 1. Run the command to install Nginx: ``` sudo apt-get install nginx ```
#### 2. Configure the nginx.conf: ``` sudo vim /etc/nginx/sites-available/default ```
#### 3. Add three locations in the server part:
``` server_name_;
    location / {
             root *********/Betsy-WEB; (The file path of Betsy-WEB downloaded)
             index index.html index.html;
    }
    location /menu {
             alias *********/Betsy-chatbot/images/; (The file path of images in Betsy-chatbot)
             autoindex on;
    }
    location ~ \. (img|text|audio|video)$ {
             alias *********/Betsy-chatbot/images/;
             autoindex on;
    }
```
#### 4. Run the command to check the status of nginx: ``` sudo nginx -t ```
#### 5. Run two commands to restart the nginx service: ``` service nginx restart ```, ``` systemctl restart nginx ```
## 8. Open one browser(Google Chrome, Firefox or Edge) and input the ip: http://127.0.0.1. Now you can use the chatbot in the local.
