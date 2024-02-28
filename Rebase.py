import requests
from bs4 import BeautifulSoup
import os
import urllib3
import re



class Main:

    def __init__(self, URL):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.URL =URL

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
        self.AddressesRegex = r"^\d{1,5}\s\w{1,20}(?:[A-Za-z0-9. -]+[ ]?)+\w{2,}\.?(?:[,]\s\w{1,20}\s[A-Z]{2}\s\d{5})?$"
        self.AddressesRegex2 = r"^\w{1,10}.\w{1,10}?.\w{1,10}?,.Suite.\d{1,10},.\w{1,20},.\w{2}.\d{1,5}"
        self.AddressesRegex3 = r"^\d{1,5}.\w{1,20}.\w{1,10}.\w{2}\n\w{1,20},.\w{2}.\d{1,5}"
        self.AddressesRegex4 = r"^\d{1,5}.\w{1,2}\W{1}.\w{1,20}.\w{1,20}.\w{1,20}.\w{1,20},.\w{2}.\d{1,5}"
        self.AddressesRegex5 = r"^\d{1,5}.\w{1,2}\W{1}.\w{1,20}.\w{1,20}.\n.\w{1,20}.\w{1,20},.\w{2}.\d{1,5}"
        self.AddressesRegex6 = r"\d{0,5}.\w{0,20}.\w{0,20}\n[A-Z]{1}\w{1,20}..?[A-Z]{0,2}.\d{0,5}"
        self.AddressesRegex7 = r"\d{1,5}.\w{1,20}.[A-Z]{1}[a-z]{1,20}..?[A-Z]{1}[a-z]{1,20}..?[A-Z]{1,2}.\d{1,5}"
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

        self.AddressesRegexList = [self.AddressesRegex, self.AddressesRegex2, self.AddressesRegex3,
                              self.AddressesRegex4, self.AddressesRegex5, self.AddressesRegex6,
                              self.AddressesRegex7]

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

        #for String in self.Strings:
        #    print(String)


        self.Filter()
    def Filter(self):

        self.EmailsList = []
        self.PhoneNumbersList = []
        self.AddressesList = []

        #print(self.EmailRegex)
        for String in self.Strings:

            #print(f"Pattern: {self.EmailRegex} String: {String}")
            if re.search(self.EmailRegex, String):
                print(String)



Main(URL="https://www.ally.com/contact-us/")

