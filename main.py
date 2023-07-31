import re
import requests
from bs4 import BeautifulSoup
import pandas
import sys
PhoneNumbersToBeFiltered = []
PhoneNumbersFiltered = []
EmailsToBeFiltered = []
EmailsFiltered = []
AddressesToBeFiltered = []
AddressesFiltered = []




AddressesRegex = r"^\d{1,5}\s\w{1,20}(?:[A-Za-z0-9. -]+[ ]?)+\w{2,}\.?(?:[,]\s\w{1,20}\s[A-Z]{2}\s\d{5})?$"  # matchs    501 Willow Lane, Greenville AL 36037 | 3371 S Alabama Ave, Monroeville AL 36460 | 34301 Hwy 43, Thomasville AL 36784
AddressesRegex2 = r"^\w{1,10}.\w{1,10}?.\w{1,10}?,.Suite.\d{1,10},.\w{1,20},.\w{2}.\d{1,5}"
AddressesRegex3 = r"^\d{1,5}.\w{1,20}.\w{1,10}.\w{2}\n\w{1,20},.\w{2}.\d{1,5}"
AddressesRegex4 = r"^\d{1,5}.\w{1,2}\W{1}.\w{1,20}.\w{1,20}.\w{1,20}.\w{1,20},.\w{2}.\d{1,5}"
AddressesRegex5 = r"^\d{1,5}.\w{1,2}\W{1}.\w{1,20}.\w{1,20}.\n.\w{1,20}.\w{1,20},.\w{2}.\d{1,5}"


EmailRegex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
PhoneNumberRegex1 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex2 = r"^\+?1?-\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex3 = r"\+?1?\s?\(?\d{3}\)?\s]?\d{3}\s]?\d{4}$"
PhoneNumberRegex4 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}.$"
PhoneNumberRegex5 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex6 = r"^\d{10}"

Response = requests.get("https://www.peoplemetrics.com/contact")
HtmlContent = Response.text

soup = BeautifulSoup(HtmlContent, 'html.parser')





tags = [
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




for tagU1 in soup.find_all(tags):
    PhoneNumber = tagU1.get_text().strip()
    for PhoneRegex in PhoneNumberRegex1, PhoneNumberRegex2, PhoneNumberRegex3, PhoneNumberRegex4, PhoneNumberRegex5, PhoneNumberRegex6:
        if re.match(PhoneRegex, PhoneNumber):
            PhoneNumbersToBeFiltered.append(PhoneNumber)


for i in PhoneNumbersToBeFiltered:
    if i not in PhoneNumbersFiltered:
        PhoneNumbersFiltered.append(i)


for tagU2 in soup.find_all(tags):
    Emails = tagU2.get_text().strip()
    if re.match(EmailRegex, Emails):
        EmailsToBeFiltered.append(Emails)

for i in EmailsToBeFiltered:
    if i not in EmailsFiltered:
        EmailsFiltered.append(i)



for tagU3 in soup.find_all(tags):
    Addresses = tagU3.get_text().strip()
    for AddressesRegexs in AddressesRegex, AddressesRegex2, AddressesRegex3, AddressesRegex4, AddressesRegex5:
        if re.match(AddressesRegexs, Addresses):
            AddressesToBeFiltered.append(Addresses)

for i in AddressesToBeFiltered:
    if i not in AddressesFiltered:
        AddressesFiltered.append(i)


DF = pandas.DataFrame({


    'Phone Numbers': PhoneNumbersFiltered,
    'Emails': EmailsFiltered,
    'Addresses': AddressesFiltered,

})


DFF = pandas.melt(DF)

print(DFF)



with open('output.txt', 'w') as file:
    file.write(DFF.to_string())

# This code will be a regex libreary for my WebsiteInfoGrabber project


