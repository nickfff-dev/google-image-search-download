this script takes a csv with two columns: one column has the product title, and the other the product SKu. the script searches google images for the right product image by comparing the product title string and the image alt attribute text, to find matches, and downloads  the image with the correct matches then it renames the image with the corresponding SKU,

install all the dependencies in a venv

    python -m venv env

    env/Scripts/Activate.ps1

    pip install selenium

    pip install wget

    pip install pandas


mimetypes is a standard built in lib for detecting image extension in this case but wget has to be downloaded from <a href="http://gnuwin32.sourceforge.net/packages/wget.htm"> here</a> and made available to PATH before you can pip install wget and use it in the script <a href="https://phoenixnap.com/kb/wget-command-with-examples">find installation guide and adding to path here</a>

the script uses selenium and chrome driver(download the version of chromedriver that matches with your browser version ) to run the search and wget to manage the downloads

to initialize add the csv with "SellerSku" and "title" columns to the script folder
activate venv 

    env/Scripts/Activate.ps1

run the script

    python main.py
