import re
import requests
from bs4 import BeautifulSoup
import pandas

PhoneNumbersToBeFiltered = []


EmailRegex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
PhoneNumberRegex1 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex2 = r"^\+?1?-\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex3 = r"\+?1?\s?\(?\d{3}\)?\s]?\d{3}\s]?\d{4}$"
PhoneNumberRegex4 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}.$"
PhoneNumberRegex5 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex6 = r"^\d{10}"

Response = requests.get("https://www.missionoaksdental.com/contact/dentist-appointment/?sc_cid=GBP%3AO%3AGP%3A166%3AOrganic_Search%3AGeneral%3Ana&y_source=1_MTEwMjc1NS03MTUtbG9jYXRpb24ucmVzZXJ2YXRpb25fdXJs")
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




for tags in soup.find_all(tags):
    PhoneNumber = tags.get_text().strip()
    for PhoneRegex in PhoneNumberRegex1, PhoneNumberRegex2, PhoneNumberRegex3, PhoneNumberRegex4, PhoneNumberRegex5, PhoneNumberRegex6, EmailRegex:
        if re.match(PhoneRegex, PhoneNumber):
            PhoneNumbersToBeFiltered.append(PhoneNumber)

PhoneNumbersFiltered = []
for i in PhoneNumbersToBeFiltered:
    if i not in PhoneNumbersFiltered:
        PhoneNumbersFiltered.append(i)



DF = pandas.DataFrame(

    [PhoneNumbersFiltered],
    index = [PhoneNumbersFiltered.index(i) for i in PhoneNumbersFiltered],
    columns = ["Phone Numbers"]

)

print(DF)



# This code will be a regex libreary for my WebsiteInfoGrabber project


