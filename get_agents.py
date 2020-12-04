import requests
import csv
import logging
import getpass
import datetime

# This python3 script generates a csv report of person agents in ArchivesSpace.
# To do: add argparse options for corporate, family, personal agents

aspace_url = "https://aspace-staff.fivecolleges.edu/api"
username = getpass.getuser()
# getuser() checks the environment variables LOGNAME, USER, LNAME and USERNAME, in order, and returns the value of the first non-empty string.
password = getpass.getpass(prompt='input password: ')
datetime = datetime.datetime.now()
datetime_formatted = datetime.strftime("%Y%b%d-%H%M%S")
csvfile = input('csv filename: ')

auth = requests.post(aspace_url + '/users/' + username +
                     '/login?password=' + password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session}
logging.basicConfig(
    filename=(f'agent_request_error_{datetime_formatted}.log'), level=logging.DEBUG)

agent_request = requests.get(
    "https://aspace-staff.fivecolleges.edu/api/agents/people?page=1&page_size=250").json()
num_pages = agent_request['last_page']
agents = []
for page in range(1, num_pages + 1):

    r_agent_request = requests.get(
        "https://aspace-staff.fivecolleges.edu/api/agents/people", params={'page': page, 'page_size': 250}).json()
    for agent in r_agent_request['results']:
        agent_row = []
        agent_row.append(agent['publish'])
        agent_row.append(agent['uri'])
        agent_row.append(agent['is_linked_to_published_record'])
        agent_row.append(agent['title'])
        names = agent['names'][0]
        agent_row.append(names.get('primary_name', 'NULL'))
        agent_row.append(names.get('title', 'NULL'))
        agent_row.append(names.get('prefix', 'NULL'))
        agent_row.append(names.get('rest_of_name', 'NULL'))
        agent_row.append(names.get('suffix', 'NULL'))
        agent_row.append(names.get('fuller_form', 'NULL'))
        agent_row.append(names.get('number', 'NULL'))
        agent_row.append(names.get('dates', 'NULL'))
        agent_row.append(names.get('sort_name', 'NULL'))
        agent_row.append(names.get('source', 'NULL'))
        agent_row.append(names.get('rules', 'NULL'))
        agent_row.append(names.get('name_order', 'NULL'))
        agent_row.append(names.get('authority_id', 'NULL'))
        agent_row.append(agent['created_by'])
        agent_row.append(agent['last_modified_by'])
        agents.append(agent_row)

csv_header = ['publish', 'uri', 'is_linked_to_published_record', 'full_name_aka_title', 'primary_name', 'title', 'prefix', 'rest_of_name',
              'suffix', 'fuller_form', 'number', 'dates', 'sort_name', 'source', 'rules', 'name_order', 'authority_id', 'created_by', 'last_modified_by']


with open(csvfile, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(csv_header)
    writer.writerows(agents)
