import requests
import json
from tabula import read_pdf
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


# def upload_assignments(page_amount: int, assignment_data: dict):
#     create_url = 'https://api.notion.com/v1/pages'
#
#     for k in range(page_amount):
#         assignment_data["properties"]["AssignmentName"]["title"][0]["text"]["content"] = "Assignment" + str(k)
#         assig_name = assignment_data["properties"]["AssignmentName"]["title"][0]["text"]["content"]
#
#         payload = json.dumps(assignment_data)
#
#         res = requests.request("POST", create_url, headers=headers, data=payload)
#         status_code = res.status_code
#
#         if status_code == 200:
#             print("Upload status code for", assig_name, ":", status_code, "--> SUCCESS")
#         elif status_code == 400:
#             print("Upload status code for", assig_name, ":", status_code, "--> FAILED")


# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
pdf_path = "sp23_Narrative_and_Technology_1.pdf"
main_df = read_pdf(pdf_path, pages="all")


week_one = []
week_two = []
week_three = []
week_four = []

counter = 0
for mini_df in main_df:
    if counter == 0 or counter == 1:
        counter += 1
        continue
    if counter > 5:
        break
    for i in range(len(mini_df.index)):
        data = mini_df.iloc[i].to_string()
        data = data.split(' ')
        if data[1] == "1":
            week_one.append(data[12:])
            # print(data[12:])
        elif data[1] == "2":
            week_two.append(data[11:])
            # print(data[11:])
        elif data[1] == "3":
            week_three.append(data[12:])
            # print(data[12:])
        elif data[1] == "4":
            week_four.append(data[12:])
            # print(data[12:])
    counter += 1


def print_assignments(week_number: list):
    for i in range(len(week_number)):
        if week_number[i][0] == "M" or week_number[i][0] == "W" or week_number[i][0] == "F":
            print(week_number[i])
            if i + 1 < len(week_number):
                print(week_number[i + 1])
                print(week_number[i + 2])
    print("------------------------")


def extract_info(week_number: list) -> list:
    week_assignments = []
    for i in range(len(week_number)):
        if week_number[i][0] == "M" or week_number[i][0] == "W" or week_number[i][0] == "F":
            week_assignments.append(week_number[i])
            # if i + 1 < len(week_number):
            #     week_assignments.append(week_number[i+1])
            #     week_assignments.append(week_number[i+2])
    return week_assignments


week_one_assignments = extract_info(week_one)
week_two_assignments = extract_info(week_two)
week_three_assignments = extract_info(week_three)
week_four_assignments = extract_info(week_four)


def package_assignments(assignment_list: list):
    for i in range(len(assignment_list)):
        month = assignment_list[i][1].split('/')[0]
        if len(month) == 1:
            month = "0" + month

        day = assignment_list[i][1].split('/')[1]
        if len(day) == 1:
            day = "0" + day

        temp = assignment_list[i][2:]
        assignment = ' '.join(temp)
        date = "2023-" + month + "-" + day

        curr = [assignment, date]
        demo.append(curr)


demo = []
package_assignments(week_one_assignments)
package_assignments(week_two_assignments)
package_assignments(week_three_assignments)
package_assignments(week_four_assignments)

for i in demo:
    print(i)
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------


# Creating a basic assignment entry for our notion database
# ------------------------------------------------------------------------
due_at = "11:59pm"
start_date = "2023-02-09"
status_box = False
task_type = "Homework"
course = "CS0001"
assignment_name = "DEMO ASSIGNMENT"
# ------------------------------------------------------------------------


def upload_EVERYTHING(due_at: str, status_box: bool, task_type: str, course: str, week_assignment: list):
    create_url = 'https://api.notion.com/v1/pages'

    for i in week_assignment:
        data = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Due At": {"rich_text": [{"text": {"content": due_at}}]},
                "Date": {"date": {"start": i[1], "end": None, "time_zone": None}},
                "Status": {"checkbox": status_box},
                "Task": {"rich_text": [{"text": {"content": task_type}}]},
                "Course": {"rich_text": [{"text": {"content": course}}]},
                "AssignmentName": {"title": [{"text": {"content": i[0]}}]}
            }
        }
        payload = json.dumps(data)

        res = requests.request("POST", create_url, headers=headers, data=payload)
        status_code = res.status_code

        if status_code == 200:
            print("Upload status code for", i[0], ":", status_code, "--> SUCCESS")
        elif status_code == 400:
            print("Upload status code for", i[0], ":", status_code, "--> FAILED")


upload_EVERYTHING(due_at, status_box, task_type, course, demo)


































