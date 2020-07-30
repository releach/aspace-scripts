import requests
import csv
import logging
import getpass
import datetime

ao_csv = input('input csv: ')

aspace_url = input('api url: ')
username = getpass.getuser()
# getuser() checks the environment variables LOGNAME, USER, LNAME and USERNAME, in order, and returns the value of the first non-empty string.
password = getpass.getpass(prompt='input password: ')
datetime = datetime.datetime.now()
datetime_formatted = datetime.strftime("%Y%b%d-%H%M%S")

auth = requests.post(aspace_url + '/users/' + username + '/login?password=' + password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session}
logging.basicConfig(filename=(f'ao_creation_error_{datetime_formatted}.log'), level=logging.DEBUG)


def post_ao():
    ao_dict = {}
    child_dict = {
        "external_ids": [],
        "subjects": [{"ref": "/subjects/" + subject}],
        "linked_events": [],
        "extents": [{"number": extent_number, "portion":
                    extent_portion, "extent_type": extent_type}],
        "dates": [],
        "external_documents": [],
        "rights_statements": [],
        "linked_agents": [],
        "is_slug_auto": True,
        "restrictions_apply": False,
        "publish": True,
        "ancestors": [],
        "instances": [{"instance_type": "digital_object", "digital_object":
                      {"ref": "/repositories/2/digital_objects/" + digital_object}}],
        "level": level,  # Required field, controlled value
        "lang_materials": [{"language_and_script": {"language": lang}}],
        "title": title,  # Required field
        "resource": {"ref": resource_uri}
    }
    notes = []
    if scopecontent_note != '':
        sn_notecontent = {"jsonmodel_type": "note_multipart", "type":
                          "scopecontent", "subnotes": [{"jsonmodel_type": "note_text",
                                                        "content": scopecontent_note, "publish": True}], "publish": True}
        notes.append(sn_notecontent)
        # child_dict["notes"] = notecontent
    if general_note != '':
        general_notecontent = {"jsonmodel_type": "note_multipart", "type":
                               "odd", "subnotes": [{"jsonmodel_type": "note_text",
                                                   "content": general_note, "publish": True}], "publish": True}
        notes.append(general_notecontent)

    child_dict["notes"] = notes
    array = []
    array.append(child_dict)
    ao_dict["children"] = array
    logging.debug(f"Debugging for {title}:")
    ao_post = requests.post(aspace_url + '/repositories/2' + archival_object_parent_uri + '/children', headers=headers, json=ao_dict).json()
    # print(ao_post)
    if 'status' in ao_post.keys():
        print(f"Archival object for {title} posted successfully")
    if 'error' in ao_post.keys():
        print(f"There was an error for {title}; check error log")


with open(ao_csv, newline="") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        archival_object_parent_uri = row['ao_uri']  # full path to ao, eg '/archival_objects/30886'

        title = row['title']
        level = row['level'].lower()  # use controlled values, eg item, series, file
        resource_uri = row['resource_uri']  # path to the resource eg '/repositories/2/resources/685'
        extent_number = row['extent_number']
        extent_portion = row['extent_portion'].lower()
        extent_type = row['extent_type'].lower()
        subject = row['genre']  # as id for the genre term
        lang = row['language']  # use language codes eg 'eng'
        digital_object = row['digital_object']  # as id for do
        scopecontent_note = row['scopecontent_note']
        general_note = row['general_note']
        post_ao()
