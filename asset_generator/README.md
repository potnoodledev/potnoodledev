# Game Asset Generator

This tool generates pixel art assets for the Evolve game, saving them directly to the game's asset folders.

## Features

- Generate player character sprites and animations
- Generate enemy sprites and animations
- Generate item sprites
- Generate weapon sprites with projectiles
- Assets are saved directly to the game's src/assets/images directory structure
- Animations are saved as individual frames in the appropriate folders

## Requirements

- Python 3.7+
- PixelLab API token (set as environment variable `PIXELLAB_API_TOKEN`)

## Usage

### Generate a player character

```bash
./generate_character.py --description "warrior with sword and shield"
```

This will:
1. Generate a main player sprite at `src/assets/images/player.png`

To also generate walk animation frames:

```bash
./generate_character.py --description "warrior with sword and shield" --animation
```

This will:
1. Generate a main player sprite at `src/assets/images/player.png`
2. Generate walk animation frames at `src/assets/images/player/walk/frame_1.png`, etc.

### Generate an enemy

```bash
./generate_enemy.py --type "zombie"
```

This will:
1. Generate a main enemy sprite at `src/assets/images/enemy.png`

To also generate walk animation frames:

```bash
./generate_enemy.py --type "zombie" --animation
```

This will:
1. Generate a main enemy sprite at `src/assets/images/enemy.png`
2. Generate walk animation frames at `src/assets/images/enemies/walk/frame_1.png`, etc.

To generate multiple enemy variations:

```bash
./generate_enemy.py --type "zombie" --variations 3
```

### Generate an item

```bash
./generate_item.py --description "crystal gem with magical glow" --name "crystal"
```

This will:
1. Generate an item sprite at `src/assets/images/items/crystal.png`

### Generate a weapon with projectile

Generate a weapon with its corresponding projectile:

```bash
./generate_weapon_with_projectile.py --weapon "throwing axe" --projectile "axe" --weapon-name "axe"
```

This will generate a weapon sprite at `src/assets/images/weapons/axe.png` and a projectile sprite at `src/assets/images/weapons/projectiles/axe.png`.

If you don't specify a projectile type, it will be automatically determined based on the weapon type:
- Bows will generate arrows
- Guns will generate bullets
- Wands/staffs will generate magic orbs
- Throwable weapons will use the weapon itself as the projectile

### Additional Options

- `--seed`: Specify a seed for reproducible generation
- `--token`: Provide a PixelLab API token (overrides environment variable)

## Examples

Generate a wizard character with animations:
```bash
./generate_character.py --description "wizard with staff and magical robes" --animation --seed 12345
```

Generate a skeleton enemy with animations:
```bash
./generate_enemy.py --type "skeleton warrior with sword" --animation --seed 67890
```

Generate a magic staff with magic orb projectile:
```bash
./generate_weapon_with_projectile.py --weapon "magic staff with glowing runes" --weapon-name "staff" --seed 54321
```

## Integration with the Game

The assets are saved directly to the game's asset folders, so they will be automatically used by the game when it loads. The game's BootScene loads these assets during startup. 