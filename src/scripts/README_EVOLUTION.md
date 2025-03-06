# AI-Powered Character Evolution System

This system automatically evolves your game character based on GitHub commits by a specific user (potnoodledev), using Claude AI to generate creative character improvements.

## How It Works

1. The system periodically checks for new commits by the specified GitHub user
2. When new commits are detected, it counts them toward character evolution
3. Every 3 commits triggers an evolution to the next character level
4. Claude AI generates a new, improved character description based on the current one
5. The asset generator creates a new character sprite and animations based on this description
6. The first frame of the walk animation is automatically used as the idle character sprite

## AI-Generated Character Evolution

Instead of using preset evolution stages, this system uses Claude AI to:

1. Analyze the current character description
2. Generate a new, improved description that builds upon the existing one
3. Make the character progressively more interesting, powerful, and visually distinctive
4. Maintain continuity between evolution stages while adding new elements
5. Ensure the character is always facing right for consistent animations

This creates a unique evolution path for your character that's different every time!

## Usage

### Running the Evolution System

To start the character evolution system that continuously checks for new commits:

```bash
npm run evolve-character
```

This will:
- Start a background process that checks for new commits every hour
- Log information about commit checks and character evolutions
- Continue running until manually stopped (Ctrl+C)

### Manual Evolution Check

To manually trigger a check for new commits and potential character evolution:

```bash
npm run check-evolution
```

This is useful for:
- Testing the system
- Forcing an immediate check without waiting for the hourly interval
- Debugging issues with the evolution process

## Configuration

You can modify the following settings in `src/scripts/character-evolution.js`:

- `GITHUB_USERNAME`: The GitHub username to monitor for commits (default: 'potnoodledev')
- `COMMIT_CHECK_INTERVAL`: How often to check for new commits (default: every hour)
- The Claude AI prompt to customize how character descriptions are generated

## Requirements

This system requires:
- An Anthropic API key for Claude AI (stored in your .env file as ANTHROPIC_API_KEY)
- Node.js with axios for API calls
- Python with the asset generator dependencies installed

## How Character Generation Works

When a character evolution is triggered:

1. The system uses Claude AI to generate an improved character description
2. It ensures the description specifies that the character is facing right
3. It calls the asset generator to create walk animation frames
4. The first frame of the walk animation is copied to be the idle character sprite
5. The game automatically uses the new character assets when restarted

This approach ensures:
- Consistent character orientation (always facing right)
- Visual consistency between the idle character and walk animation
- Smooth transitions between different character states

## Commit History

The system maintains a commit history file (`commit-history.json`) in the project root to track:

- The last checked commit SHA
- The current character description
- The current evolution level
- The total number of commits counted

This ensures that:
- The same commits aren't counted multiple times
- The character evolution state persists between system restarts
- The evolution progresses correctly over time

## Troubleshooting

If you encounter issues:

1. Check the console output for error messages
2. Verify that the GitHub API is accessible
3. Ensure your Anthropic API key is valid and properly set in the .env file
4. Check that the commit-history.json file exists and is valid JSON
5. Try running a manual check with `npm run check-evolution`

## Fallback Mechanism

If the Claude API is unavailable or returns an error, the system includes a fallback mechanism that will use predefined character descriptions to ensure the evolution can continue. These fallback descriptions also specify that the character is facing right.

## Extending the System

You can extend this system by:

- Adding more evolution stages
- Changing the number of commits required per evolution
- Modifying the character descriptions for different visual styles
- Adding additional effects or abilities that unlock with each evolution 