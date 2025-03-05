# Itch.io Comments Fetcher

This tool allows you to fetch the latest comments from your game's itch.io page.

## Prerequisites

- Node.js (v14 or higher recommended)
- npm (comes with Node.js)

## Installation

Make sure you have installed the required dependencies:

```bash
npm install
```

This will install the necessary packages (axios and cheerio) defined in the project's package.json.

## Usage

### Basic Command Line

You can run the basic comment fetcher directly from the command line:

```bash
# Format
npm run fetch-comments -- <username> <game-name> [limit]

# Example: Fetch 5 latest comments from potnoodledev/evolve
npm run fetch-comments -- potnoodledev evolve 5
```

Parameters:
- `username`: Your itch.io username
- `game-name`: The name of your game as it appears in the URL
- `limit` (optional): Maximum number of comments to retrieve (default: 10)

### Advanced Command Line

The advanced comment fetcher provides more options and can save comments to a file:

```bash
# Format
npm run fetch-comments-advanced -- <username> <game-name> [options]

# Example: Fetch comments and save to a file
npm run fetch-comments-advanced -- potnoodledev evolve --limit=10 --output=./data/comments.json

# Example: Only show new comments since last check
npm run fetch-comments-advanced -- potnoodledev evolve --notify-only-new --format=text
```

Advanced options:
- `--limit=<number>`: Maximum number of comments to retrieve (default: 20)
- `--output=<file-path>`: Path to save comments (default: ./comments.json)
- `--notify-only-new`: Only display new comments since last check
- `--format=<json|text>`: Output format (default: json)

### Programmatic Usage

You can also use the comment fetcher in your own scripts:

```javascript
const { fetchItchComments } = require('./itchCommentsFetcher');

// Example: Fetch 5 latest comments
fetchItchComments('potnoodledev', 'evolve', 5)
  .then(comments => {
    console.log('Latest comments:', comments);
    // Do something with the comments
  })
  .catch(error => {
    console.error('Error fetching comments:', error);
  });
```

## Comment Object Structure

Each comment is returned as an object with the following properties:

```javascript
{
  author: "Username",
  date: "3 days ago",
  text: "This is the comment text..."
}
```

## Setting Up Automated Comment Checking

You can set up a cron job or scheduled task to automatically check for new comments:

### On Linux/macOS (using cron)

1. Open your crontab:
   ```bash
   crontab -e
   ```

2. Add a line to run the script every hour:
   ```
   0 * * * * cd /path/to/your/project && npm run fetch-comments-advanced -- potnoodledev evolve --notify-only-new --output=/path/to/save/comments.json
   ```

### On Windows (using Task Scheduler)

1. Create a batch file (check-comments.bat):
   ```batch
   cd /path/to/your/project
   npm run fetch-comments-advanced -- potnoodledev evolve --notify-only-new --output=C:\path\to\save\comments.json
   ```

2. Open Task Scheduler and create a new task to run this batch file on your desired schedule.

## Limitations

- This tool uses web scraping, so it may break if itch.io changes their page structure.
- Be respectful of itch.io's servers and avoid making too many requests in a short period.
- This tool only fetches public comments visible on the game page.

## Troubleshooting

If you encounter issues:

1. Verify that your game has a public comments section enabled on itch.io
2. Check that you're using the correct username and game name
3. Make sure you have an active internet connection
4. If the structure seems to have changed, check the HTML structure of your game's page and update the selectors in `itchCommentsFetcher.js` 