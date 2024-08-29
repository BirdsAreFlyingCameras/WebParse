# WebParse

## About

**Version Number: Beta 1.0**

WebParse is a command-line tool that retrieves names, addresses, phone numbers, and emails from a given URL and outputs
them in a human-friendly format to the command line, with an option to save the results in a text file.
WebParse extensively uses regex to retrieve the desired information from raw HTML. Due to the use of regex,
WebParse is imperfect and mainly relies on text being matched by a regex pattern (this does not apply to names).
It is much more difficult to retrieve names because regex is not effective for name retrieval. To retrieve names,
WebParse makes use of word lists containing over 800,000 words across all of them, sorted into categories to determine
if a string is a name. A drawback of this approach is that the error rate is determined by the quality of the word lists
and the methods used to filter a string against the word list content, which can lead to false positives.
This is particularly challenging if the word lists don't have the necessary content to provide an effective filter.



## Installation

**In the terminal of your choice:**

**Install files from GitHub:**

    git clone https://github.com/BirdsAreFlyingCameras/WebParse

**Travel to the path of installation:**

    cd [Path to script]

**Then install the requirements:**

    pip install -r requirements.txt


## Usage

**In the terminal of your choice:**


**Travel to the path of installation:**

    cd [Path to script]

**Then to run the script:**

    python3 main.py

![WebParseDemo.gif](images%2FWebParseDemo.gif)