# Game Asset Generator

This tool generates pixel art assets for the Evolve game, saving them directly to the game's asset folders.

## Features

- Generate player character sprites and animations
- Generate enemy sprites and animations
- Generate item sprites
- Generate weapon sprites with projectiles
- Generate terrain tiles with variations
- Assets are saved directly to the game's src/assets/images directory structure
- Animations are saved as individual frames in the appropriate folders

## Requirements

- Python 3.7+
- PixelLab API token (set as environment variable `PIXELLAB_API_TOKEN`)
- Anthropic API token (set as environment variable `ANTHROPIC_API_KEY`) for terrain generation

## Installation

1. Install the required Python packages:
   ```bash
   # From the project root
   cd asset_generator
   pip install -r requirements.txt
   cd ..
   
   # Or directly from the asset_generator directory
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   # Create .env file in the root directory
   echo "PIXELLAB_API_TOKEN=your_pixellab_token_here" > .env
   echo "ANTHROPIC_API_KEY=your_anthropic_key_here" >> .env
   ```

## Command Reference

Below is a complete reference of all available commands with their parameters:

### Generate a player character

```bash
# Basic usage
python asset_generator/generate_character.py --description "warrior with sword and shield"

# With animation frames
python asset_generator/generate_character.py --description "warrior with sword and shield" --animation

# With custom dimensions
python asset_generator/generate_character.py --description "warrior with sword and shield" --width 64 --height 64

# With specific seed for reproducibility
python asset_generator/generate_character.py --description "warrior with sword and shield" --seed 12345

# Full options
python asset_generator/generate_character.py --description "warrior with sword and shield" --animation --width 64 --height 64 --seed 12345 --output-dir "src/assets/images/player" --token "your_pixellab_token"
```

**Parameters:**
- `--description` (required): Text description of the character
- `--animation` (optional): Generate walk animation frames
- `--width` (optional): Width of the sprite in pixels (default: 64)
- `--height` (optional): Height of the sprite in pixels (default: 64)
- `--seed` (optional): Seed for reproducible generation
- `--output-dir` (optional): Custom output directory
- `--token` (optional): PixelLab API token (overrides environment variable)

### Generate an enemy

```bash
# Basic usage
python asset_generator/generate_enemy.py --type "zombie"

# With animation frames
python asset_generator/generate_enemy.py --type "zombie" --animation

# With multiple variations
python asset_generator/generate_enemy.py --type "zombie" --variations 3

# With custom dimensions
python asset_generator/generate_enemy.py --type "zombie" --width 64 --height 64

# Full options
python asset_generator/generate_enemy.py --type "zombie" --animation --variations 3 --width 64 --height 64 --seed 67890 --output-dir "src/assets/images/enemies" --token "your_pixellab_token"
```

**Parameters:**
- `--type` (required): Type of enemy to generate
- `--animation` (optional): Generate walk animation frames
- `--variations` (optional): Number of variations to generate (default: 1)
- `--width` (optional): Width of the sprite in pixels (default: 64)
- `--height` (optional): Height of the sprite in pixels (default: 64)
- `--seed` (optional): Seed for reproducible generation
- `--output-dir` (optional): Custom output directory
- `--token` (optional): PixelLab API token (overrides environment variable)

### Generate an item

```bash
# Basic usage
python asset_generator/generate_item.py --description "crystal gem with magical glow" --name "crystal"

# With multiple variations
python asset_generator/generate_item.py --description "crystal gem with magical glow" --name "crystal" --variations 3

# With custom dimensions
python asset_generator/generate_item.py --description "crystal gem with magical glow" --name "crystal" --width 32 --height 32

# Full options
python asset_generator/generate_item.py --description "crystal gem with magical glow" --name "crystal" --variations 3 --width 32 --height 32 --seed 54321 --output-dir "src/assets/images/items" --token "your_pixellab_token"
```

**Parameters:**
- `--description` (required): Text description of the item
- `--name` (required): Name of the item (used for filename)
- `--variations` (optional): Number of variations to generate (default: 1)
- `--width` (optional): Width of the sprite in pixels (default: 32)
- `--height` (optional): Height of the sprite in pixels (default: 32)
- `--seed` (optional): Seed for reproducible generation
- `--output-dir` (optional): Custom output directory
- `--token` (optional): PixelLab API token (overrides environment variable)

### Generate a weapon with projectile

```bash
# Basic usage
python asset_generator/generate_weapon_with_projectile.py --weapon "throwing axe" --weapon-name "axe"

# With specific projectile
python asset_generator/generate_weapon_with_projectile.py --weapon "throwing axe" --projectile "axe" --weapon-name "axe"

# With custom dimensions
python asset_generator/generate_weapon_with_projectile.py --weapon "throwing axe" --weapon-name "axe" --weapon-width 48 --weapon-height 48 --projectile-width 24 --projectile-height 24

# Full options
python asset_generator/generate_weapon_with_projectile.py --weapon "throwing axe" --projectile "axe" --weapon-name "axe" --weapon-width 48 --weapon-height 48 --projectile-width 24 --projectile-height 24 --seed 13579 --output-dir "src/assets/images/weapons" --token "your_pixellab_token"
```

**Parameters:**
- `--weapon` (required): Text description of the weapon
- `--weapon-name` (required): Name of the weapon (used for filename)
- `--projectile` (optional): Text description of the projectile (if not specified, will be determined based on weapon type)
- `--weapon-width` (optional): Width of the weapon sprite in pixels (default: 48)
- `--weapon-height` (optional): Height of the weapon sprite in pixels (default: 48)
- `--projectile-width` (optional): Width of the projectile sprite in pixels (default: 24)
- `--projectile-height` (optional): Height of the projectile sprite in pixels (default: 24)
- `--seed` (optional): Seed for reproducible generation
- `--output-dir` (optional): Custom output directory
- `--token` (optional): PixelLab API token (overrides environment variable)

### Generate Terrain Tiles

```bash
# Basic usage
python asset_generator/generate_tiles.py --terrain "grass"

# With custom output directory
python asset_generator/generate_tiles.py --terrain "grass" --output-dir "src/assets/images/tiles"

# With specific number of variations
python asset_generator/generate_tiles.py --terrain "grass" --variations 5

# With custom dimensions
python asset_generator/generate_tiles.py --terrain "grass" --width 64 --height 64

# Full options
python asset_generator/generate_tiles.py --terrain "grass" --variations 3 --width 64 --height 64 --seed 24680 --output-dir "src/assets/images/tiles" --token "your_pixellab_token" --anthropic-token "your_anthropic_token"
```

**Parameters:**
- `--terrain` (required): Type of terrain to generate (e.g., grass, dungeon, lava, water, desert, snow, forest, cave, crystal, metal)
- `--variations` (optional): Number of variations to generate (default: 3)
- `--width` (optional): Width of the tile in pixels (default: 64)
- `--height` (optional): Height of the tile in pixels (default: 64)
- `--seed` (optional): Seed for reproducible generation
- `--output-dir` (optional): Custom output directory (default: src/assets/images/tiles)
- `--token` (optional): PixelLab API token (overrides environment variable)
- `--anthropic-token` (optional): Anthropic API token (overrides environment variable)

### Generate Tile List

```bash
# Basic usage
node asset_generator/generate_tile_list.js

# With custom input directory
node asset_generator/generate_tile_list.js --input-dir "src/assets/images/tiles"

# With custom output file
node asset_generator/generate_tile_list.js --output-file "src/assets/tileList.js"

# Full options
node asset_generator/generate_tile_list.js --input-dir "src/assets/images/tiles" --output-file "src/assets/tileList.js"
```

**Parameters:**
- `--input-dir` (optional): Directory containing tile images (default: src/assets/images/tiles)
- `--output-file` (optional): Output JavaScript file path (default: src/assets/tileList.js)

## Examples

Generate a wizard character with animations:
```bash
python asset_generator/generate_character.py --description "wizard with staff and magical robes" --animation --seed 12345
```

Generate a skeleton enemy with animations:
```bash
python asset_generator/generate_enemy.py --type "skeleton warrior with sword" --animation --seed 67890
```

Generate a magic staff with magic orb projectile:
```bash
python asset_generator/generate_weapon_with_projectile.py --weapon "magic staff with glowing runes" --weapon-name "staff" --seed 54321
```

Generate lava terrain tiles:
```bash
python asset_generator/generate_tiles.py --terrain "lava with bubbling magma" --seed 24680
```

## Advanced Usage

### Using the Python API

You can also use the asset generator as a Python module in your own scripts:

```python
from asset_generator import game_asset_generator

# Generate a character
game_asset_generator.generate_character_set(
    description="warrior with axe",
    animation=True,
    width=64,
    height=64,
    seed=12345,
    output_dir="src/assets/images/player"
)

# Generate an enemy
game_asset_generator.generate_enemy_set(
    enemy_type="goblin archer",
    animation=True,
    variations=3,
    width=64,
    height=64,
    seed=67890,
    output_dir="src/assets/images/enemies"
)

# Generate a weapon with projectile
game_asset_generator.generate_weapon_with_projectile(
    weapon_description="bow",
    projectile_description="arrow",
    weapon_name="bow",
    weapon_width=48,
    weapon_height=48,
    projectile_width=24,
    projectile_height=24,
    seed=54321,
    output_dir="src/assets/images/weapons"
)

# Generate terrain tiles
from asset_generator.generate_tiles import generate_terrain_tiles
generate_terrain_tiles(
    terrain_type="desert sand",
    variations=3,
    width=64,
    height=64,
    seed=24680,
    output_dir="src/assets/images/tiles"
)
```

## Integration with the Game

The assets are saved directly to the game's asset folders, so they will be automatically used by the game when it loads. The game's BootScene loads these assets during startup.

## Troubleshooting

If you encounter issues with the asset generator, try the following:

1. Check that your API tokens are correctly set in the `.env` file
2. Ensure you have installed all required dependencies with `pip install -r requirements.txt`
3. Make sure the output directories exist and are writable
4. Try running with a specific seed value to reproduce and debug issues 