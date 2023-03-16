import ftplib
import gzip
import json
import concurrent.futures
import logging

FTP_HOST = "interview.noragh.com"
USER = "interview"
PASS = "noragh"

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(threadName)s - %(message)s",
)


def process_file(filename):
    with ftplib.FTP(FTP_HOST, timeout=120) as ftp_connection:  # each thread will connect to ftp server
        ftp_connection.login(USER, PASS)
        ftp_connection.encoding = "utf-8"
        ftp_connection.set_pasv(False)
        logging.debug(f'Downloading file {filename}')
        with open(filename, 'wb') as f:
            ftp_connection.retrbinary('RETR ' + filename, f.write)

        logging.debug(f'Processing file {filename}')
        with gzip.GzipFile(filename, 'rb') as f:  # unzip file to get to json objects
            contents = f.read().decode('utf-8')
            results = {}
            for line in contents.splitlines():
                data = json.loads(line)
                state = data['state']
                population = data['population']
                results[state] = results.get(state, 0) + population  # add state and population as key-value
    return results


try:
    with ftplib.FTP(FTP_HOST, timeout=60) as ftp_connection:
        ftp_connection.login(USER, PASS)  # user and pwd can be stored in a config/utility file
        ftp_connection.encoding = "utf-8"
        logging.debug(ftp_connection.getwelcome())

        filenames = ftp_connection.nlst()
        results = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(process_file, filename) for filename in filenames]

            for future in concurrent.futures.as_completed(futures):
                state_populations = future.result()
                for state, population in state_populations.items():
                    results[state] = results.get(state, 0) + population

        for state, population in sorted(results.items(), key=lambda item: item[
            0]):  # sorting alphabetically, returns items in an iterable
            print(f'{state}:\t{population}')  # print state and population with tab
except ftplib.all_errors as e:
    logging.error(f'Failed to connect to FTP server: {e}')
