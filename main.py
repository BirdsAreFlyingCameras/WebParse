import re
import requests
from bs4 import BeautifulSoup
import pandas

PhoneNumbersToBeFiltered = []
PhoneNumbersFiltered = []
EmailsToBeFiltered = []
EmailsFiltered = []



EmailRegex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
PhoneNumberRegex1 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex2 = r"^\+?1?-\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex3 = r"\+?1?\s?\(?\d{3}\)?\s]?\d{3}\s]?\d{4}$"
PhoneNumberRegex4 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}.$"
PhoneNumberRegex5 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex6 = r"^\d{10}"

Response = requests.get("https://www.ally.com/contact-us/")
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




DF1 = pandas.DataFrame({


    'Phone Numbers': PhoneNumbersFiltered,

})


DF2 = pandas.DataFrame({


    'Emails': EmailsFiltered,

})

print(EmailsFiltered)
print(PhoneNumbersFiltered)

DFF = pandas.concat([DF1, DF2], axis=1)

pandas.melt(DFF)

print(DFF)

# This code will be a regex libreary for my WebsiteInfoGrabber project


