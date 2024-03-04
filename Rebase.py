import requests
from bs4 import BeautifulSoup
import os
import urllib3
import re


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

        self.NameRegex1 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1][a-z]{1,15}$"
        self.NameRegex2 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}[a-z]{1,15}$"
        self.NameRegex3 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}.\s[A-Z]{1}[a-z]{1,15}$"
        self.NameRegex4 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]\w{1,15}$'
        self.NameRegex5 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]{1}[a-z]{1,' \
                          r'15}\s[A-Z]{1}[a-z]{0,15}$'
        self.NameRegex6 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]{1}[a-z]{1,' \
                          r'15}\s[A-Z]{1}[a-z]{0,15}\s[A-Z]{1}[a-z]{0,15}$'

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

        self.PhoneNumberRegex1 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
        self.PhoneNumberRegex2 = r"^\+?1?-\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
        self.PhoneNumberRegex3 = r"\+?1?\s?\(?\d{3}\)?\s]?\d{3}\s]?\d{4}$"
        self.PhoneNumberRegex4 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}.$"
        self.PhoneNumberRegex5 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
        self.PhoneNumberRegex6 = r"^\d{10}"

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
                                     self.PhoneNumberRegex4, self.PhoneNumberRegex5, self.PhoneNumberRegex6]

        self.NameRegexList = [self.NameRegex1, self.NameRegex2, self.NameRegex3,
                              self.NameRegex4, self.NameRegex5, self.NameRegex6]

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
                                 self.AddressesRegex25,
                                 self.AddressesRegex26]

        self.Replace = [" ", "'", ",", "[", "]", "(", ")", "-", ".", "+"]

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

        # for String in self.Strings:
        #    print(String)

        # for String in self.Strings:
        #    print(String)

        self.Filter()

    def Filter(self):

        self.EmailsList = []
        self.PhoneNumbersList = []
        self.AddressesList = []

        # print(self.EmailRegex)
        for String in (self.Strings):
            print(String)

            # print(f"Pattern: {self.EmailRegex} String: {String}")
            if re.search(self.EmailRegex, String):
                if String not in self.EmailsList:
                    self.EmailsList.append(String)

            for Regex in self.PhoneNumberRegexList:
                if re.search(Regex, String):
                    if String not in self.PhoneNumbersList:
                        self.PhoneNumbersList.append(String)

            for Regex in self.AddressRegexList:
                if String in self.AddressesList:
                    continue
                else:
                    if re.match(Regex, String):
                        if String not in self.AddressesList:
                            self.AddressesList.append(String)


        #for String1, String2 in zip(self.Strings[0::2], self.Strings[1::2]):
        #    print(f"String 1: {String1}")
        #    print(f"String 2: {String2}")
        #    print(f"String 2: {String2}")
        #    print(f"String 1: {String1}")
        #    for Regex in self.AddressRegexList:
        #        if f"{String1}, {String2}" in self.AddressesList:
        #            continue
        #        else:
        #            if re.match(Regex, f"{String1}, {String2}"):
        #                if f"{String1} {String2}" not in self.AddressesList:
        #                    self.AddressesList.append(f"{String1}, {String2}")

        for Index, String in enumerate(self.Strings):
            for Regex in self.AddressRegexList:
                try:
                    NewString = f"{String}, {self.Strings[Index+1]}"
                    print(f"Index: {Index} String: {String}")
                    if NewString in self.AddressesList:
                        continue
                    else:
                        if re.match(Regex, NewString):
                            if NewString not in self.AddressesList:
                                self.AddressesList.append(NewString)
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


        print(self.EmailsList)
        print(self.PhoneNumbersList)
        print(self.AddressesList)


Main(URL="https://www.wellsfargo.com/help/addresses/")
