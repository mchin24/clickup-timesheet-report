import requests
import json
import os
import dotenv
from google import genai
from google.genai import types
from datetime import datetime, timedelta

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

    # Calculate previous week's Sunday to Saturday
    today = datetime.now()
    days_since_sunday = (today.weekday() + 1) % 7  # Sunday = 0
    last_sunday = today - timedelta(days=days_since_sunday + 7)
    previous_sunday = last_sunday.replace(hour=0, minute=0, second=0, microsecond=0)
    previous_saturday = previous_sunday + timedelta(days=6, hours=23, minutes=59, seconds=59)

    # Convert to milliseconds (ClickUp API format)
    start_timestamp = int(previous_sunday.timestamp() * 1000)
    end_timestamp = int(previous_saturday.timestamp() * 1000)
    print(f"Report period: {previous_sunday} ({start_timestamp}) --> {previous_saturday} ({end_timestamp})")

    # Now we can get timesheet data
    url = f"https://api.clickup.com/api/v2/team/{team['id']}/time_entries?start_date={start_timestamp}&end_date={end_timestamp}"

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
    ai_messages = f'''Please provide an executive summary for this employee's recent task history. 
    The summary should be concise with no flowery language. Praise for noteworthy work is fine, but do not be overly
    effusive. The purpose of this summary is to provide an update on project status, not to measure employee performance.
    This is a high priority and high visibility project. It's important to provide accurate information and highlight
    any issues.
    
    For each task, the full comment history is included so you have context of the project's overall progress. For this
     summary, we're only concern with updates where the timestamp is between the timestamps {start_timestamp} and 
    {end_timestamp}. The timestamps are in Unix time as milliseconds. They should evaluate to {previous_sunday} and
    {previous_saturday}. This history is provided so you have context of the project's overall progress. Do not include 
    updates on projects that haven't been updated during the time period mentioned. Note that we are in the Eastern 
    timezone so please convert any dates that you mention appropriately.
    
    Each task summary should include the task name, a summarization of the progress, and next steps for the upcoming week.
    
    At the end of the report, include an advisory section. Use this section to provide feedback on the team's handling
    of the tasks and overall project.
    
    Generate the report in markdown, using UTF-8.
    ********
    {json.dumps(tasks)}
    '''
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
            model="gemini-3-flash-preview",
            contents= ai_messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt
            )
        )
        print(response.candidates[0].content.parts[0].text)
        open('report.md', 'w').write(response.candidates[0].content.parts[0].text)
        print(f"\n\n\n{response.usage_metadata}")
    except Exception as e:
        print("Error during content generation: " + e.message)


if __name__ == "__main__":
    main()