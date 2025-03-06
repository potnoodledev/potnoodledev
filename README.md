# Evolve the Game

A top-down action survival game built with Phaser 3.

## Game Description

"Evolve the Game" is a top-down action survival game where the player must survive for 10 minutes against progressively stronger waves of enemies. The player starts with a rock weapon that automatically targets and attacks the nearest enemy. As the player defeats enemies, they drop crystals that can be collected to gain XP and level up, improving the player's stats and weapon.

## Controls

- **Keyboard**: Use WASD keys to move the player character.
- **Mouse/Touch**: Drag anywhere on the screen to create a virtual joystick. The player will move in the direction you drag away from the initial touch point.

## Game Features

- **Automatic Weapon**: The player's rock weapon automatically targets and attacks the nearest enemy.
- **Leveling System**: Collect crystals from defeated enemies to gain XP and level up.
- **Progressive Difficulty**: Enemy waves become stronger over time, with more enemies and increased stats.
- **Timer**: Survive for 10 minutes to win the game.
- **Procedurally Generated Assets**: Game assets are generated using AI through the asset_generator module.
- **AI Agents**: Specialized AI agents can modify the game based on user requests.

## Project Structure

- **src/**: Main game source code
  - **assets/**: Game assets (images, audio, etc.)
  - **scenes/**: Phaser scenes (Boot, Game, UI, GameOver)
  - **scripts/**: Utility scripts for fetching comments and other tasks
  - **index.js**: Main game initialization
  - **index.html**: HTML entry point

- **asset_generator/**: Python-based tool for generating game assets using AI
  - See the [Asset Generator README](asset_generator/README.md) for details

- **game_studio/**: Central command hub for AI agents to modify the game
  - See the [Game Studio README](game_studio/README.md) for details
  - See the [AI Agents README](game_studio/README_AGENTS.md) for details on the agent system

## Development

### Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Python 3.7+ (for asset generation)
- Anthropic API key (for AI agents)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/evolve-the-game.git
   cd evolve-the-game
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. For asset generation, install Python dependencies:
   ```bash
   cd asset_generator
   pip install -r requirements.txt
   cd ..
   ```

4. For AI agents, install additional Python dependencies:
   ```bash
   pip install anthropic requests
   ```

5. Set up environment variables:
   ```bash
   # Create .env file in the root directory
   echo "PIXELLAB_API_TOKEN=your_pixellab_token_here" > .env
   echo "ANTHROPIC_API_KEY=your_anthropic_key_here" >> .env
   ```

### Running the Game

Start the development server:
```bash
npm start
```

Open your browser and navigate to `http://localhost:8080`

### Available NPM Scripts

The following npm scripts are available for development and deployment:

```bash
# Start development server
npm start

# Build for production
npm run build

# Deploy to itch.io (requires Butler)
npm run deploy

# Fetch comments from itch.io
npm run fetch-comments

# Fetch comments with advanced options
npm run fetch-comments-advanced
```

### Generating Assets

The game includes a powerful asset generation system. All asset generation commands should be run from the project root directory.

#### Using the Game Studio (Recommended for AI Agents)

The Game Studio provides a unified interface for all game operations:

```bash
# Generate player character
python game_studio/evolve.py generate-character --description "warrior with sword and shield"

# Generate enemy
python game_studio/evolve.py generate-enemy --type "zombie" --variations 3

# Generate item
python game_studio/evolve.py generate-item --description "crystal gem with magical glow" --name "crystal"

# Run the game
python game_studio/evolve.py run
```

See the [Game Studio README](game_studio/README.md) for complete documentation.

#### Using Asset Generator Directly

You can also use the asset generator scripts directly:

```bash
# Generate player character
python asset_generator/generate_character.py --description "warrior with sword and shield"

# Generate enemy
python asset_generator/generate_enemy.py --type "zombie" --variations 3

# Generate item
python asset_generator/generate_item.py --description "crystal gem with magical glow" --name "crystal"

# Generate weapon with projectile
python asset_generator/generate_weapon_with_projectile.py --weapon "throwing axe" --projectile "axe" --weapon-name "axe"

# Generate terrain tiles
python asset_generator/generate_tiles.py --terrain "grass" --output-dir "src/assets/images/tiles"

# Generate tile list JavaScript file
node asset_generator/generate_tile_list.js
```

For detailed documentation on all asset generation options, see the [Asset Generator README](asset_generator/README.md).

### Using AI Agents

The game includes a powerful AI agent system that can modify the game based on user requests. The system consists of:

1. **Game Developer Agent**: Makes changes to existing game code
2. **Artist Agent**: Generates game assets using evolve.py commands
3. **Agent Coordinator**: Orchestrates the work between the two agents

To use the AI agents:

```bash
# Process a user request
python game_studio/agent_coordinator.py "I wish there was a flaming axe in the game"

# With explicit API key
python game_studio/agent_coordinator.py "Add a zombie enemy that moves slowly but is hard to kill" --api-key your_api_key_here
```

Example requests you can try:
- "I wish there was a flaming axe in the game"
- "Add a zombie enemy that moves slowly but is hard to kill"
- "Create a health potion that restores 50 health points"
- "Add a desert terrain with cactus obstacles"

For detailed documentation on the AI agent system, see the [AI Agents README](game_studio/README_AGENTS.md).

### Building for Production

To build the game for production:

```bash
npm run build
```

The built files will be in the `dist` directory.

### Deployment

To deploy the game to itch.io (requires Butler):

```bash
npm run deploy
```

## AI-Powered Character Evolution

This project includes an AI-powered character evolution system that automatically improves your game character based on GitHub commits. Each time the specified GitHub user (potnoodledev) makes new commits, the character evolves to become more powerful and visually distinctive.

### How It Works

1. The system checks for new commits by potnoodledev
2. Every 3 commits triggers a character evolution
3. Claude AI generates a creative, improved character description
4. The asset generator creates new character sprites and animations
5. The game automatically uses the new character when restarted

### Using the Evolution System

```bash
# Start the continuous evolution system (checks hourly)
npm run evolve-character

# Manually trigger an evolution check
npm run check-evolution
```

For more details, see the [Character Evolution README](src/scripts/README_EVOLUTION.md).

## Technologies Used

- [Phaser 3](https://phaser.io/phaser3) - HTML5 game framework
- [Webpack](https://webpack.js.org/) - Module bundler
- [Python](https://www.python.org/) - For asset generation
- [PixelLab API](https://pixellab.ai/) - AI-powered pixel art generation
- [Anthropic Claude API](https://www.anthropic.com/) - For terrain generation and AI agents

## License

This project is licensed under the ISC License.

## Test Evolution
Testing character evolution with this commit - [timestamp: ${new Date().toISOString()}]
Testing another evolution trigger 