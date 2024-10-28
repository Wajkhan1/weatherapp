import sys
from http.client import responses
from re import match
from urllib import response

import requests
#from PyQt5.QtCore.QUrl import matches
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from requests import HTTPError, RequestException


class Weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name", self)  #print in window
        self.cityinput = QLineEdit(self)  #allow us to input in gui
        self.getwbutton = QPushButton("Get Weather",self)  #added button to sxecute the command when clicked it will request to api
        self.templabel = QLabel( self)
        self.emojilabel = QLabel( self)
        self.deslabel = QLabel( self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weatherapp")  #add title to window
        vbox = QVBoxLayout()  #arrage everything horizontality with all steps used below
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.cityinput)
        vbox.addWidget(self.getwbutton)
        vbox.addWidget(self.templabel)
        vbox.addWidget(self.emojilabel)
        vbox.addWidget(self.deslabel)
            #centerlay allinged all attributes
        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.cityinput.setAlignment(Qt.AlignCenter)
        self.templabel.setAlignment(Qt.AlignCenter)
        self.emojilabel.setAlignment(Qt.AlignCenter)
        self.deslabel.setAlignment(Qt.AlignCenter)
          # creating objec so we can style the further
        self.city_label.setObjectName("city_label")
        self.cityinput.setObjectName("cityname")
        self.getwbutton.setObjectName("getw")
        self.templabel.setObjectName("templabel")
        self.emojilabel.setObjectName("emoji")
        self.deslabel.setObjectName("des")
       # triple quoates are used for long string so no data lost and more organised
        self.setStyleSheet("""
                      QLabel, QPushButton {
                            font-family: Calibri;
                             }
                      QLabel#city_label {
                          font-size: 40px;  /* Changed to a more reasonable size */
                          font-style: italic;         
                                   }
                      QLineEdit#cityname {
                                 font-size: 40px;  /* Changed to a more reasonable size */
                                }
                      QPushButton#getw {
                                         font-size: 30px;  /* Changed to a more reasonable size */
                                         font-weight: bold;
                                         }
                      QLabel#templabel {
                                    font-size: 75px;  /* Changed to a more reasonable size */
                                    }            
                      QLabel#emoji {
                                     font-size: 100px;  /* Changed to a more reasonable size */
                                     font-family: segoe UI emoji;
                                    }
                      QLabel#des {
                                   font-size: 50px;  /* Changed to a more reasonable size */
                                   }                     
                               """)
        self.getwbutton.clicked.connect(self.getw)
    def getw(self):
        apikey="3365ec3f905158a51c18600dc06d1155"  #access key for api
        city=self.cityinput.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}"
        try:
            response = requests.get(url)
            response.raise_for_status() #this will raise any exceptions
            data = response.json()  # placing data in jso format so you can read easily
            if data["cod"]==200: #cod=200 means data found access code 200
             self.displayw(data)


        except requests.exceptions.HTTPError as http_error:
          match response.status_code:
              case 400:
                  self.displayerror("Bad Request")
              case 401:
                  self.displayerror("Unauthorized")
              case 402:
                  self.displayerror("Forbidden")
              case 403:
                  self.displayerror("Not Authorized")
              case 404:
                self.displayerror("Not Found")
              case 500:
                  self.displayerror("Server Error")
              case 502:
                  self.displayerror("Bad Gateway")
              case 503:
                  self.displayerror("Service Unavailable")
              case 504:
                  self.displayerror("Gateway Timeout")
              case _:
                     self.displayerror(f"HTTP error ocurred: \n{http_error}")
        except requests.exceptions.RequestException as req_error:
            self.displayerror("Request Error:\n:{req_error}")
        except requests.exceptions.ConnectionError:
            self.displayerror("Connection Error\n Check Internet Connection")
        except requests.exceptions.Timeout:
            self.displayerror("Timeout Error\n Request timed out")
        except requests.exceptions.TooManyRedirects:
            self.displayerror("Too Many Redirects\n Check URL")

    def displayerror(self,error):
        self.templabel.setStyleSheet("set font-size: 10px;")  #will set fint style in window to 30
        self.templabel.setText(str(error))                    # will show all the massages recived in window
    def displayw(self,data):
        tempk=data["main"]["temp"]   #accessing api data to store temperature in tempk
        tempc=tempk-273.15          #converting temperature from klvin to degree celcius
        self.templabel.setText(f"{tempc:.1f}°C")
        wid=data["weather"][0]["id"]
        wdis=data["weather"][0]["description"]
        self.emojilabel.setText(self.getwemoji(wid))
        self.deslabel.setText(wdis)

    @staticmethod
    def getwemoji(wid):

        if wid>= 200 and wid <= 300:
            return '⛈️' #thunderstorm
        elif wid>= 300 and wid <= 400:
            return '🌦️'#drizzle
        elif wid>= 400 and wid <= 500:
            return '🌧️'#rain
        elif wid>= 500 and wid <= 600:
             return '🌧️'#rain
        elif wid>= 600 and wid <= 700:
            return '❄️'#snow
        elif wid>= 700 and wid <= 800:
            return '🌫️️'#fog/mist
        elif wid==800:
            return "☀️" #clear sky
        elif wid == 801:
            return "🌤️"  #fewclouds
        elif wid == 802:
            return "☁️"  #cloudy
        elif wid == 803:
            return "☁️"   #cloudy

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wapp = Weatherapp()  # creating an object of class weather app
    wapp.show()  # will show the window
    sys.exit(app.exec_())  #will stop window from exiting until asked for
