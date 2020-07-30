import requests
import csv
import logging
import getpass
import datetime

do_csv = input('input csv: ')
updated_do_csv = input('output csv: ')

aspace_url = 'https://aspace-staff.fivecolleges.edu/api'
username = getpass.getuser()
# getuser() checks the environment variables LOGNAME, USER, LNAME and USERNAME, in order, and returns the value of the first non-empty string.
password = getpass.getpass(prompt='input password: ')
datetime = datetime.datetime.now()
datetime_formatted = datetime.strftime("%Y%b%d-%H%M%S")

auth = requests.post(aspace_url + '/users/' + username + '/login?password=' + password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session}
logging.basicConfig(filename=(f'do_creation_error_{datetime_formatted}.log'), level=logging.DEBUG)


def create_do():
    dig_obj = {
        'title': do_title,
        'digital_object_id': digital_object_identifier,
        'file_versions': [{'file_uri': file_uri, 'use_statement': file_version_use_statement}]
    }

    try:
        dig_obj_post = requests.post(aspace_url + '/repositories/2/digital_objects', headers=headers, json=dig_obj).json()
        print(f'Successful update for {do_title}')
        dig_obj_uri = dig_obj_post['uri']
        print('Digital Object URI: ', dig_obj_uri)
        writer.writerow([digital_object_identifier, dig_obj_uri, do_title])
    except Exception:
        print(f'Failed update for {do_title}')

    if publish_true_false == "TRUE":
        print(f"Publishing {dig_obj_uri}")
        try:
            requests.post(aspace_url + dig_obj_uri + '/publish', headers=headers)
        except Exception:
            print(f"Failed to publish {dig_obj_uri}")


with open(do_csv, newline="") as csvfile, open(updated_do_csv, mode='a') as csvout:
    reader = csv.DictReader(csvfile)
    writer = csv.writer(csvout)
    for row in reader:

        digital_object_identifier = row['do_id']
        file_uri = row['file_uri']
        file_version_use_statement = row['use_statement']
        do_title = row['do_title']
        publish_true_false = row['publish']
        create_do()
