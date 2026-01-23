import requests
import json
import os
import dotenv

def main():
    dotenv.load_dotenv()
    CLICKUP_API_KEY = os.environ['CLICKUP_API_KEY']
    GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

    # First, we need a list of authorized workspaces
    url = "https://api.clickup.com/api/v2/team"
    headers = {"authorization": CLICKUP_API_KEY, "accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed retrieving workspaces with status code: " + str(response.status_code))

    workspaces = response.json()
    if len(workspaces['teams']) > 1:
        for available_team in workspaces['teams']:
            if available_team['name'] == "Sharpen":
                team = available_team
    else:
        team = workspaces['teams'][0]

    # Now we can get timesheet data
    url = f"https://api.clickup.com/api/v2/team/{team['id']}/time_entries"

    headers = {
        "authorization": CLICKUP_API_KEY,
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed retrieving timesheets with status code: " + str(response.status_code))

    time_entries = response.json()['data']
    tasks = {}
    for entry in time_entries:
        task_id = entry['task']['id']
        if task_id not in tasks:
            tasks[task_id] = {"id": task_id, "time_entries": []}
        tasks[task_id]["time_entries"].append(entry)

    for task in tasks:
        url = f"https://api.clickup.com/api/v2/task/{task}/?include_subtasks=true"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("Failed retrieving tasks with status code: " + str(response.status_code))
        task_data = response.json()
        tasks[task]['name'] = task_data['name']

        url = f"https://api.clickup.com/api/v2/task/{task}/comment"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("Failed retrieving tasks with status code: " + str(response.status_code))
        comments = response.json()
        tasks[task]['comments'] = comments

        # Are there subtasks?
        tasks[task]['subtasks'] = {}
        for subtask in task_data['subtasks']:
            subtask_id = subtask['id']
            if subtask_id not in tasks[task]['subtasks']:
                tasks[task]['subtasks'][subtask_id] = subtask

            # Get subtask comments
            url = f"https://api.clickup.com/api/v2/task/{subtask_id}/comment"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception("Failed retrieving tasks with status code: " + str(response.status_code))
            comments = response.json()
            tasks[task]['subtasks'][subtask_id]['comments'] = comments

    open('task.json', 'w').write(json.dumps(tasks))
    print('data saved')

if __name__ == "__main__":
    main()