# ClickUp Timesheet Report

A Python tool that retrieves ClickUp time entries and task data for the previous week (Sunday to Saturday) and generates an AI-powered executive summary report using Google Gemini.

## Features

- **Automated Weekly Reporting**: Automatically calculates and fetches data for the previous week (Sunday 00:00:00 to Saturday 23:59:59)
- **Comprehensive Data Collection**: Retrieves time entries, tasks, subtasks, and comment history from ClickUp
- **AI-Powered Summaries**: Uses Google Gemini to generate executive-level project status reports
- **Contextual Analysis**: Analyzes comment history while focusing on updates within the reporting period
- **Markdown Output**: Generates formatted reports ready for distribution

## Prerequisites

- Python 3.7+
- ClickUp API access
- Google Gemini API access

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   
   Create a `.env` file in the project root:
   ```env
   CLICKUP_API_KEY=your_clickup_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Obtain API Keys**
   - **ClickUp API Key**: Get from [ClickUp Settings > Apps](https://app.clickup.com/settings/apps)
   - **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Usage

Run the script to generate a report for the previous week:

```bash
python main.py
```

The script will:
1. Fetch your ClickUp workspaces (defaults to "Sharpen" if multiple exist)
2. Calculate the previous week's date range
3. Retrieve time entries and related task data
4. Generate an AI summary with project insights
5. Save outputs to `output.json` and `report.md`

## Output Files

- **`output.json`**: Raw data including tasks, time entries, comments, and subtasks
- **`report.md`**: AI-generated executive summary in Markdown format

## Report Structure

The generated report includes:
- **Task Summaries**: Name, progress summary, and next steps for each task
- **Advisory Section**: Executive feedback on team performance and project handling
- **Date Context**: All timestamps converted to Eastern timezone for clarity

## Technical Details

- **Language**: Python 3
- **APIs**: ClickUp API v2, Google Gemini API
- **Date Handling**: Automatic calculation of previous week (Sunday-Saturday)
- **Timezone**: Reports use Eastern Time (America/New_York)
- **AI Model**: gemini-3-flash-preview

## Notes

- The script focuses on the "Sharpen" workspace if multiple workspaces exist
- Time entries are filtered to the previous week's Sunday 00:00:00 - Saturday 23:59:59
- Comment history provides context but only updates within the reporting period are summarized
- The AI generates concise, actionable summaries focused on project status, not employee performance