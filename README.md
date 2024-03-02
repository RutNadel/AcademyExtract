# AcademyExtract

## תוכנה לחילוץ מידע מאתר האקדמיה עבור המילון העולמי

Welcome to my Python academy extract program!

### FEATURES

- **Get Dotted Word Information Table**: Retrieve information about the word as provided by the academy on the website.
- **Get All Existing Combinations**: Obtain all existing combinations as a new sheet.
- **Check if a Dotted Word is Suitable (Not Combinations)**: Check if a dotted word is suitable according to the academy's rules.
### פיצ'רים 

- **קבלת טבלת אינפורמציה עבור מילה מנוקדת**: קבלת אינפורמציה על המילה כפי שמספקת האקדמיה באתר.
- **קבלת כל הצירופים הקימים**: קבלת כל הצירופים הקימים כגליון חדש.
- **בדיקה האם מילה מנוקדת כיאות (לא צירופים)**: בדיקה האם מילה מנוקדת לפי כללי האקדמיה.

###Warnings
Download the source xl file from safe source,
Prefer not to use email messages (instead of you can get link to drive)
for it might change the right order

### Installation

To install and run this program, follow these steps:
0. install python (recommend v 3.12) and all the required packages:
    ```bash
    pip install <package>
    ```

    **packages requirements**
    * pandas
    * bs4
    * subprocess
    * openpyxl
    * aiohttp
    * pyarrow - even you don't import it
    
    for splitXI also:
    * xlsxwriter
   

1. Clone the repository:

    ```bash
    git clone https://github.com/RutNadel/AcademyExtract.git
    ```

2. Navigate to the project directory:

    ```bash
    cd .
    ```
3. Split big files (more than 12,000 rows) using SplitXL.py file,
   cnage before the next line:
   ```python
   input_file = '..\\xlSplitted\\H.xlsx'  # link to source file
   output_prefix = '..\\xlSplitted\\s'  # link to prefix and path to the output files
   ```
4. Change the parameters in "main.py" file

   ```python
   input_file_path = "..\\xl\\hebDict.xlsx"  # link for xl dict
   original_column = 'original'  # name of the dotted column in the xl dict. (sometimes it's another, e.g. 'Trns')
   only_is_dotted = False  # change to True if you want to get only the inforamtion if the word is dotted as needed (האם המילה מנוקדת כראוי לפי כללי האקדמיה. לא רלוונטי לצירופים)
   ```
5. Run the Python script:

    ```bash
    python main.py
    ```

### Usage

- **קבלת הטבלה**: תוכנה זו עוזרת לקבל מידע מאתר האקדמיה עבור מילים מנוקדות שנשלחות לאתר
