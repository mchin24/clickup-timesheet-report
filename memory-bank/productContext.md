# Product Context

## Problem Statement
Organizations using ClickUp for time tracking need a way to:
- Generate weekly status reports without manual data compilation
- Provide executive-level summaries without getting lost in task details
- Track project progress across multiple tasks and team members
- Identify issues and next steps quickly

## Solution
An automated tool that bridges ClickUp time tracking data with AI-powered analysis to produce executive-ready weekly reports.

## How It Works

### User Workflow
1. User runs the script (`python main.py`)
2. Script automatically calculates previous week's date range
3. Data is fetched from ClickUp API
4. AI analyzes the data and generates a summary
5. Two outputs are created:
   - `output.json`: Raw data for reference
   - `report.md`: Executive summary in Markdown

### Key Benefits
- **Time Savings**: No manual data compilation or report writing
- **Consistency**: Same format and structure every week
- **Context-Aware**: AI considers full comment history while focusing on recent updates
- **Actionable**: Reports include next steps and advisory sections
- **Ready to Share**: Markdown format easily converts to any needed format

## User Experience Goals
- **Zero Configuration**: After initial setup, just run the script
- **Reliable**: Accurate date calculations and complete data retrieval
- **Insightful**: AI provides meaningful analysis, not just data regurgitation
- **Professional**: Report quality suitable for executive stakeholders

## Report Structure
Each generated report includes:
- **Task Summaries**: For each active task
  - Task name
  - Progress summary
  - Next steps for upcoming week
- **Advisory Section**: Executive feedback on team performance and project handling
- **Contextual Information**: Proper date formatting and timezone handling

## Design Principles
1. **Automation First**: Minimize manual intervention
2. **Context Matters**: Full history provides AI with complete picture
3. **Focus on Action**: Reports drive decisions, not just inform
4. **Executive-Level**: High-level insights, not technical details
5. **Honest Assessment**: AI instructed to highlight issues, not sugarcoat