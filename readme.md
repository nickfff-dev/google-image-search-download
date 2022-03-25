this script takes a csv with  one column  that has the product title. the script searches google images for the right product image by comparing the product title string and the image alt attribute text, to find matches, and downloads  the image with the correct matches with the title as the image name.

install all the dependencies in a venv

    python -m venv env

    env/Scripts/Activate.ps1

    pip install selenium

    pip install wget

    pip install pandas

base64 is a standard built in lib for decoding the image data in base64 format so that it can be saved as a file.

mimetypes is a standard built in lib for detecting image extension in this case.

wget has to be downloaded from <a href="http://gnuwin32.sourceforge.net/packages/wget.htm"> here</a> and made available to PATH before you can pip install wget and use it in the script. <a href="https://phoenixnap.com/kb/wget-command-with-examples">find installation guide and adding to path here</a>

the script uses selenium and chrome driver(download the latest version of chromedriver that matches with your browser version) to run the search and wget to manage the downloads

to initialize add the csv with "title" column to the script folder

ensure you have a folder named "images" in the same folder as the script

ensure you have chromedriver in the same folder as the script

activate venv 

    env/Scripts/Activate.ps1

run the script

    python main.py
