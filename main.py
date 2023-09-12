import re
import requests
from bs4 import BeautifulSoup
import os

def main():

    class Regexs:

        global EmailRegex, APIReadySTR
        global NameRegex1, NameRegex2, NameRegex3, NameRegex4, NameRegex5, NameRegex6
        global AddressesRegex , AddressesRegex2, AddressesRegex3
        global AddressesRegex4, AddressesRegex5, AddressesRegex6, AddressesRegex7
        global PhoneNumberRegex1, PhoneNumberRegex2, PhoneNumberRegex3
        global PhoneNumberRegex4, PhoneNumberRegex5, PhoneNumberRegex6


        EmailRegex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        NameRegex1 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1][a-z]{1,15}$"
        NameRegex2 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}[a-z]{1,15}$"
        NameRegex3 = r"^[A-Z]{1}[a-z]{1,15}\s[A-Z]{1}.\s[A-Z]{1}[a-z]{1,15}$"
        NameRegex4 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]\w{1,15}$'
        NameRegex5 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]{1}[a-z]{1,' \
                     r'15}\s[A-Z]{1}[a-z]{0,15}$'
        NameRegex6 = r'^(?:Ms|Mrs|Mr|Miss|Master|Mx|Dr|Prof|Rev|Hon|Col|Gen|Maj|Capt|Sen|Rep|Esq)\.[A-Z]{1}[a-z]{1,' \
                     r'15}\s[A-Z]{1}[a-z]{0,15}\s[A-Z]{1}[a-z]{0,15}$'

        AddressesRegex = r"^\d{1,5}\s\w{1,20}(?:[A-Za-z0-9. -]+[ ]?)+\w{2,}\.?(?:[,]\s\w{1,20}\s[A-Z]{2}\s\d{5})?$"
        AddressesRegex2 = r"^\w{1,10}.\w{1,10}?.\w{1,10}?,.Suite.\d{1,10},.\w{1,20},.\w{2}.\d{1,5}"
        AddressesRegex3 = r"^\d{1,5}.\w{1,20}.\w{1,10}.\w{2}\n\w{1,20},.\w{2}.\d{1,5}"
        AddressesRegex4 = r"^\d{1,5}.\w{1,2}\W{1}.\w{1,20}.\w{1,20}.\w{1,20}.\w{1,20},.\w{2}.\d{1,5}"
        AddressesRegex5 = r"^\d{1,5}.\w{1,2}\W{1}.\w{1,20}.\w{1,20}.\n.\w{1,20}.\w{1,20},.\w{2}.\d{1,5}"
        AddressesRegex6 = r"\d{0,5}.\w{0,20}.\w{0,20}\n[A-Z]{1}\w{1,20}..?[A-Z]{0,2}.\d{0,5}"
        AddressesRegex7 = r"\d{1,5}.\w{1,20}.[A-Z]{1}[a-z]{1,20}..?[A-Z]{1}[a-z]{1,20}..?[A-Z]{1,2}.\d{1,5}"

        PhoneNumberRegex1 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
        PhoneNumberRegex2 = r"^\+?1?-\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
        PhoneNumberRegex3 = r"\+?1?\s?\(?\d{3}\)?\s]?\d{3}\s]?\d{4}$"
        PhoneNumberRegex4 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}.$"
        PhoneNumberRegex5 = r"^\+?1?\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"
        PhoneNumberRegex6 = r"^\d{10}"
    class ListAndDicts:

        global PhoneNumbersToBeFiltered, PhoneNumbersFiltered, PhoneNumbersFormatted
        global EmailsToBeFiltered, EmailsFiltered
        global AddressesToBeFiltered, AddressesFiltered, LongPrefixList, ShortPrefixList, AddyDict
        global StreetEndingsLong, StreetEndingsShort
        global NamesToBeFiltered, NamesFilteredReadyForAPI1
        global APIList, APIOutput, APIOutputFiltered
        global tags
        global PhoneNumberRegexList, NameRegexList, AddressesRegexList
        global Replace


        PhoneNumbersToBeFiltered = []
        PhoneNumbersFiltered = []
        PhoneNumbersFormatted = []
        EmailsToBeFiltered = []
        EmailsFiltered = []
        AddressesToBeFiltered = []
        AddressesFiltered = []
        LongPrefixList = []
        ShortPrefixList = []
        AddyDict = {}

        NamesToBeFiltered = []
        NamesFilteredReadyForAPI1 = []
        APIList = []
        APIOutput = []
        APIOutputFiltered = []

        StreetEndingsLong = [
            "Avenue", "Boulevard", "Drive", "Lane",
            "Place", "Road", "Street", "Way",
            "Circle", "Court", "Crescent", "Expressway",
            "Freeway", "Parkway", "Square"
        ]

        StreetEndingsShort = [
            "Ave.","Blvd.","Dr.","Ln.",
            "Pl.", "Rd.", "St.", "Wy.",
            "Cir.", "Ct.", "Cres.", "Expy.",
            "Fwy.","Pkwy.","Sq.",]

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

        PhoneNumberRegexList = [PhoneNumberRegex1, PhoneNumberRegex2, PhoneNumberRegex3,
                                 PhoneNumberRegex4, PhoneNumberRegex5, PhoneNumberRegex6]
        NameRegexList = [NameRegex1, NameRegex2, NameRegex3, NameRegex4, NameRegex5, NameRegex6]

        AddressesRegexList = [AddressesRegex, AddressesRegex2, AddressesRegex3,
                              AddressesRegex4, AddressesRegex5, AddressesRegex6,
                              AddressesRegex7]


        Replace = [" ", "'", ",", "[", "]", "(", ")","-", ".","+"]


    # Response = requests.get('https://www.progressive.com/contact-us')
    #Response = requests.get("https://www.unileverusa.com/contact")  # | works
    #Response = requests.get("https://www.peoplemetrics.com/contact")  # | Works
    #Response = requests.get(
    # +
    #
    # .0
    # "https://www.pge.com/en_US/residential/customer-service/help/contact-pge-landing/contact-us.page") # | Works
    #Response = requests.get()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "en-US,en;q=0.5",

    }



    def Input():
        global URL

        #URL = input('Please Enter URL: ')

        URL = "https://aetna.com/about-us/contact-aetna.html"

        if URL.startswith('https://'):
            global FileName
            if URL[8:].startswith('www.'):
                if ((URL[8:].count('/'))) >= 1:
                    Index = URL[8:].index('/')
                    FileName = URL[12:Index+8]

                if ((URL[8:].count('/'))) == 0:
                    FileName = URL[12:]

            else:
                if ((URL[8:].count('/'))) >= 1:
                    Index = URL[8:].index('/')
                    FileName = URL[8:Index + 8]

                if ((URL[8:].count('/'))) == 0:
                    FileName = URL[8:]

        print(FileName)



    Input()


    Response = requests.get(f"{URL}", headers=headers) # | Does Not Work


    HtmlContent = Response.text

    soup = BeautifulSoup(HtmlContent, 'html.parser')

    def FilterByTag():


        def PhoneNumberTag():
            for tagU1 in soup.find_all(tags):
                PhoneNumber = tagU1.get_text().strip()

                for PhoneRegex in PhoneNumberRegexList:

                    if re.match(PhoneRegex, PhoneNumber):
                        PhoneNumbersToBeFiltered.append(PhoneNumber)

            for i in PhoneNumbersToBeFiltered:

                if i not in PhoneNumbersFiltered:
                    PhoneNumbersFiltered.append(i)

            for i in range(len(PhoneNumbersFiltered)):

                for x in Replace:
                    PhonenumbersToBeFormated = str(PhoneNumbersFiltered[i]).replace(x, "")

                if len(PhonenumbersToBeFormated) == 10:
                    x = list(PhonenumbersToBeFormated)
                    x.insert(3, "-")
                    x.insert(7, "-")
                    for i in Replace:
                        NumberFormated = (str(x).strip("[]").replace(i, ""))

                    if NumberFormated not in PhoneNumbersFormatted:
                        PhoneNumbersFormatted.append(NumberFormated)
                else:
                    if PhonenumbersToBeFormated not in PhoneNumbersFormatted:
                        PhoneNumbersFormatted.append(PhonenumbersToBeFormated)


        def EmailTag():

            for tagU2 in soup.find_all(tags):
                Emails = tagU2.get_text().strip()
                if re.match(EmailRegex, Emails):

                    if Emails not in EmailsToBeFiltered:

                        EmailsToBeFiltered.append(Emails)

                    else:
                        continue

            for i in EmailsToBeFiltered:
                if i not in EmailsFiltered:
                    EmailsFiltered.append(i)

        def AddressesTag():

            for tagU3 in soup.find_all(tags):
                Addresses = tagU3.get_text().strip()
                lines = [line.strip() for line in Addresses.splitlines() if line.strip()]
                for pattern in AddressesRegexList:
                        for line in lines:
                            if re.search(pattern, line):
                                if line not in AddressesToBeFiltered:
                                    AddressesToBeFiltered.append(line)

            indices = [index for index, address in enumerate(AddressesToBeFiltered) if
                       any(prefix in address for prefix in StreetEndingsLong)]

            for i in indices:
                AddressesFiltered.append(AddressesToBeFiltered[i])

        def NamesTag():

            for tagU4 in soup.find_all(tags):
                Names = tagU4.get_text().strip()
                for NameRegexs in NameRegexList:
                    if re.match(NameRegexs, Names):
                        NamesToBeFiltered.append(Names)

            for i in NamesToBeFiltered:
                if i not in NamesFilteredReadyForAPI1:
                    NamesFilteredReadyForAPI1.append(i)

            for x in Replace:
                APIReadySTR = str(NamesFilteredReadyForAPI1).replace(x, "")

            for i in APIReadySTR.split():
                APIList.append(i)

            for i in APIList:
                if requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{i}").status_code == 200:
                    pass
                if requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{i}").status_code == 404:
                    APIOutput.append(i)

            APIOutputToString = str(APIOutput)
            for x in Replace:
                APIOutputToString = APIOutputToString.replace(x,"")

            for i in APIOutputToString.split():
                if re.match(NameRegex1, i):
                    APIOutputFiltered.append(i)

        PhoneNumberTag()
        EmailTag()
        AddressesTag()
        NamesTag()
    FilterByTag()

    def Outputs():

        def PhoneNumbersOutput():
            if len(PhoneNumbersFiltered) == 0:
                print("No Phone Numbers Found")

                if os.path.exists(f'{FileName}.txt'):
                    with open(f"{FileName}.txt", "a") as file:
                        file.write("No Phone Numbers Found\n")
                else:
                    with open(f"{FileName}.txt", "x") as file:
                        file.write("No Phone Numbers Found\n")

            else:
                for x in Replace:
                    PhoneNumberOutput = ("Phone Numbers Found: " + str(PhoneNumbersFormatted).replace("[", "").replace("]", "")
                            .replace(x,"").replace("'", ""))

                print(PhoneNumberOutput)

                if os.path.exists(f'{FileName}.txt'):
                    with open(f"{FileName}.txt", "a") as file:
                        file.write(f'{PhoneNumberOutput}\n')

                else:
                    with open(f"{FileName}.txt", "x") as file:
                        file.write(f'{PhoneNumberOutput}\n')


        def EmailsOutput():

            if len(EmailsFiltered) == 0:
                print("No Emails Found")

                if os.path.exists(f'{FileName}.txt'):
                    with open(f"{FileName}.txt", "a") as file:
                        file.write("No Emails Found\n")
                else:
                    with open(f"{FileName}.txt", "x") as file:
                        file.write("No Emails Found\n")

            else:
                for x in Replace:
                    EmailOutput = ("Emails Found: " + str(EmailsFiltered).replace("[", "")
                                   .replace("]", "").replace(x,"").replace("'", ""))

                print(EmailOutput)

                if os.path.exists(f'{FileName}.txt'):
                    with open(f"{FileName}.txt", "a") as file:
                        file.write(f'{EmailOutput}\n')

                else:
                    with open(f"{FileName}.txt", "x") as file:
                        file.write(f'{EmailOutput}\n')




        def AddressesOutput():

            if len(AddressesFiltered) == 0:
                print("No Addresses Found")

                if os.path.exists(f'{FileName}.txt'):
                    with open(f"{FileName}.txt", "a") as file:
                        file.write("No Addresses Found\n")
                else:
                    with open(f"{FileName}.txt", "x") as file:
                        file.write("No Addresses Found\n")

            else:
                for x in Replace:
                    AddressesOutput = ("Addresses Found: " + str(AddressesFiltered).replace("[", "")
                               .replace("]", "").replace(x,"").replace("'", ""))

                print(AddressesOutput)

                if os.path.exists(f'{FileName}.txt'):
                    with open(f"{FileName}.txt", "a") as file:
                        file.write(f'{AddressesOutput}\n')

                else:
                    with open(f"{FileName}.txt", "x") as file:
                        file.write(f'{AddressesOutput}\n')

        def NamesOutput():
            if len(APIOutputFiltered) == 0:
                print("No Names Found")

                if os.path.exists(f'{FileName}.txt'):
                    with open(f"{FileName}.txt", "a") as file:
                        file.write('No Names Found\n')
                else:
                    with open(f"{FileName}.txt", "x") as file:
                        file.write('No Names Found\n')
            else:
                for x in Replace:
                    NamesOutput = ("Names Found: " + str(APIOutputFiltered).replace("[", "")
                                   .replace("]", "").replace(x,"").replace("'", ""))

                print(NamesOutput)



                if os.path.exists(f'{FileName}.txt'):
                    with open(f"{FileName}.txt", "a") as file:
                        file.write(f'{NamesOutput}\n')

                else:
                    with open(f"{FileName}.txt", "x") as file:
                        file.write(f'{NamesOutput}\n')



        PhoneNumbersOutput()
        EmailsOutput()
        AddressesOutput()
        NamesOutput()
    Outputs()

if __name__ == '__main__':
    main()

# WebParse 1.1.1

# NotABird
# CEO of Bird Inc.
