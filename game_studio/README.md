# Evolve Game Studio

A central command hub for AI agents to modify and interact with the Evolve game.

## Overview

The Evolve Game Studio provides a unified interface for AI agents to:

1. Generate game assets (characters, enemies, items, weapons, terrain)
2. Run the game and development server
3. Build and deploy the game
4. Fetch and analyze player comments

All commands are accessible through a single Python script (`evolve.py`), making it easy for AI agents to understand and modify the game.

## Usage

```bash
python game_studio/evolve.py <command> [options]
```

Or if you've made the script executable:

```bash
./game_studio/evolve.py <command> [options]
```

To see all available commands:

```bash
python game_studio/evolve.py --help
```

## Available Commands

### Asset Generation

#### Generate a Player Character

```bash
python game_studio/evolve.py generate-character --description "warrior with sword and shield"
```

Options:
- `--description` (required): Text description of the character
- `--animation`: Generate walk animation frames
- `--width`: Width of the sprite in pixels (default: 64)
- `--height`: Height of the sprite in pixels (default: 64)
- `--seed`: Seed for reproducible generation
- `--output-dir`: Custom output directory
- `--token`: PixelLab API token (overrides environment variable)

#### Generate an Enemy

```bash
python game_studio/evolve.py generate-enemy --type "zombie"
```

Options:
- `--type` (required): Type of enemy to generate
- `--animation`: Generate walk animation frames
- `--variations`: Number of variations to generate (default: 1)
- `--width`: Width of the sprite in pixels (default: 64)
- `--height`: Height of the sprite in pixels (default: 64)
- `--seed`: Seed for reproducible generation
- `--output-dir`: Custom output directory
- `--token`: PixelLab API token (overrides environment variable)

#### Generate an Item

```bash
python game_studio/evolve.py generate-item --description "crystal gem with magical glow" --name "crystal"
```

Options:
- `--description` (required): Text description of the item
- `--name` (required): Name of the item (used for filename)
- `--variations`: Number of variations to generate (default: 1)
- `--width`: Width of the sprite in pixels (default: 32)
- `--height`: Height of the sprite in pixels (default: 32)
- `--seed`: Seed for reproducible generation
- `--output-dir`: Custom output directory
- `--token`: PixelLab API token (overrides environment variable)

#### Generate a Weapon with Projectile

```bash
python game_studio/evolve.py generate-weapon --weapon "throwing axe" --weapon-name "axe"
```

Options:
- `--weapon` (required): Text description of the weapon
- `--weapon-name` (required): Name of the weapon (used for filename)
- `--projectile`: Text description of the projectile
- `--weapon-width`: Width of the weapon sprite in pixels (default: 48)
- `--weapon-height`: Height of the weapon sprite in pixels (default: 48)
- `--projectile-width`: Width of the projectile sprite in pixels (default: 24)
- `--projectile-height`: Height of the projectile sprite in pixels (default: 24)
- `--seed`: Seed for reproducible generation
- `--output-dir`: Custom output directory
- `--token`: PixelLab API token (overrides environment variable)

#### Generate Terrain Tiles

```bash
python game_studio/evolve.py generate-terrain --terrain "grass"
```

Options:
- `--terrain` (required): Type of terrain to generate
- `--variations`: Number of variations to generate (default: 3)
- `--width`: Width of the tile in pixels (default: 64)
- `--height`: Height of the tile in pixels (default: 64)
- `--seed`: Seed for reproducible generation
- `--output-dir`: Custom output directory
- `--token`: PixelLab API token (overrides environment variable)
- `--anthropic-token`: Anthropic API token (overrides environment variable)

#### Generate Tile List

```bash
python game_studio/evolve.py generate-tile-list
```

Options:
- `--input-dir`: Directory containing tile images (default: src/assets/images/tiles)
- `--output-file`: Output JavaScript file path (default: src/assets/tileList.js)

### Game Management

#### Run the Game

```bash
python game_studio/evolve.py run
```

Options:
- `--port`: Port to run the server on (default: 8080)
- `--open`: Open the game in a browser

#### Build the Game

```bash
python game_studio/evolve.py build
```

Options:
- `--mode`: Build mode (choices: "production", "development", default: "production")

#### Deploy the Game

```bash
python game_studio/evolve.py deploy
```

Options:
- `--skip-build`: Skip building the game before deployment

### Comment Fetching

#### Fetch Comments

```bash
python game_studio/evolve.py fetch-comments
```

Options:
- `--username`: itch.io username (default: "potnoodledev")
- `--game-name`: Game name on itch.io (default: "evolve")
- `--limit`: Maximum number of comments to retrieve (default: 10)
- `--advanced`: Use advanced comment fetcher
- `--output`: Path to save comments (for advanced fetcher)
- `--notify-only-new`: Only display new comments (for advanced fetcher)
- `--format`: Output format (choices: "json", "text", default: "json")

## Examples

### Generate a Wizard Character with Animations

```bash
python game_studio/evolve.py generate-character --description "wizard with staff and magical robes" --animation --seed 12345
```

### Generate Multiple Skeleton Enemy Variations

```bash
python game_studio/evolve.py generate-enemy --type "skeleton warrior with sword" --variations 3 --animation
```

### Generate a Magic Staff with Projectile

```bash
python game_studio/evolve.py generate-weapon --weapon "magic staff with glowing runes" --weapon-name "staff" --seed 54321
```

### Generate Lava Terrain Tiles

```bash
python game_studio/evolve.py generate-terrain --terrain "lava with bubbling magma" --seed 24680
```

### Run the Game on a Custom Port

```bash
python game_studio/evolve.py run --port 3000 --open
```

### Build and Deploy the Game

```bash
python game_studio/evolve.py deploy
```

### Fetch and Save New Comments

```bash
python game_studio/evolve.py fetch-comments --advanced --output "./comments.json" --notify-only-new --format "text"
```

## For AI Agents

This unified command interface is designed to make it easy for AI agents to modify and interact with the Evolve game. All commands follow a consistent pattern and provide helpful error messages.

When working with the game, AI agents should:

1. Use the `evolve.py` script for all game-related operations
2. Check command help for available options (`python game_studio/evolve.py <command> --help`)
3. Use the appropriate seed values for reproducible asset generation
4. Check command output for success/failure messages

## Implementation Details

The `evolve.py` script uses two approaches to execute commands:

1. **Direct Module Import**: If the asset generator modules are available, it imports and calls them directly
2. **Subprocess Execution**: As a fallback, it executes the appropriate scripts as subprocesses

This ensures that the script works even if the Python environment doesn't have all the required dependencies installed. 