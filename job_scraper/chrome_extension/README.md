# Job Page Saver Chrome Extension

A Chrome extension that saves job pages to your local database.

## Features

- Save the current page you're viewing
- Or enter a custom URL to save
- Captures the full HTML content of the page
- Saves directly to your job_page database table

## Setup Instructions

### 1. Install Dependencies

Make sure FastAPI and uvicorn are installed:

```bash
uv add fastapi uvicorn pydantic
```

### 2. Start the API Server

Start the FastAPI server that the extension will communicate with:

```bash
uv run python -m src.hoarder.api_server
```

The server will run at `http://localhost:8000`

### 3. Load the Extension in Chrome

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in the top right)
3. Click "Load unpacked"
4. Select the `chrome_extension` directory from this project
5. The extension should now appear in your extensions list

### 4. Add Extension Icons (Optional)

The extension requires icons to display properly. Create or add these icon files to the `chrome_extension` directory:

- `icon16.png` (16x16px)
- `icon48.png` (48x48px)
- `icon128.png` (128x128px)

Or remove the icon references from `manifest.json` if you don't want icons.

## Usage

1. Navigate to a job posting page in Chrome
2. Click the extension icon in your browser toolbar
3. Either:
   - Leave the URL field blank to save the current page
   - Or enter a different URL to fetch and save that page
4. Click "Save Job Page"
5. You'll see a success message with the Page ID

## Configuration

To change the API endpoint, edit the `API_URL` variable in `popup.js`:

```javascript
const API_URL = 'http://localhost:8000/api/job-page';
```

## Database

The extension saves data to the `job_page` table with:
- `page_id`: Auto-incrementing primary key
- `url`: The URL of the job page
- `page_html`: The full HTML content of the page

## Troubleshooting

### CORS Errors

If you see CORS errors, make sure the API server is running and the CORS middleware is properly configured in `api_server.py`.

### Extension Not Working

1. Check the browser console for errors (right-click extension icon → "Inspect popup")
2. Verify the API server is running at `http://localhost:8000`
3. Test the API directly: `curl http://localhost:8000/`

### Database Errors

Make sure your database is initialized:

```bash
alembic upgrade head
```
