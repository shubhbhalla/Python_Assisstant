import subprocess
import os
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup


class Commander:
    def __int__(self):
        self.confirm = ["yes", "confirm", "affirmative", "sure", "yeah", "do it"]
        self.cancel = ["cancel", "no", "negative", "don't", "wait"]

    def discover(self, text):
        print("Your command was:")
        print(text)
        if "ip address" in text.lower():
            self.respond("Your IP Address is: ")
            os.system("ipconfig getifaddr en0")

        if ("launch" or "open") in text:
            app = text.split(" ")[-1]
            self.respond("Opening " + app)
            os.system("open -a " + app)

        if "mail" in text:
            val_email = input("Please enter the email of the individual")
            print("Speak the subject of the email")
            val_subject = self.input_voice()
            print("Speak the body of the email")
            val_body = self.input_voice()
            self.respond("Writing mail to " + val_email + " with subject \"" + val_subject +
                         "\" and body -  " + val_body)
            subprocess.call("echo \"" + val_body + "\" | mail -s \"" + val_subject + "\" " +
                            val_email, shell=True)
        if "search" in text.lower():
            self.search_online()

    def respond(self, response):
        print(response)
        subprocess.call("say " + response, shell=True)

    def input_voice(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
        except:
            command = "I am sorry, The speech recognition couldn't understand you"

        return command

    def search_online(self):
        search = input("Type what you want to search: ")
        para = {"q": search}
        r = requests.get("https://www.bing.com/search", para)
        soup = BeautifulSoup(r.text, "html.parser")
        result = soup.find("ol", {"id": "b_results"})
        items = result.findAll("li", {"class": "b_algo"})

        for item in items:
            heading = item.find("a").text
            link = item.find("a").attrs["href"]
            if heading and link:
                print("\n" + heading)
                print(link)

                # You can also use .child and .parent methods
                ''' Gets the next sibling of the item chosen, there is also a previous
                sibling function '''
                children = item.find("h2")
                print("Next sibling of h2 element is:", children.next_sibling)

                # Gets summary of the item
                summary = item.find("p").text
                print("Summary of link is:", summary)
