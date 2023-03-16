import ftplib
import gzip
import json
import logging

FTP_HOST = "interview.noragh.com"
USER = "interview"
PASS = "noragh"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s'
)

state_populations = {}  # dictionary to track state as key and population as the value


def read_files(filenames):
    results = {}
    for filename in filenames:
        with open(filename, 'wb') as file:
            logging.debug(f'Downloading {filename}')
            ftp_connection.retrbinary(f'RETR {filename}', file.write)

        logging.debug(f'Processing {filename}')
        with gzip.open(filename, 'rb') as f_in:
            for line in f_in:
                data = json.loads(line)
                state = data['state']
                population = data['population']
                results[state] = results.get(state,
                                             0) + population  # add population value to key if key is present. If not present then the get function adds 0 as value by default

    return results


try:
    with ftplib.FTP(FTP_HOST) as ftp_connection:  # handles closing of connection
        ftp_connection.login(USER, PASS)  # user and pwd can be stored in a config/utility file
        ftp_connection.encoding = "utf-8"
        logging.debug(ftp_connection.getwelcome())

        state_populations = read_files(ftp_connection.nlst())

        for state, population in sorted(state_populations.items(), key=lambda item: item[0]):  # sorting alphabetically, returns items in an iterable
            print(f'{state}:\t{population}')  # print state and population with tab
except ftplib.all_errors as e:
    logging.error(f'Failed to connect to FTP server: {e}')
