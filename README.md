# Evolve the Game

A dynamic game project featuring an AI-powered character that evolves based on your GitHub commits.

## Core Feature: AI Character Evolution

The heart of this project is its unique character evolution system that automatically improves your game character based on your GitHub activity. Every three commits you make, your character evolves to become more visually distinctive, powered by Claude AI.

### How Character Evolution Works

1. **Real-Time Commit Detection**: The system continuously monitors your GitHub activity for new commits
2. **Evolution Trigger**: Every three commits triggers a character evolution
3. **AI-Powered Design**: Claude AI generates creative, improved character descriptions
4. **Automated Asset Generation**: The system automatically creates new character sprites based on the AI's description
5. **Immediate Updates**: The game instantly reflects your new character design

### Character Evolution Components

- **GitHub Integration**: Monitors commits in real-time using the GitHub API
- **Claude AI Integration**: Generates creative character improvements
- **Asset Generation**: Converts AI descriptions into pixel art sprites
- **State Management**: Tracks evolution progress in `commit-history.json`

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- Python 3.7+ (for asset generation)
- GitHub Personal Access Token
- Anthropic API Key (for Claude AI)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/evolve-the-game.git
   cd evolve-the-game
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   # Create .env file with your tokens
   GITHUB_TOKEN=your_github_token_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

### Running the Evolution System

Start the character evolution system:
```bash
npm run evolve-character
```

The system will:
- Immediately check for any unprocessed commits
- Continue checking periodically (default: every hour)
- Generate new character designs for each commit
- Update the game assets automatically

You can customize the check interval:
```bash
# Example: Check every 30 minutes
COMMIT_CHECK_INTERVAL_MINUTES=30 npm run evolve-character
```

### Available Scripts

```bash
# Start the evolution system
npm run evolve-character

# Manually check evolution status
npm run check-evolution

# Generate a new character manually
npm run generate-character

# Reset evolution history
npm run reset-evolution

# Copy commit history to assets
npm run copy-history
```

## Project Structure

```
├── src/
│   ├── assets/            # Game assets and commit history
│   ├── scripts/          
│   │   └── character-evolution.js  # Core evolution logic
│   └── scenes/           # Game scenes
├── asset_generator/      # Python-based sprite generation
├── evolve-character.js   # Evolution system entry point
├── check-evolution.js    # Manual evolution checker
├── generate-character.js # Manual character generator
└── commit-history.json   # Evolution state tracking
```

## How to Trigger Evolution

1. Make commits to your GitHub repository
2. The system will detect new commits automatically
3. After every three commits:
   - Claude AI generates an improved character description
   - The asset generator creates new sprites
   - The character evolves with new features
4. The evolution history is tracked in `commit-history.json`

## Technologies Used

- [GitHub API](https://docs.github.com/en/rest) - Commit tracking
- [Claude AI](https://www.anthropic.com/) - Character design generation
- [Node.js](https://nodejs.org/) - Runtime environment
- [Python](https://www.python.org/) - Asset generation

## License

This project is licensed under the ISC License.

## Contributing

Feel free to submit issues and enhancement requests! 