import PyEnhance.Loading
import requests
from bs4 import BeautifulSoup
import os
import urllib3
import re
import regex
from PyEnhance import Loading

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

        self.StringsDebugList = [] # REMOVE JUST FOR TESTING
        self.NamesMatchedButNotPassed = [] # REMOVE JUST FOR TESTING
        self.GetHtml()

    def LoadingI(self):
        Loading = PyEnhance.Loading.Loading()

        self.LoadingEmails = Loading.Spin(Text="Getting Emails")
        self.LoadingAddresses = Loading.Spin(Text="Getting Addresses")
        self.LoadingPhoneNumbers = Loading.Spin("Getting Phone Numbers")
        self.LoadingNames = Loading.Spin(Text="Getting Names")


    def GetHtml(self):
        Response = requests.get(f"{self.URL}", headers=self.WebHeaders, verify=False, )

        self.HtmlContent = Response.text

        self.Soup = BeautifulSoup(self.HtmlContent, 'html.parser')

        AllTags = self.Soup.descendants

        for Tag in AllTags:
            for String in Tag.stripped_strings:
                if String not in self.Strings:
                    self.Strings.append(String)

        # for String in self.Strings:
        #    print(String)

        # for String in self.Strings:
        #    print(String)

        self.Filter()

    def Filter(self):

        self.EmailsList = []
        self.PhoneNumbersList = []
        self.AddressesList = []
        self.NamesList = []


    #|=|=| EMAIL MATCH CODE START |=|=|#
        self.EmailLoading = PyEnhance.Loading.Loading()

        self.EmailLoading.Spin(Text="Getting Emails")

        # print(self.EmailRegex)
        for String in self.Strings:
            # print(f"Pattern: {self.EmailRegex} String: {String}")
            if re.search(self.EmailRegex, String):
                if String not in self.EmailsList:
                    self.EmailsList.append(String)

    #|=|=| EMAIL MATCH CODE END |=|=|#



    #|=|=| PHONE NUMBER MATCH CODE START |=|=|#

        self.EmailLoading.Stop()
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
        self.AddressLoading = PyEnhance.Loading.Loading()
        self.AddressLoading.Spin("Getting Addresses")
        for String in self.Strings:
            for Regex in self.AddressRegexList:

                #if String not in self.DebugAddressStrings:
                #    #print(f"String: {String}")
                #    self.DebugAddressStrings.append(String)

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

                    #if NewString not in self.DebugAddressStrings:
                    #    #print(f"Index: {Index} String: {String}")
                    #    self.DebugAddressStrings.append(NewString)

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



    #|=|=| NAME MATCH CODE START |=|=|#

        self.AddressLoading.Stop()
        self.NameLoading = PyEnhance.Loading.Loading()
        self.NameLoading.Spin("Getting Names")

        StringsForNames = self.Strings

        for String in StringsForNames:
            for Regex in self.NameRegexList:

                if String in self.NamesList:
                    continue

                SubStrings = String.split(" ")

                # ||| DEBUG CODE START |||

                if String not in self.StringsDebugList:
                    self.StringsDebugList.append(String)

                # ||| DEBUG CODE END |||

                if re.fullmatch(Regex, String):
                    for SubString in SubStrings:
                            #print(f"String: {String}")
                            #print(f"Sub Strings: {SubStrings}")

                            if requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{SubString}").status_code == 200:

                                #print(f"String: {String}")
                                #print(f"Sub Strings: {SubStrings}")

                                if SubString == SubStrings[-1]:

                                    IndexToRemove = StringsForNames.index(String)
                                    StringsForNames.pop(IndexToRemove)
                                    self.NamesMatchedButNotPassed.append(String)
                                    break
                                else:
                                    continue

                            if requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{SubString}").status_code == 404:
                                if String not in self.NamesList:
                                    self.NamesList.append(String)


        #print(self.NamesList) # ||| DEBUG REMOVE AFTER

        # ||| START OF TEST CODE FOR PyEnhance REMOVE WHEN DONE!!! |||

        NamesFromFile = []

        with open('Names.txt', 'r') as f:

            for Name in f:
                NamesFromFile.append(Name.replace('\n', ''))


        # ||| END OF TEST CODE FOR PyEnhance REMOVE WHEN DONE!!! |||



        NamesToRemove = []

        for Name in self.NamesList:

            #print(f"Name: {Name}")# ||| DEBUG REMOVE AFTER
            #print(f"Names List: {self.NamesList}")# ||| DEBUG REMOVE AFTER


            NameSubs = str(Name).split(' ')
            InDict = []
            NotInDict = []

            for SubName in NameSubs:

                if requests.get(f"https://www.dictionary.com/browse/{SubName}").status_code == 200:
                    InDict.append(SubName)

                if requests.get(f"https://www.dictionary.com/browse/{SubName}").status_code == 200 and SubName in NamesFromFile:
                    NotInDict.append(SubName)

                if requests.get(f"https://www.dictionary.com/browse/{SubName}").status_code == 404:
                    NotInDict.append(SubName)


            # ||| DEBUG START |||

            #print(f"Name: {Name}")
            #print(f"In the dict: {InDict}")
            #print(f"Not In the dict: {NotInDict}")

            # ||| DEBUG END |||


            if len(NotInDict) == 0:
                NamesToRemove.append(Name)

        for NameToRemove in NamesToRemove:
            self.NamesList.remove(NameToRemove)

        self.NameLoading.Stop()

        #|=|=| NAME MATCH CODE END |=|=|#



    #|=|=| OUTPUT CODE START |=|=|#

        print(f"Emails: {self.EmailsList}")
        print(f"Phone Numbers: {self.PhoneNumbersList}")
        print(f"Addresses: {self.AddressesList}")
        print(f"Names: {self.NamesList}")

        print('\n')



    #|=|=| OUTPUT CODE END |=|=|#



    #|=|=| DEBUG CODE START |=|=|#

        #for Name in self.NamesList:
        #    NameSub = str(Name).split(' ')
        #    print(f"Full Name: {Name}")
        #    print(f"Sub Strings: {NameSub}")

        #print(self.NamesMatchedButNotPassed)

        if os.path.exists('DebugAddressStrings.txt'):
            os.remove('DebugAddressStrings.txt')

        with open('DebugAddressStrings.txt', 'x', encoding='utf-8') as f:
            for String in self.StringsDebugList:
                try:
                    f.write(f"'{String}',")
                    f.write('\n')
                except:
                    continue

    #|=|=| DEBUG CODE END |=|=|#


Main(URL="https://www.wellsfargo.com/help/addresses/")

# https://www.wellsfargo.com/help/addresses/ | Works
# https://www.apple.com/contact/ | Works
# https://www.schwab.com/contact-us | https://www.schwab.com/contact-us | Works
# https://it.tamu.edu/about/leadership/index.php | Works