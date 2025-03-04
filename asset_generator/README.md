# MCPTool - Pixel Art Generator

A Python package for generating pixel art images using the PixelLab API, with specialized support for creating game assets and terrain tiles.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/MCPTool.git
cd MCPTool
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your PixelLab API token:
```
PIXELLAB_API_TOKEN=your_api_token_here
```

## Usage

### Basic Pixel Art Generation

```python
from game_asset_generator import generate_pixel_art

# Generate a simple pixel art image and save it to a file
generate_pixel_art(
    description="cute dragon",
    width=128,
    height=128,
    output_path="dragon.png"
)

# Generate a pixel art image with more customization
generate_pixel_art(
    description="medieval castle on a hill",
    width=256,
    height=256,
    output_path="castle.png",
    outline="single color black outline",
    shading="detailed shading",
    detail="highly detailed",
    view="side",
    direction="north-east",
    no_background=True
)

# Generate a pixel art image and get the PIL Image object
image = generate_pixel_art(
    description="pixel art forest with animals",
    width=200,
    height=200,
    negative_description="humans, buildings",
    outline="selective outline",
    shading="medium shading"
)

# You can then manipulate the image using PIL
print("Image size:", image.size)
print("Image mode:", image.mode)

# Save the image with a different name
image.save("forest.png")

# You can also display the image
image.show()
```

### Game Asset Generation

The package includes specialized functions for generating game assets with consistent styling:

```python
from game_asset_generator import generate_game_asset, generate_character_set, generate_enemy_set, generate_weapon_set, generate_character_animation, generate_enemy_animation, generate_item

# Generate a single game asset
character = generate_game_asset(
    asset_type="character",  # Options: "character", "enemy", "weapon", "item", "environment", "effect"
    description="warrior with sword",
    output_path="warrior.png"
)

# Generate a character asset
character_path = generate_character_set(
    character_description="wizard with staff",
    output_dir="characters",
    seed=12345  # Optional: for reproducibility
)
print(f"Generated character asset: {character_path}")

# Generate character animations
animation_path = generate_character_animation(
    character_description="wizard with staff",
    action="walk",  # Can be any action: walk, run, attack, cast, idle, etc.
    direction="east",
    reference_image_path="characters/wizard_with_staff.png",  # Optional: use existing character as reference
    output_format="spritesheet",  # Options: "spritesheet", "gif", "frames"
    output_dir="characters",
    seed=12345  # Optional: for reproducibility
)
print(f"Generated animation: {animation_path}")

# Generate enemy variations
enemy_assets = generate_enemy_set(
    enemy_type="zombie",
    output_dir="enemies/zombie",
    count=3,  # Number of variations
    seed=67890  # Optional: for reproducibility
)

# Generate enemy animations
enemy_animation_path = generate_enemy_animation(
    enemy_type="zombie",
    action="attack",  # Can be any action: idle, attack, walk, etc.
    direction="east",
    reference_image_path="enemies/zombie/zombie_1.png",  # Optional: use existing enemy as reference
    output_format="spritesheet",  # Options: "spritesheet", "gif", "frames"
    output_dir="enemies/animations",
    seed=13579  # Optional: for reproducibility
)
print(f"Generated enemy animation: {enemy_animation_path}")

# Generate an item
item_path = generate_item(
    item_description="health potion with red liquid",
    output_dir="items",
    seed=11223  # Optional: for reproducibility
)
print(f"Generated item asset: {item_path}")

# Generate a weapon
weapon_path = generate_weapon_set(
    weapon_type="sword",
    output_dir="weapons/sword",
    seed=24680  # Optional: for reproducibility
)
print(f"Generated weapon asset: {weapon_path}")

# Generate a weapon with a detailed description
weapon_path = generate_weapon_set(
    weapon_type="dagger made of glowing sunbeams with golden light",
    output_dir="weapons/special",
    seed=42  # Optional: for reproducibility
)
print(f"Generated weapon asset: {weapon_path}")
```

### Terrain Tile Generation

The package includes a specialized script for generating seamless terrain tiles for games, including regular tiles, transitions, and corners.

#### Using the Tile Generator

The `create_tile.py` script provides a command-line interface for generating various types of terrain tiles:

```bash
# Generate a basic terrain tile
python create_tile.py grass

# Generate a transition tile between two terrain types
python create_tile.py sand --transition-to water --transition-direction left_to_right

# Generate a corner tile where two terrain types meet
python create_tile.py grass --transition-to water --corner-type top_right

# Use a specific seed for reproducibility
python create_tile.py grass --transition-to water --corner-type bottom_left --seed 12345

# Change the output directory
python create_tile.py grass --output-dir my_tiles

# Change the tile size (default is 32x32)
python create_tile.py grass --size 64
```

#### Tile Types

The tile generator supports various terrain types:

- `grass`: Green grass texture
- `sand`: Beige sand texture
- `water`: Blue water texture
- `stone`: Gray stone texture
- `dirt`: Brown dirt texture
- `snow`: White snow texture
- `lava`: Orange and red lava texture
- `wood`: Brown wood texture with grain
- `ice`: Light blue ice texture
- `mud`: Dark brown mud texture

You can also use any other terrain type not in this list, and the generator will create a suitable tile.

#### Transition Types

Transitions between terrain types can be generated in four directions:

- `left_to_right`: First terrain on the left, second on the right
- `right_to_left`: First terrain on the right, second on the left
- `top_to_bottom`: First terrain on the top, second on the bottom
- `bottom_to_top`: First terrain on the bottom, second on the top

#### Corner Types

Corner tiles create square L-shaped corners where two terrain types meet:

- `top_left`: Second terrain in the top left corner
- `top_right`: Second terrain in the top right corner
- `bottom_left`: Second terrain in the bottom left corner
- `bottom_right`: Second terrain in the bottom right corner

All corner tiles feature a clear, hard-edged boundary with a thin border between terrain types, perfect for creating terrain features like ponds, lakes, beaches, and more.

#### Example: Creating a Complete Pond

To create a complete pond, you would need:

1. Regular grass tiles for the surrounding area
2. Regular water tiles for the center of the pond
3. Four corner tiles for the corners of the pond
4. Transition tiles for the straight edges of the pond

```bash
# Generate the regular tiles
python create_tile.py grass
python create_tile.py water

# Generate the corner tiles
python create_tile.py grass --transition-to water --corner-type top_left
python create_tile.py grass --transition-to water --corner-type top_right
python create_tile.py grass --transition-to water --corner-type bottom_left
python create_tile.py grass --transition-to water --corner-type bottom_right

# Generate the transition tiles
python create_tile.py grass --transition-to water --transition-direction top_to_bottom
python create_tile.py grass --transition-to water --transition-direction bottom_to_top
python create_tile.py grass --transition-to water --transition-direction left_to_right
python create_tile.py grass --transition-to water --transition-direction right_to_left
```

These tiles can then be arranged in your game to create a seamless pond with proper corners and transitions.

### Advanced Features

#### Using an Initial Image

```python
import base64
from io import BytesIO
from PIL import Image

# Load an existing image
initial_image = Image.open("existing_image.png")

# Convert to base64
buffered = BytesIO()
initial_image.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

# Generate a new image based on the initial image
modified_image = generate_pixel_art(
    description="dragon with wings",
    width=initial_image.width,
    height=initial_image.height,
    init_image={"type": "base64", "base64": img_str},
    init_image_strength=300,  # Controls how much influence the initial image has (1-999)
    output_path="modified_dragon.png"
)
```

#### Transparent Backgrounds

All game assets are generated with transparent backgrounds by default, making them ready to use in game engines and design tools. This is especially important for:

```python
# Generate a weapon with guaranteed transparent background
weapon_path = generate_weapon_set(
    weapon_type="magical staff with glowing blue runes",
    output_dir="weapons",
    seed=42
)

# You can also explicitly set the transparent background when using generate_game_asset
magical_weapon = generate_game_asset(
    asset_type="weapon",
    description="magical staff with glowing blue runes",
    output_path="weapons/magical_staff.png",
    no_background=True  # Explicitly ensure transparent background
)
```

When using the command line:

```bash
# The weapon-set command always uses transparent backgrounds
python game_asset_generator.py weapon-set --type "dagger made of sunbeams" --output-dir weapons

# For other assets, you can use the --no-background flag
python game_asset_generator.py generate --description "magical effect" --width 64 --height 64 --no-background --output effects/magic.png
```

#### Using a Color Palette

```python
# Create or load an image with your desired color palette
palette_image = Image.open("my_palette.png")

# Convert to base64
buffered = BytesIO()
palette_image.save(buffered, format="PNG")
palette_str = base64.b64encode(buffered.getvalue()).decode()

# Generate an image using this color palette
styled_image = generate_pixel_art(
    description="medieval castle",
    width=128,
    height=128,
    color_image={"type": "base64", "base64": palette_str},
    output_path="styled_castle.png"
)
```

#### Controlling Text Guidance

```python
# Generate an image with strict adherence to the description
precise_image = generate_pixel_art(
    description="red dragon with blue wings breathing fire",
    width=128,
    height=128,
    text_guidance_scale=15,  # Higher value = follow description more closely (1-20)
    output_path="precise_dragon.png"
)
```

### Using the Command Line Interface

The package provides several command-line interfaces for different tasks:

#### Basic Pixel Art Generation

```bash
python game_asset_generator.py generate --description "cute dragon" --width 128 --height 128 --output dragon.png
```

#### Game Asset Generation

```bash
# Generate a single game asset
python game_asset_generator.py asset --type character --description "warrior with sword" --output warrior.png

# Generate a character asset
python game_asset_generator.py character-set --description "wizard with staff" --output-dir characters

# Generate character animations
python game_asset_generator.py character-animation --description "wizard with staff" --action "walk" --direction "east" --format "spritesheet" --reference "characters/wizard_with_staff.png"

# Generate animation frames for game development
python game_asset_generator.py character-animation --description "wizard with staff" --action "attack" --direction "east" --format "frames" --reference "characters/wizard_with_staff.png"

# Generate animated GIF
python game_asset_generator.py character-animation --description "wizard with staff" --action "idle" --direction "east" --format "gif" --reference "characters/wizard_with_staff.png"

# Generate enemy variations
python game_asset_generator.py enemy-set --type zombie --output-dir enemies/zombie --count 3

# Generate enemy animations
python game_asset_generator.py enemy-animation --type "zombie" --action "attack" --direction "east" --format "spritesheet" --reference "enemies/zombie/zombie_1.png"

# Generate enemy animation frames for game development
python game_asset_generator.py enemy-animation --type "skeleton" --action "walk" --direction "east" --format "frames"

# Generate a weapon
python game_asset_generator.py weapon-set --type sword --output-dir weapons/sword

# Generate a weapon with a detailed description
python game_asset_generator.py weapon-set --type "ice sword with frost effects" --output-dir weapons/special

# Generate an item
python game_asset_generator.py item --description "health potion with red liquid" --output-dir items
```

For more options:

```bash
python game_asset_generator.py --help
python game_asset_generator.py generate --help
python game_asset_generator.py asset --help
python game_asset_generator.py character-set --help
python game_asset_generator.py character-animation --help
python game_asset_generator.py enemy-set --help
python game_asset_generator.py weapon-set --help
python game_asset_generator.py item --help
```

### Utility Scripts

The package includes several utility scripts for generating assets:

```bash
# Generate a few test assets
python test_assets.py

# Run examples of how to use and modify the generated assets
python example_game_assets.py

# Generate a complete set of game assets (character, animation, enemy, item, and weapon)
python create_game_assets.py

# Generate terrain tiles for your game
python create_tile.py grass
```

#### Using create_game_assets.py

The `create_game_assets.py` script provides a convenient way to generate a complete set of game assets in one go. The script runs in interactive mode, prompting you for descriptions of each asset:

```bash
# Run the script to generate all assets interactively
python create_game_assets.py
```

The script first collects all your asset descriptions and then generates everything at once:

1. First, it collects all your inputs:
   - Asks if you want to use a specific seed for reproducibility
   - Prompts you to describe your character
   - Asks what action and direction the character animation should use
   - Asks which output format you want for the character animation (spritesheet, gif, or frames)
   - Prompts you to describe your enemy
   - Asks what action and direction the enemy animation should use
   - Asks which output format you want for the enemy animation (spritesheet, gif, or frames)
   - Prompts you to describe your item
   - Prompts you to describe your weapon

2. Then, it generates all assets based on your descriptions:
   - Character
   - Character animation
   - Enemy
   - Enemy animation
   - Item
   - Weapon

This approach allows you to provide all your creative input upfront and then let the script handle the generation process without interruption. The script also includes error handling to continue generating assets even if some fail due to API issues.

Example interaction:
```
===== GAME ASSET GENERATOR =====
This script will help you create a set of game assets.
You'll be prompted to describe each asset, and then all assets will be generated at once.
All assets will be created with transparent backgrounds for game use.

----- COLLECTING ASSET DESCRIPTIONS -----

Do you want to use a specific seed for reproducibility? (yes/no): no

Using seed: 42913

1. CHARACTER
Describe your character (e.g., 'wizard with blue robes and a magical staff'): archer with green hood and a longbow

2. CHARACTER ANIMATION
What action should the character perform? (e.g., walk, run, attack, cast, idle): attack
In which direction? (e.g., north, east, south, west): east
Choose animation output format (spritesheet/gif/frames): gif

3. ENEMY
Describe your enemy (e.g., 'goblin with a small dagger, green skin'): skeleton warrior with a rusty sword

4. ENEMY ANIMATION
What action should the enemy perform? (e.g., idle, attack, walk): attack
In which direction? (e.g., north, east, south, west): west
Choose animation output format (spritesheet/gif/frames): gif

5. ITEM
Describe your item (e.g., 'ancient magic scroll with glowing runes'): healing potion with red liquid

6. WEAPON
Describe your weapon (e.g., 'enchanted sword with blue glowing runes on the blade'): golden bow with magical arrows

----- GENERATING ASSETS -----

1. Generating character...
Character generated: characters/archer_with_green_hood_and_a_longbow,_pixel_art_style.png

2. Generating character animation...
Character animation generated: characters/archer_with_green_hood_and_a_longbow_attack_east.gif

3. Generating enemy...
Enemy generated: enemies/skeleton_warrior_with_a_rusty_sword_1.png

4. Generating enemy animation...
Enemy animation generated: enemies/skeleton_warrior_with_a_rusty_sword_attack_west.gif

5. Generating item...
Item generated: items/healing_potion_with_red_liquid,_pixel_art_style.png

6. Generating weapon...
Weapon generated: weapons/golden_bow_with_magical_arrows.png

===== GENERATION SUMMARY =====
Successfully generated 6 out of 6 assets:
1. Character: characters/archer_with_green_hood_and_a_longbow,_pixel_art_style.png
2. Character Animation: characters/archer_with_green_hood_and_a_longbow_attack_east.gif
3. Enemy: enemies/skeleton_warrior_with_a_rusty_sword_1.png
4. Enemy Animation: enemies/skeleton_warrior_with_a_rusty_sword_attack_west.gif
5. Item: items/healing_potion_with_red_liquid,_pixel_art_style.png
6. Weapon: weapons/golden_bow_with_magical_arrows.png
```

#### Using create_tile.py

The `create_tile.py` script provides a convenient way to generate terrain tiles for your game. See the [Terrain Tile Generation](#terrain-tile-generation) section for detailed usage instructions.

## Game Asset Features

The game asset generation functions are specifically designed for creating assets for games like Vampire Survivors, with:

- **Transparent backgrounds** for all assets
- **Consistent pixel art styling** across all assets
- **Appropriate sizes** for each asset type:
  - Characters: 64×64 pixels
  - Enemies: 64×64 pixels
  - Weapons: 48×48 pixels
  - Items: 32×32 pixels
  - Environment: 128×128 pixels
  - Effects: 64×64 pixels
- **Character assets** with idle pose
- **Character animations** with various actions (walk, run, attack, cast, idle, etc.)
- **Animation output formats**:
  - Spritesheets: Single PNG with all frames side by side
  - GIFs: Animated GIF files for previewing
  - Individual frames: Separate PNG files for each animation frame
- **Enemy variations** with normal, larger, and elite versions
- **Enemy animations** with various actions (idle, attack, walk, etc.) in the same formats as character animations
- **Weapons** with detailed descriptions and guaranteed transparent backgrounds
- **Items** with detailed descriptions and guaranteed transparent backgrounds
- **Consistent styling** for each asset type:
  - Characters: Single color black outline, medium shading, medium detail, side view
  - Enemies: Single color black outline, medium shading, medium detail, side view
  - Weapons: Single color black outline, basic shading, medium detail, side view
  - Items: Single color black outline, basic shading, low detail, side view
  - Environment: Selective outline, medium shading, medium detail, low top-down view
  - Effects: Lineless, basic shading, low detail

## General Features

- Generate pixel art images from text descriptions
- Customize image size, outline style, shading, and more
- Save generated images to your local machine
- Use as a Python module or command-line tool
- Supports various customization options:
  - Outline styles: single color black outline, single color outline, selective outline, lineless
  - Shading styles: flat shading, basic shading, medium shading, detailed shading, highly detailed shading
  - Detail levels: low detail, medium detail, highly detailed
  - View perspectives: side, low top-down, high top-down
  - Directions: north, north-east, east, south-east, south, south-west, west, north-west
  - Isometric view
  - Transparent background
  - Initial image influence
  - Color palette enforcement
  - Text guidance scale
  - Seed for reproducibility

## API Documentation

For more information about the PixelLab API, visit [PixelLab API Documentation](https://api.pixellab.ai/v1). 