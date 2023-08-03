import re
import requests
from bs4 import BeautifulSoup
PhoneNumbersToBeFiltered = []
PhoneNumbersFiltered = []
EmailsToBeFiltered = []
EmailsFiltered = []
AddressesToBeFiltered = []
AddressesFiltered = []
NamesToBeFiltered = []
NamesFilteredReadyForAPI1 = []
APIList = []
APIOutput = []
APIOutputFiltered = []


EmailRegex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


NameRegex1 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1][a-z]{1,15}$"
NameRegex2 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}[a-z]{1,15}$"
NameRegex3 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}.\s[A-Z]{1}[a-z]{1,15}$"
NameRegex4 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]\w{1,15}$'
NameRegex5 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}[a-z]{0,15}$'
NameRegex6 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}[a-z]{0,15}\s[A-Z]{1}[a-z]{0,15}$'


AddressesRegex = r"^\d{1,5}\s\w{1,20}(?:[A-Za-z0-9. -]+[ ]?)+\w{2,}\.?(?:[,]\s\w{1,20}\s[A-Z]{2}\s\d{5})?$"
AddressesRegex2 = r"^\w{1,10}.\w{1,10}?.\w{1,10}?,.Suite.\d{1,10},.\w{1,20},.\w{2}.\d{1,5}"
AddressesRegex3 = r"^\d{1,5}.\w{1,20}.\w{1,10}.\w{2}\n\w{1,20},.\w{2}.\d{1,5}"
AddressesRegex4 = r"^\d{1,5}.\w{1,2}\W{1}.\w{1,20}.\w{1,20}.\w{1,20}.\w{1,20},.\w{2}.\d{1,5}"
AddressesRegex5 = r"^\d{1,5}.\w{1,2}\W{1}.\w{1,20}.\w{1,20}.\n.\w{1,20}.\w{1,20},.\w{2}.\d{1,5}"


PhoneNumberRegex1 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex2 = r"^\+?1?-\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex3 = r"\+?1?\s?\(?\d{3}\)?\s]?\d{3}\s]?\d{4}$"
PhoneNumberRegex4 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}.$"
PhoneNumberRegex5 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
PhoneNumberRegex6 = r"^\d{10}"

Response = requests.get("https://www.unileverusa.com/contact")
#Response = requests.get("https://www.peoplemetrics.com/contact") | Works

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




for tagU4 in soup.find_all(tags):
    Names = tagU4.get_text().strip()
    for NameRegexs in NameRegex1, NameRegex2, NameRegex3, NameRegex4, NameRegex5, NameRegex6:
        if re.match(NameRegexs, Names):
            NamesToBeFiltered.append(Names)


for i in NamesToBeFiltered:
    if i not in NamesFilteredReadyForAPI1:
        NamesFilteredReadyForAPI1.append(i)

APIReadySTR = str(NamesFilteredReadyForAPI1).replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace("(", "").replace(")", "")

for i in APIReadySTR.split():
        APIList.append(i)


for i in APIList:
    if requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{i}").status_code == 200:
        pass
    if requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{i}").status_code == 404:
        APIOutput.append(i)


APIOutputToString = str(APIOutput)
APIOutputToString = APIOutputToString.replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace("(", "").replace(")", "")


for i in APIOutputToString.split():
    if re.match(NameRegex1, i):
        APIOutputFiltered.append(i)



if len(PhoneNumbersFiltered) == 0:
    print("No Phone Numbers Found")
else:
    print("Phone Numbers Found: " + str(PhoneNumbersFiltered).replace("[", "").replace("]", "").replace("'", "").replace(",", "|").replace("(", "").replace(")", ""))

if len(EmailsFiltered) == 0:
    print("No Emails Found")
else:
    print("Emails Found: " + str(EmailsFiltered).replace("[", "").replace("]", "").replace("'", "").replace(",", "|").replace("(", "").replace(")", ""))

if len(AddressesFiltered) == 0:
    print("No Addresses Found")
else:
    print("Addresses Found: " + str(AddressesFiltered).replace("[", "").replace("]", "").replace("'", "").replace(",", "|").replace("(", "").replace(")", ""))

if len(APIOutputFiltered) == 0:
    print("No Names Found")
else:
    print("Names Found: " + str(APIOutputFiltered).replace("[", "").replace("]", "").replace("'", "").replace(",", "|").replace("(", "").replace(")", ""))


#f len(PhoneNumbersFiltered) == 0:

#   print("No Phone Numbers Found")
#   with open('output.txt', 'w') as file:
#       file.write("No Phone Numbers Found" + '\n' + '\r')

#lse:

#   DF1 = pandas.DataFrame({ 'Phone Numbers': PhoneNumbersFiltered})
#   print(DF1.to_string(index=False).strip())

#   with open('output.txt', 'w') as file:
#      file.write(DF1.to_string(index=False).strip()+'\n'+'\r')



#f len(EmailsFiltered) == 0:

#   print("No Emails Found")

#   with open('output.txt', 'w') as file:
#       file.write("No Emails Found")

#lse:

#   DF2 = pandas.DataFrame({ 'Emails': EmailsFiltered})
#   print(DF2.to_string(index=False).strip())

#   with open('output.txt', 'w') as file:
#       file.write(DF2.to_string(index=False).strip() + '\n' + '\r')



#f len(AddressesFiltered) == 0:

#   print("No Addresses Found")

#   with open('output.txt', 'w') as file:
#       file.write("No Addresses Found" + '\n' + '\r')
#lse:

#   DF3 = pandas.DataFrame({ 'Addresses': AddressesFiltered})
#   print(DF3.to_string(index=False).strip())

#   with open('output.txt', 'w') as file:
#       file.write(DF3.to_string(index=False).strip() + '\n' + '\r')



#f len(APIOutput) == 0:

#   print("No Names Found")

#   with open('output.txt', 'w') as file:
#       file.write("No Names Found" + '\n' + '\r')

#lse:

#   DF4 = pandas.DataFrame({ 'Names': APIOutputFiltered})
#   print(DF4.to_string(index=False).strip())

#   with open('output.txt', 'w') as file:
#       file.write(DF4.to_string(index=False).strip())


# This code will be a regex libreary for my WebsiteInfoGrabber project


