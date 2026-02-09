# Project Brief: ClickUp Timesheet Report

## Project Overview
A Python automation tool that generates AI-powered executive summary reports from ClickUp timesheet data.

## Core Purpose
Automate weekly reporting by:
1. Fetching ClickUp time entries for the previous week (Sunday-Saturday)
2. Collecting associated task data, comments, and subtasks
3. Using Google Gemini AI to generate executive-level project status summaries
4. Outputting actionable reports in Markdown format

## Key Requirements
- **Time Range**: Automatically calculate previous week (Sunday 00:00:00 to Saturday 23:59:59)
- **Data Collection**: Retrieve time entries, tasks, subtasks, and comment history
- **AI Analysis**: Generate concise, actionable summaries focused on project status
- **Timezone**: Handle Eastern Time (America/New_York) correctly
- **Output**: Generate both raw JSON data and formatted Markdown reports

## Target Users
- Executives needing weekly project status updates
- Team leads tracking progress across multiple tasks
- Stakeholders requiring high-level project summaries

## Success Criteria
- Accurate weekly time period calculation
- Complete task and comment data retrieval
- AI-generated reports that are concise and actionable
- Minimal manual intervention required

## Constraints
- Requires ClickUp API access
- Requires Google Gemini API access
- Python 3.7+ environment
- Designed for "Sharpen" workspace (configurable)