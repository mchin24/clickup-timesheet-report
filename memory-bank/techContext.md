# Technical Context

## Technology Stack

### Core Language
- **Python 3.7+**: Main implementation language
- **Standard Library Modules**:
  - `datetime`, `timedelta`: Date calculations
  - `json`: Data serialization
  - `os`: Environment variable access

### Dependencies
Listed in `requirements.txt`:
1. **requests**: HTTP client for ClickUp API calls
2. **python-dotenv**: Environment variable management from `.env` file
3. **google-genai**: Google Gemini AI integration

### External Services
1. **ClickUp API v2**:
   - Base URL: `https://api.clickup.com/api/v2/`
   - Authentication: API key via `authorization` header
   - Endpoints used:
     - `/team` - Get workspaces
     - `/team/{team_id}/time_entries` - Get time entries with date filters
     - `/task/{task_id}` - Get task details with subtasks
     - `/task/{task_id}/comment` - Get task comments

2. **Google Gemini API**:
   - Model: `gemini-3-flash-preview`
   - Authentication: API key
   - Features used: Content generation with system instructions

## Development Setup

### Environment Variables (.env)
```env
CLICKUP_API_KEY=pk_***
GEMINI_API_KEY=***
```

### Installation
```bash
pip install -r requirements.txt
```

### Running the Script
```bash
python main.py
```

## API Integration Details

### ClickUp API Patterns

**Authentication Header**:
```python
headers = {
    "authorization": CLICKUP_API_KEY,
    "accept": "application/json",
    "Content-Type": "application/json"
}
```

**Date Filtering**:
- Parameters: `start_date` and `end_date`
- Format: Unix timestamp in milliseconds
- Example: `?start_date=1707609600000&end_date=1708214399000`

**Response Handling**:
- All responses checked for `status_code != 200`
- Exceptions thrown with descriptive messages
- JSON parsing with `.json()` method

### Gemini AI Integration

**Client Setup**:
```python
ai_client = genai.Client()  # Uses GEMINI_API_KEY from environment
```

**Generation Config**:
```python
config = types.GenerateContentConfig(
    system_instruction=system_prompt
)
```

**Usage Metadata**:
- Available in `response.usage_metadata`
- Printed for monitoring API usage

## File I/O

### Output Files
1. **output.json**:
   - Raw task data dump
   - Written with `open('output.json', 'w').write(json.dumps(tasks))`
   - UTF-8 encoding (default)

2. **report.md**:
   - AI-generated Markdown report
   - Written with `open('report.md', 'w').write(response_text)`
   - UTF-8 encoding (default)

## Technical Constraints

### Date/Time Handling
- Currently uses naive datetime (no timezone awareness)
- System timezone assumed
- **Known Issue**: Should use `zoneinfo.ZoneInfo("America/New_York")` for proper Eastern Time

### API Rate Limits
- No rate limiting implemented
- No retry logic for failed requests
- Could hit rate limits with large task sets

### Error Recovery
- Fail-fast approach
- No graceful degradation
- All API failures stop execution

## Performance Considerations

### API Call Volume
For N tasks with M subtasks each:
- 1 workspace list call
- 1 time entries call
- N task detail calls
- N comment calls
- N×M subtask comment calls

**Total**: 2 + N + (N × M) calls

### Memory Usage
- Entire dataset held in memory
- No streaming or pagination
- Could be problematic for very large workspaces

## Development Tools

### IDE
- IntelliJ IDEA Ultimate (based on .idea directory)
- Python plugin configured

### Version Control
- Git repository
- Remote: https://github.com/mchin24/clickup-timesheet-report.git

### Python Environment
- Virtual environment (`venv/` directory)
- Isolated dependency management

## Future Technical Enhancements

### High Priority
1. **Timezone Awareness**: Use `zoneinfo` for proper Eastern Time handling
2. **Error Retry**: Implement exponential backoff for API failures
3. **Configuration**: Make workspace name configurable

### Medium Priority
1. **Logging**: Add proper logging instead of print statements
2. **Rate Limiting**: Implement request throttling
3. **Pagination**: Handle large result sets

### Low Priority
1. **Caching**: Cache task/comment data to reduce API calls
2. **Parallel Requests**: Use async/await for concurrent API calls
3. **Testing**: Add unit tests for date calculations and data processing