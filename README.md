# State Population Analyzer
I have created 2 scripts that download compressed JSON files from an FTP server, processes them to extract state-wise population data, and prints the total population of each state in alphabetical order.

The files are:
1. AnkuraAssignment.py
2. AnkuraAssignment-multithreading.py
    - Reads data from files using threads

## Dependencies
- Python 3.6 or higher
- ftplib, gzip, and json standard libraries

## Usage
1. Open a terminal in the project directory.
2.  Run ```python AnkuraAssignment.py```.
3.  Run ```python AnkuraAssignment-multithreading.py```.

## Design Decisions and Assumptions
The script follows these design decisions and assumptions:

- It assumes that the FTP server is accessible at the `FTP_HOST` URL and requires username and password authentication.
- It assumes that the JSON files are compressed using gzip.
- It uses the `ftplib` library to connect to the FTP server, download the files, and read them.
- It uses the `gzip` and `json` libraries to extract the data from the compressed JSON files.
- It uses a dictionary to track state as key and population as the value.
- No need to track name of geographic region. If this needed then I would create a class that takes geographic region name, state, and population as instance variables.
- It prints the total population of each state in alphabetical order to the console.
- It logs debug-level messages to the console to indicate the progress of the script.
- It handles FTP errors and exceptions using the `ftplib.all_errors` class.
- For `AnkuraAssignment-multithreading.py` the script downloads and processes files concurrently using a ThreadPoolExecutor with a maximum of 3 workers. Workers can be modified depending on available processors.