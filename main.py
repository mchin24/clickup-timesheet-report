import requests
import json
import os
import dotenv
from google import genai
from google.genai import types

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

    open('output.json', 'w').write(json.dumps(tasks))
    print('data saved')

    # Send the result to AI engine
    ai_messages = "Please provide an executive summary for this employee's recent task history.\n\n" + json.dumps(tasks)
    ai_client = genai.Client()
    system_prompt = '''
    You are a successful executive offering advice to a small startup. They are willing to provide you any information 
    to enable you to offer relevant advice on achieving their goals of running a successful company. They are
    inexperienced and will benefit from your foresight. They may need help understanding terminology or justifications
    for your advice. You should be able to site evidence from real-world sources. Do not ever make up information to
    provide an answer. Always draw from real-world knowledge available to you. If there is information that you lack,
    be honest about the lack of information. Ask for more information if you need it.
    '''

    try:
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents= ai_messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            )
        )
        print(response.candidates[0].content.parts[0].text)
    except Exception as e:
        print("Error during content generation: " + e.message)


if __name__ == "__main__":
    main()