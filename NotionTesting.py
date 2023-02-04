import requests
from datetime import datetime, timezone
# ----------------------
import json
import jsonpickle
from json import JSONEncoder
# ----------------------


NOTION_TOKEN = "secret_6i4uDnuWACqoVTiBsteKaUAXJ5RBqh6ZANauN4DdpON"
DATABASE_ID = "e0df044e59764cd1b2b7c6bf02338146"


headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    payload = {'page size:', 100}
    response = requests.post(url, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    import json
    with open('db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    return results


def extract_data():
    pages = get_pages()
    number_of_assignments = len(pages)
    print("Number of Assignments:", number_of_assignments)
    print("------------")

    for i in range(0, number_of_assignments):
        attributes = pages[i]["properties"]
        due_at = attributes["Due At"]["rich_text"][0]["plain_text"]
        date = attributes["Date"]["date"]["start"]
        status = attributes["Status"]["checkbox"]
        task = attributes["Task"]["rich_text"][0]["plain_text"]
        course = attributes["Course"]["rich_text"][0]["plain_text"]
        assignment_name = attributes["AssignmentName"]["title"][0]["plain_text"]

        print_assignment_data(i, attributes, due_at, date, status, task, course, assignment_name)


def print_assignment_data(i: int, attributes: dict, due_at: str, date: str, status: bool, task: str, course: str, assignment: str):
    print(f"Data for #{i} assignment entry in our notion database:")
    print("Due At:", due_at)
    print("Date:", date)
    print("Is Task completed:", status)
    print("Type of Task:", task)
    print("Course:", course)
    print("Assignment:", assignment)
    print("--------------------------------------")


def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    encoded_payload = jsonpickle.encode(payload)

    res = requests.post(create_url, headers=headers, json=encoded_payload)
    print(res.status_code)
    return res






































