import time

import PyEnhance.Loading
import requests
import unicodedata
from bs4 import BeautifulSoup
import os
import urllib3
import re
import regex
from PyEnhance import Loading, Timer, Counter, WebTools, Stamps
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.table import Table
import platform
class Main:

    def __init__(self, URL):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.URL = URL

        self.WebHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "en-US,en;q=0.5",
        }

        self.Strings = []

        self.EmailRegex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        self.NameRegex1 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}[a-z]{1,15}$"
        self.NameRegex2 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}[a-z]{1,15}$"
        self.NameRegex3 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}.?\s[A-Z]{1}[a-z]{1,15}$"
        self.NameRegex4 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]\w{1,15}$'
        self.NameRegex5 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]{1}[a-z]{1,' \
                          r'15}\s[A-Z]{1}[a-z]{0,15}$'
        self.NameRegex6 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]{1}[a-z]{1,' \
                          r'15}\s[A-Z]{1}[a-z]{0,15}\s[A-Z]{1}[a-z]{0,15}$'
        self.NameRegex7 = r'(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.{0,1}(\s{0,1}\.{0,1})[A-Z]{1}[a-z]{1,15}\s[A-Z]{0,1}[a-z]{0,15}\s?[A-Z]{0,1}[a-z]{0,15}'




        self.AddressRegex1 = r"^(\d{1,5})\s(\w{1,20})\s?(\w{1,20}){0,}\s(\w{1,10})(\.?)(,?)\s(\w{1,20})\s?(\w{1,20}){0,}(,?)\s(\w{2}?)(,?)\s(\d{1,9})$"
        self.AddressRegex2 = r"^(\d{1,5})\s(\w{1,20})\s?(\w{1,20}){0,}(,?)\s(\w{1,10})(\.?)(,?)\s(\w{1,10}){0,}(\.?)\s(\d{1,10})(,?)\s(\w{1,20})\s?(\w{1,20}){0,}(,?)\s(\w{2}?)(,?)\s(\d{1,9})$"
        self.AddressRegex3 = r"^(P.O.?|PO)\s(Box)\s(\d{1,8})(,?)\s(\w{1,10})(\s?)(\w{1,10}){0,}(,?)\s(\w{2})\s(\d{5,9}-\d{1,9}|\d{5,9})$"
        self.AddressRegex4 = r"^(\d{1,5})\s(\w{1,20})(\.?)(,?)\s(\w{1,20})\s?(\w{1,20}){0,}(,?)\s(\w{2}?)(,?)\s(\d{1,9})$"
        self.AddressesRegex5 = r"^\d{1,5}\s\w{1,20}(?:[A-Za-z0-9. -]+[ ]?)+\w{2,}\.?(?:[,]\s\w{1,20}\s[A-Z]{2}\s\d{5})?$"
        self.AddressesRegex6 = r"^\w{1,10}.\w{1,10}?.\w{1,10}?,.Suite.\d{1,10},.\w{1,20},.\w{2}.\d{1,5}"
        self.AddressesRegex7 = r"^\d{1,5}.\w{1,20}.\w{1,10}.\w{2}\n\w{1,20},.\w{2}.\d{1,5}"
        self.AddressesRegex8 = r"^\d{1,5}.\w{1,2}\W{1}.\w{1,20}.\w{1,20}.\w{1,20}.\w{1,20},.\w{2}.\d{1,5}"
        self.AddressesRegex9 = r"^\d{1,5}.\w{1,2}\W{1}.\w{1,20}.\w{1,20}.\n.\w{1,20}.\w{1,20},.\w{2}.\d{1,5}"
        self.AddressesRegex10 = r"\d{0,5}.\w{0,20}.\w{0,20}\n[A-Z]{1}\w{1,20}..?[A-Z]{0,2}.\d{0,5}"
        self.AddressesRegex11 = r"\d{1,5}.\w{1,20}.[A-Z]{1}[a-z]{1,20}..?[A-Z]{1}[a-z]{1,20}..?[A-Z]{1,2}.\d{1,5}"
        self.AddressesRegex12 = r"\d+[\w\s]+(?:Suite\s\d+|Rt\s\d+|[A-Z])?,?\s[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}(?:\s-\s\d{3,4})?(?:\s\d{3}\s-\s\d{3}\s-\s\d{4})?"
        self.AddressesRegex13 = r"^(\d{1,})\s(-)\s(\d{1,})\s([A-Z][a-z]{1,})\s(\w{1,20})(,)\s([A-Z][a-z]{1,})\s([A-Z]{2})\s(\d{1,9})$"
        self.AddressesRegex14 = r"^(\d{1,})\s([A-Z][a-z]{1,})\s(\w{1,20})\s(-)\s([A-Z][a-z]{1,})\s(\d{1,})(,)\s([A-Z][a-z]{1,})\s([A-Z]{2})\s(\d{1,9})$"
        self.AddressesRegex15 = r"^(\d{1,})\s([A-Z][a-z]{1,})\s(\w{1,2})\s([A-Z][a-z]{1,})\s(\w{1,})(,)\s([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})\s([A-Z]{2})\s(\d{1,})$"
        self.AddressesRegex16 = r"^(\d{1,})\s([A-Z][a-z]{1,})\s(\w{1,})\s(\d{1,})\s(\w{1,2})(,)\s([A-Z][a-z]{1,})\s([A-Z]{2})\s(\d{1,})$"
        self.AddressesRegex17 = r"^(\d{1,}\w{1,})\s([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})(,)\s([A-Z][a-z]{1,})\s([A-Z]{2})\s(\d{1,})"
        self.AddressesRegex18 = r"^(\d{1,}\w{1,})\s([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})(,)\s([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})\s([A-Z]{2})\s(\d{1,})"
        self.AddressesRegex19 = r"^(\d{1,})\s(\d{1,}\w{1,})\s(\w{1,})\s(\w{1,})(,)\s([A-Z][a-z]{1,})\s([A-Z]{2})\s(\d{1,})\s(\s?)(\d{1,})\s-\s(\d{1,})\s(-)\s(\d{1,})"
        self.AddressesRegex20 = r"^(\d{1,})\s(\w{1,})\s(\d{1,})\s(-)\s(\d{1,})\s(\w{1,2})(,)\s([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})\s([A-Z]{2})\s(\d{1,})"
        self.AddressesRegex21 = r"^([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})(,)\s([A-Z][a-z]{1,})(,)\s([A-Z]{2})\s(\d{1,})(,)\s(\w{1,})$"
        self.AddressesRegex22 = r"^([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})(,)\s([A-Z][a-z]{1,})(,)\s([A-Z]{2})\s(\d{1,})"
        self.AddressesRegex23 = r"^([A-Z][a-z]{1,})\s(\d{1,}\w{1,})\s(\w{1,})(,)\s([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})(,)\s([A-Z]{2})\s(\d{1,})(,)\s([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})"
        self.AddressesRegex24 = r"^(\w{1,})\s([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})\s(\w{1,2})(,)\s([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})(,)\s([A-Z]{2})\s(\d{1,})(,)\s(\w{1,})"
        self.AddressesRegex25 = r"^(\w{1,})\s([A-Z][a-z]{1,})\s(\w{1,})(,)\s([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})(,)\s([A-Z]{2})\s(\d{1,})(,)\s(\w{1,})"
        self.AddressesRegex26 = r"^(\w{1,})\s(\w{1,})\s(\d{1,}\w{1,})\s(\w{1,})(,)\s([A-Z][a-z]{1,})\s([A-Z][a-z]{1,})(,)\s([A-Z]{1,})\s(\d{1,})(,)\s(\w{1,})"
        self.AddressesRegex27 = r"^(\w{1,})\s(\w{1,})\s(\w{0,})\s(\w{0,}),\s([A-Z]\w{1,}),\s([A-Z]{2})\s(\d{5,})$"

        self.PhoneNumberRegex1 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
        self.PhoneNumberRegex2 = r"^\+?1?-\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
        self.PhoneNumberRegex3 = r"\+?1?\s?\(?\d{3}\)?\s]?\d{3}\s]?\d{4}$"
        self.PhoneNumberRegex4 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}.$"
        self.PhoneNumberRegex5 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
        self.PhoneNumberRegex6 = r"^([+]?\d?)([(]?)([+]?\d?)([–]?)( ?)(\d{3})([–]?)( ?)(\d{3})([–]?)( ?)(\d{4})([)]?)$"
        self.PhoneNumberRegex7 = r"^([(]?)(\d{3})([)]?)\s(\d{3})(–|-?)(\d{4})$"
        self.PhoneNumberRegex8 = r"^\d{10}"

        self.StreetEndingsLong = [
            "Avenue", "Boulevard", "Drive", "Lane",
            "Place", "Road", "Street", "Way",
            "Circle", "Court", "Crescent", "Expressway",
            "Freeway", "Parkway", "Square"
        ]

        self.StreetEndingsShort = [
            "Ave.", "Blvd.", "Dr.", "Ln.",
            "Pl.", "Rd.", "St.", "Wy.",
            "Cir.", "Ct.", "Cres.", "Expy.",
            "Fwy.", "Pkwy.", "Sq.", ]

        self.Tags = [
            "a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi",
            "bdo", "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code",
            "col", "colgroup", "command", "datalist", "dd", "del", "details", "dfn", "dialog",
            "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "footer",
            "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "html",
            "i", "iframe", "img", "input", "ins", "kbd", "label", "legend", "li", "link",
            "main", "map", "mark", "menu", "meta", "meter", "nav", "noscript", "object",
            "ol", "optgroup", "option", "output", "p", "param", "picture", "pre", "progress",
            "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "slot", "small", "source",
            "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "textarea",
            "tfoot", "th", "thead", "time", "title", "tr", "track", "u", "ul", "var", "video",
            "wbr"
        ]

        self.PhoneNumberRegexList = [self.PhoneNumberRegex1, self.PhoneNumberRegex2, self.PhoneNumberRegex3,
                                     self.PhoneNumberRegex4, self.PhoneNumberRegex5, self.PhoneNumberRegex6,
                                     self.PhoneNumberRegex7, self.PhoneNumberRegex8]

        self.NameRegexList = [self.NameRegex1, self.NameRegex2, self.NameRegex3,
                              self.NameRegex4, self.NameRegex5, self.NameRegex6, self.NameRegex7]

        self.AddressRegexList = [self.AddressRegex1, self.AddressRegex2, self.AddressRegex3, self.AddressRegex4,
                                 self.AddressesRegex5,
                                 self.AddressesRegex6,
                                 self.AddressesRegex7, self.AddressesRegex8, self.AddressesRegex9,
                                 self.AddressesRegex10,
                                 self.AddressesRegex11,
                                 self.AddressesRegex12, self.AddressesRegex13, self.AddressesRegex14,
                                 self.AddressesRegex15,
                                 self.AddressesRegex16,
                                 self.AddressesRegex17, self.AddressesRegex18, self.AddressesRegex19,
                                 self.AddressesRegex20,
                                 self.AddressesRegex21,
                                 self.AddressesRegex22, self.AddressesRegex23, self.AddressesRegex24,
                                 self.AddressesRegex25, self.AddressesRegex26, self.AddressesRegex27]

        self.Replace = [" ", "'", ",", "[", "]", "(", ")", "-", ".", "+"]


        self.ClearScreenCommand = None

        if platform.system() == "Windows":
            self.UserOS = "Windows"
            self.ClearScreenCommand = "cls"
        elif platform.system() == "Linux":
            self.UserOS = "Linux"
            self.ClearScreenCommand = "clear"
        elif platform.system() == "Darwin":
            self.UserOS = "MacOS"
            self.ClearScreenCommand = "clear"
        else:
            self.UserOS = "Unknown"
            self.ClearScreenCommand = None

        os.system(self.ClearScreenCommand)


        self.GetHtml()

    def GetHtml(self):
        Response = requests.get(f"{self.URL}", headers=self.WebHeaders, verify=False, )

        self.HtmlContent = Response.text

        self.Soup = BeautifulSoup(self.HtmlContent, 'html.parser')

        AllTags = self.Soup.descendants

        for Tag in AllTags:
            for String in Tag.stripped_strings:
                if String not in self.Strings:
                    self.Strings.append(String)

        self.Filter()

    def MatchNamesAPICalls(self, Name):

        for Regex in self.NameRegexList:

            if Name in self.NamesList:
                continue

            SubStrings = Name.split(" ")

            InDict = []
            NotInDict = []

            if re.fullmatch(Regex, Name):
                for SubString in SubStrings:


                    if requests.get(f"https://www.dictionary.com/browse/{SubString}").status_code == 200:
                        InDict.append(SubString)
                        continue

                    if requests.get(
                            f"https://www.dictionary.com/browse/{SubString}").status_code == 200 and SubString in self.NamesFromFile:
                        NotInDict.append(SubString)
                        continue

                    if requests.get(f"https://www.dictionary.com/browse/{SubString}").status_code == 404:
                        NotInDict.append(SubString)
                        continue


            if not len(NotInDict) == 0:
                if Name not in self.NamesList:
                        self.NamesList.append(Name)

    def Filter(self):

        self.EmailsList = []
        self.PhoneNumbersList = []
        self.AddressesList = []
        self.NamesList = []


    #|=|=| EMAIL MATCH CODE START |=|=|#
        self.EmailLoading = PyEnhance.Loading.Loading()

        self.EmailLoading.Spin(Text="Getting Emails")

        for String in self.Strings:
            if re.search(self.EmailRegex, String):
                if String not in self.EmailsList:
                    self.EmailsList.append(String)

    #|=|=| EMAIL MATCH CODE END |=|=|#



    #|=|=| PHONE NUMBER MATCH CODE START |=|=|#

        self.EmailLoading.Stop()
        os.system(self.ClearScreenCommand)
        self.PhoneNumberLoading = PyEnhance.Loading.Loading()
        self.PhoneNumberLoading.Spin("Getting Phone Numbers")

        for String in self.Strings:
            for Regex in self.PhoneNumberRegexList:
                if re.search(Regex, String):
                    if String not in self.PhoneNumbersList:
                        self.PhoneNumbersList.append(String)

    #|=|=| PHONE NUMBER MATCH CODE END |=|=|#



    #|=|=| ADDRESS MATCH CODE START |=|=|#

        self.PhoneNumberLoading.Stop()
        os.system(self.ClearScreenCommand)
        self.AddressLoading = PyEnhance.Loading.Loading()
        self.AddressLoading.Spin("Getting Addresses")
        for String in self.Strings:
            for Regex in self.AddressRegexList:

                if String in self.AddressesList:
                    continue
                else:
                    if regex.fullmatch(Regex, String):
                        if String not in self.AddressesList:
                            self.AddressesList.append(String)

        for Index, String in enumerate(self.Strings):
            for Regex in self.AddressRegexList:
                try:
                    NewString = f"{String}, {self.Strings[Index+1]}"

                    if NewString in self.AddressesList:
                        continue
                    else:
                        if regex.fullmatch(Regex, NewString, timeout=1):
                            if NewString not in self.AddressesList:
                                self.AddressesList.append(NewString)
                        else:
                            continue
                except TimeoutError as e:
                    print(e)
                    continue
                except:
                    continue

        for String in self.AddressesList:

            try:
                if String.split(',')[0] in self.AddressesList:
                    self.AddressesList.remove(String.split(',')[0])
                else:
                    continue
            except:
                continue

    #|=|=| ADDRESS MATCH CODE END |=|=|#

        # ||| Start of code I will add to PyEnhance |||

        self.NamesFromFile = []
        self.CommonWordsFromFile = []

        with open('Names.txt', 'r') as f:

            for Name in f:
                self.NamesFromFile.append(Name.replace('\n', ''))


        with open('CommonWords.txt', 'r') as f:

            for Word in f:
                self.CommonWordsFromFile.append(Word.replace('\n', ''))


        # ||| End of code I will add to PyEnhance |||

    #|=|=| NAME MATCH CODE START |=|=|#

        self.AddressLoading.Stop()
        os.system(self.ClearScreenCommand)
        self.NameLoading = PyEnhance.Loading.Loading()
        self.NameLoading.Spin("Getting Names")

        StringsForNames = [unicodedata.normalize("NFKD", i) for i in self.Strings]
        StringsForNames = list(dict.fromkeys(StringsForNames))


        with ThreadPoolExecutor(max_workers=10) as executor:
            list(executor.map(self.MatchNamesAPICalls, StringsForNames)) # Calls function above Filter function


        self.NamesListFiltered = []

        for Name in self.NamesList:

            SubNames = str(Name).split(' ')

            for Sub in SubNames:
                if Sub.lower() in self.CommonWordsFromFile and Sub not in self.NamesFromFile:
                    SubNames.remove(Sub)

            if len(SubNames) > 1:
                self.NamesListFiltered.append(Name)

        self.NameLoading.Stop()

        #|=|=| NAME MATCH CODE END |=|=|#



    #|=|=| OUTPUT CODE START |=|=|#

        #print(f"Emails: {' | '.join([Email for Email in self.EmailsList])}")
        #print(f"Phone Numbers: {' | '.join([PhoneNumber for PhoneNumber in self.PhoneNumbersList])}")
        #print(f"Addresses: {' | '.join([Address for Address in self.AddressesList])}")
        #print(f"Names: {' | '.join([Name for Name in self.NamesListFiltered])}")


        LongestList = max(self.EmailsList, self.PhoneNumbersList, self.AddressesList, self.NamesList)

        for i in range(len(LongestList) - len(self.EmailsList)):
            self.EmailsList += [" "]

        for i in range(len(LongestList) - len(self.PhoneNumbersList)):
            self.PhoneNumbersList += [" "]

        for i in range(len(LongestList) - len(self.AddressesList)):
            self.AddressesList += [" "]

        for i in range(len(LongestList) - len(self.NamesList)):
            self.NamesList += [" "]


        os.system(self.ClearScreenCommand)

        table = Table()

        if str(self.URL).startswith('http://'):
            TableHeader = str(self.URL).replace('http://','')
        elif str(self.URL).startswith("https://"):
            TableHeader = str(self.URL).replace('https://','')
        else:
            TableHeader = str(self.URL)

        table.title = TableHeader

        table.title_style = "bold"

        table.border_style = "rgb(255,255,255)"
        table.add_column("Emails", justify="right", style="rgb(255,255,255)", no_wrap=True)
        table.add_column("Phone Numbers", style="rgb(255,255,255)", no_wrap=True)
        table.add_column("Addresses", justify="right", style="rgb(255,255,255)", no_wrap=True)
        table.add_column("Names", justify="right", style="rgb(255,255,255)", no_wrap=True)



        for Email, PhoneNumber, Address, Name in zip(self.EmailsList, self.PhoneNumbersList, self.AddressesList,  self.NamesList):

                    table.add_row(Email,PhoneNumber,Address,Name)


        console = Console()
        console.print(table)
    #|=|=| OUTPUT CODE END |=|=|#


class UI:
    def __init__(self):
        self.Stamp = Stamps.Stamp
        self.HasInternet = None
        self.ClearScreenCommand = None
        if platform.system() == "Windows":
            self.UserOS = "Windows"
            os.system('@echo off')
            self.ClearScreenCommand = "cls"
        elif platform.system() == "Linux":
            self.UserOS = "Linux"
            self.ClearScreenCommand = "clear"
        elif platform.system() == "Darwin":
            self.UserOS = "MacOS"
            self.ClearScreenCommand = "clear"
        else:
            self.UserOS = "Unknown"
            self.ClearScreenCommand = None

        os.system(self.ClearScreenCommand)

        self.InternetConnection()
        self.Start()

    def InternetConnection(self):
        try:
            requests.get('https://google.com')
            self.HasInternet = True
        except:
            self.HasInternet = False
    def Start(self):
        WebTool = WebTools.WebTools()

        URL = input(f"{self.Stamp.Input} Please Enter URL: ")


        if not URL.startswith('https://') or URL.startswith('http://'):
            os.system(self.ClearScreenCommand)
            print(f"{self.Stamp.Error} {URL} Does not have a valid schema will need to reformat.")
            ReformatChoice = input(f"{self.Stamp.Input} Reformat URL to HTTP [1] or HTTPS [2]: ")

            if ReformatChoice == "1":
                URL = WebTool.RefactorHTTP(URL)
            elif ReformatChoice == "2":
                URL = WebTool.RefactorHTTPS(URL)
            else:
                print("Choice Not Valid")
                exit()

            if self.HasInternet == False:
                os.system(self.ClearScreenCommand)
                print(f"{Stamps.Stamp.Warring} Will not parse names due to lack of internet connective need for API calls")
                WantToContinue = input(f"{self.Stamp.Input} Do you want to continue y/n: ")

                if WantToContinue.lower() == "y" or WantToContinue == 'yes':
                    pass
                elif WantToContinue.lower() == "n" or WantToContinue == 'no':
                    exit()
                else:
                    print("Choice not valid")
                    exit()


            print('\n')
            Main(URL=URL)

        else:
            if self.HasInternet == False:
                print(f"{Stamps.Stamp.Warring} Will not parse names due to lack of internet connective need for API calls")
                WantToContinue = input(f"{self.Stamp.Input} Do you want to continue y/n: ")

                if WantToContinue.lower() == "y" or WantToContinue == 'yes':
                    pass
                elif WantToContinue.lower() == "n" or WantToContinue == 'no':
                    exit()
                else:
                    print("Choice not valid")
                    exit()
            os.system(self.ClearScreenCommand)

            print('\n')
            Main(URL=URL)

if __name__ == '__main__':
    UI()
    #Main(URL="https://www.wellsfargo.com/help/addresses/")

# https://www.wellsfargo.com/help/addresses/ | Works
# https://www.apple.com/contact/ | Works
# https://www.schwab.com/contact-us | Works
# https://it.tamu.edu/about/leadership/index.php | Works