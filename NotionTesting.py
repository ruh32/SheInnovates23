import requests
import json
# from datetime import datetime, timezone
# import jsonpickle
# from json import JSONEncoder


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


def upload_single_assignment(new_page_data):
    create_url = 'https://api.notion.com/v1/pages'

    payload = json.dumps(new_page_data)
    res = requests.request("POST", create_url, headers=headers, data=payload)

    status_code = res.status_code

    if status_code == 200:
        print("Upload Status Code:", status_code, "--> SUCCESS")
    elif status_code == 400:
        print("Upload Status Code:", status_code, "--> FAILED")

    # print(res.text)


def upload_assignments(page_amount: int, assignment_data: dict):
    create_url = 'https://api.notion.com/v1/pages'

    for k in range(page_amount):
        assignment_data["properties"]["AssignmentName"]["title"][0]["text"]["content"] = "Assignment" + str(k)
        assig_name = assignment_data["properties"]["AssignmentName"]["title"][0]["text"]["content"]

        payload = json.dumps(assignment_data)

        res = requests.request("POST", create_url, headers=headers, data=payload)
        status_code = res.status_code

        if status_code == 200:
            print("Upload status code for", assig_name, ":", status_code, "--> SUCCESS")
        elif status_code == 400:
            print("Upload status code for", assig_name, ":", status_code, "--> SUCCESS")


# Creating a basic assignment entry for our notion database
# ------------------------------------------------------------------------
due_at = "9:00pm"
start_date = "2023-02-08"
status_box = False
task_type = "Homework"
course = "CS0001"
assignment_name = "DEMO ASSIGNMENT"

data = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Due At": {"rich_text": [{"text": {"content": due_at}}]},
        "Date": {"date": {"start": start_date, "end": None, "time_zone": None}},
        "Status": {"checkbox": status_box},
        "Task": {"rich_text": [{"text": {"content": task_type}}]},
        "Course": {"rich_text": [{"text": {"content": course}}]},
        "AssignmentName": {"title": [{"text": {"content": assignment_name}}]}
    }
}
# ------------------------------------------------------------------------

upload_assignments(2, data)

























