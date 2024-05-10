import pprint
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
import brotli


class Main:

    def __init__(self, URL):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.URL = URL

        self.WebHeaders = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Sec-CH-UA": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": "\"Windows\"",
            "Cache-Control": "max-age=0",

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
        Response = requests.get(f"{self.URL}", headers=self.WebHeaders, verify=False)

        self.HtmlContent = Response.text

        self.Soup = BeautifulSoup(self.HtmlContent, 'html.parser')

        AllTags = self.Soup.descendants


        #print(Response.status_code) # Debug
        #print(Response.apparent_encoding) #Debug
        #print(Response.is_redirect) # Debug
        #print(Response.next) # Debug
        #print(Response.headers) # Debug
        #print(Response.raw) # Debug
        #print(Response.content) # Debug


        for Tag in AllTags:
            for String in Tag.stripped_strings:
                if String not in self.Strings:
                    self.Strings.append(String)

        self.Filter()

    def MatchNamesAPICalls(self, Name):  # For name matching | Called in the Filter function

        for Regex in self.NameRegexList:

            if Name in self.NamesList:
                continue

            SubStrings = Name.split(" ")

            InDict = []
            NotInDict = []

            if re.fullmatch(Regex, Name):
                for SubString in SubStrings:

                    try:

                        if SubString in self.NamesFromFile:
                            NotInDict.append(SubString)
                            continue
                        if requests.get(f"https://www.dictionary.com/browse/{SubString}").status_code == 404:
                            NotInDict.append(SubString)
                            continue
                        elif requests.get(f"https://www.dictionary.com/browse/{SubString}").status_code == 200:
                            InDict.append(SubString)
                            continue

                    except requests.exceptions.RequestException:
                        print(f"{Stamps.Stamp.Warring} API Request Error. Continuing...")
                        continue

                if len(NotInDict) != 0 and Name not in self.NamesList:
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
        print(self.PhoneNumbersList)
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
                    print(f"{Stamps.Stamp.Info} Regex Match Timed Out. Continuing to next address.")
                    print(e)
                    continue
                except IndexError:
                    break



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

        self.RealLenDict = {"EmailsList":len(self.EmailsList), "PhoneNumbersList":len(self.PhoneNumbersList),
                            "AddressesList":len(self.AddressesList), "NamesList": len(self.NamesList)}

        LongestList = max(len(self.EmailsList), len(self.PhoneNumbersList), len(self.AddressesList), len(self.NamesList))

        for _ in range(LongestList - len(self.EmailsList)):
            self.EmailsList += [" "]

        for _ in range(LongestList - len(self.PhoneNumbersList)):
            self.PhoneNumbersList += [" "]

        for _ in range(LongestList - len(self.AddressesList)):
            self.AddressesList += [" "]

        for _ in range(LongestList - len(self.NamesList)):
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

        self.SaveResults()

    #|=|=| OUTPUT CODE END |=|=|#



    #|=|=| Save Results CODE START |=|=|#

    def SaveResults(self):

        print('\n')

        SaveResultsChoice = input(f"{Stamps.Stamp.Input} Save Results [y/n]: ")

        if SaveResultsChoice == "y" or SaveResultsChoice == "Y" or SaveResultsChoice == "yes" or SaveResultsChoice == "Yes":

            if str(self.URL).startswith('https://'):
                SaveFileName = str(self.URL).replace('https://', '')
                BannerNameForTXT = SaveFileName[:SaveFileName.index('/')]
                SaveFileName = f"{SaveFileName[:SaveFileName.index('/')]}-WebParse-Results.txt"

            elif str(self.URL).startswith('http://'):
                SaveFileName = str(self.URL).replace('http://', '')
                BannerNameForTXT = SaveFileName[:SaveFileName.index('/')]
                SaveFileName = f"{SaveFileName[:SaveFileName.index('/')]}-WebParse-Results.txt"

            else:
                SaveFileName = str(self.URL)[:str(self.URL).index('/')]
                SaveFileName = f"{SaveFileName}-WebParse-Results.txt"
                BannerNameForTXT = str(self.URL)[:str(self.URL).index('/')]

            if os.path.exists(SaveFileName):
                print("\n")
                PathAlreadyExistChoice = input(f'{Stamps.Stamp.Error} A file with the name {SaveFileName} already exists. Over Write File [1] | Change Save File Name [2] | Exit [3]: ')

                if PathAlreadyExistChoice == "1":
                    os.remove(SaveFileName)

                elif PathAlreadyExistChoice == "2":
                    print("\n")
                    SaveFileName = input(f"{Stamps.Stamp.Input} New File Name: ")

                    if not SaveFileName.endswith(".txt"):
                        SaveFileName = f"{SaveFileName}.txt"
                    BannerNameForTXT = SaveFileName.replace(".txt", "")

                elif PathAlreadyExistChoice == "3":
                    exit()

                else:

                    print('\n')
                    print(f"{Stamps.Stamp.Error} Invalid Choice")
                    print("\n")
                    PathAlreadyExistChoice = input(f'{Stamps.Stamp.Error} A file with the name {SaveFileName} already exists. Over Write File [1] | Change Save File Name [2] | Exit [3]: ')

                    if PathAlreadyExistChoice == "1":
                        os.remove(SaveFileName)

                    if PathAlreadyExistChoice == "2":
                        print("\n")
                        SaveFileName = input(f"{Stamps.Stamp.Input} New File Name: ")

                        if not SaveFileName.endswith(".txt"):
                            SaveFileName = f"{SaveFileName}.txt"
                        BannerNameForTXT = SaveFileName.replace(".txt", "")

                    if PathAlreadyExistChoice == "3":
                        exit()


            with open(SaveFileName, 'x', encoding='utf-8') as f:

                f.write(f"┣━━━━━━━━━━ WebParse Results for {BannerNameForTXT} ━━━━━━━━━━┫")

                f.write('\n')
                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ Emails ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if self.RealLenDict.get('EmailsList') != 0:
                    for Email in self.EmailsList:
                        f.write(Email)
                        f.write('\n')

                else:
                    f.write("No Emails Found")


                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ Phone Numbers ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if self.RealLenDict.get('PhoneNumbersList') != 0:
                    for PhoneNumber in self.PhoneNumbersList:
                        f.write(PhoneNumber)
                        f.write('\n')
                else:
                    f.write("No Phone Numbers Found")


                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ Addresses ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if self.RealLenDict.get('AddressesList') != 0:
                    for Address in self.AddressesList:
                        f.write(Address)
                        f.write('\n')
                else:
                    f.write("No Addresses Found")


                f.write('\n')
                f.write('\n')

                f.write('━━━━━┫ Names ┣━━━━━')

                f.write('\n')
                f.write('\n')

                if self.RealLenDict.get('NamesList') != 0:
                    for Name in self.NamesList:
                        f.write(Name)
                        f.write('\n')
                else:
                    f.write("No Names Found")


            print("\n")

            if self.UserOS == "Linux" or self.UserOS == "MacOS" or self.UserOS == "Unknown":
                print(f"{Stamps.Stamp.Output} Saved Results to {os.path.dirname(os.path.abspath(__file__))}/{SaveFileName}")
            else:
                print(f"{Stamps.Stamp.Output} Saved Results to {os.path.dirname(os.path.abspath(__file__))}\\{SaveFileName}")

        else:
            print('\n')
            print(f"{Stamps.Stamp.Info} Exiting")
            exit()

    #|=|=| Save Results CODE END |=|=|#



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
        except requests.exceptions.ConnectionError:
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

            if self.HasInternet is False:
                os.system(self.ClearScreenCommand)
                print(f"{Stamps.Stamp.Warring} Will not parse names due to lack of internet connective need for API calls")
                WantToContinue = input(f"{self.Stamp.Input} Do you want to continue y/n: ")

                if WantToContinue.lower() == "n" or WantToContinue.lower() == 'no':
                    exit()
                else:
                    print("Choice not valid")
                    exit()


            print('\n')
            Main(URL=URL)

        else:
            if self.HasInternet is False:
                print(f"{Stamps.Stamp.Warring} Will not parse names due to lack of internet connective need for API calls")
                WantToContinue = input(f"{self.Stamp.Input} Do you want to continue y/n: ")

                if WantToContinue.lower() == "n" or WantToContinue.lower() == 'no':
                    exit()
                else:
                    print("Choice not valid")
                    exit()

            os.system(self.ClearScreenCommand)

            print('\n')
            Main(URL=URL)

if __name__ == '__main__':
    #UI()
    Main(URL="https://www.apple.com/contact/")

# https://www.aetna.com/about-us/contact-aetna.html | works
# https://www.wellsfargo.com/help/addresses/ | Works
# https://www.schwab.com/contact-us | Works
# https://it.tamu.edu/about/leadership/index.php | Works


# https://www.dyson.co.uk/support/contact-us | Bricks the program


# https://tfglimited.co.za/contact/ | Emails being redacted by CDN

# https://www.apple.com/contact/ | Not getting all the phone numbers
# https://www.gmfinancial.com/en-us/contact.html | Names are not names and it added 9 a.m. - 1 p.m. CT to the address
# https://admissions.umich.edu/explore-visit/contact-us | Sort of working not getting full address and names mathing to places