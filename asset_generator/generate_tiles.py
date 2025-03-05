#!/usr/bin/env python3
"""
Script to generate seamless terrain tiles for the Evolve game.
This script uses Claude AI to interpret terrain descriptions and generate
appropriate pixel art tiles with 3 variations per terrain type.
"""

import os
import argparse
import random
import json
import numpy as np
from PIL import Image, ImageDraw
import requests
import sys
from dotenv import load_dotenv
import math

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Default terrain types as fallback
DEFAULT_TERRAIN_TYPES = {
    "grass": {
        "base_colors": [(34, 139, 34), (50, 205, 50), (60, 179, 113)],  # Dark green, lime green, medium sea green
        "detail_colors": [(255, 255, 0), (255, 192, 203), (255, 255, 255)],  # Yellow, pink, white for flowers
        "detail_chance": 0.05,  # 5% chance of a detail (flower) per pixel
        "special_features": ["flowers"]
    },
    "dungeon": {
        "base_colors": [(47, 47, 47), (65, 65, 65), (80, 80, 80)],  # Very dark grays for stone floor
        "detail_colors": [(30, 30, 30), (100, 100, 100), (20, 20, 40)],  # Darker and lighter spots, cracks
        "detail_chance": 0.08,  # 8% chance of a detail (crack/moss) per pixel
        "special_features": ["cracks"]
    }
}

def query_claude(prompt):
    """
    Query Claude AI with a prompt to get terrain configuration.
    Uses the Anthropic API to get a response from Claude.
    """
    print(f"Asking Claude AI about: {prompt}")
    
    # Check if API key is available
    if not ANTHROPIC_API_KEY:
        print("Warning: No Anthropic API key found. Using fallback terrain configuration.")
        # Use fallback for known terrain types
        if prompt.lower() == "grass":
            return DEFAULT_TERRAIN_TYPES["grass"]
        elif prompt.lower() == "dungeon":
            return DEFAULT_TERRAIN_TYPES["dungeon"]
        else:
            # For unknown terrains, return a generic configuration
            return {
                "base_colors": [(100, 100, 100), (120, 120, 120), (140, 140, 140)],
                "detail_colors": [(80, 80, 80), (160, 160, 160)],
                "detail_chance": 0.05,
                "special_features": [],
                "pattern": "dots",
                "description": f"Generated terrain based on '{prompt}' with gray tones and subtle variations."
            }
    
    # Prepare the prompt for Claude
    system_prompt = """You are an expert in pixel art and game design. 
    Your task is to analyze a terrain description and provide a JSON configuration for generating pixel art tiles.
    
    For each terrain description, provide:
    1. A list of 3 base_colors as RGB tuples (e.g., [255, 0, 0] for red)
    2. A list of 2-3 detail_colors as RGB tuples for special features
    3. A detail_chance value between 0.01 and 0.1 (probability of adding details)
    4. A list of special_features from: ["flowers", "cracks", "crystals", "hieroglyphs", "bubbles"]
    5. A pattern type from: ["dots", "stripes", "waves", "small_leaves", "large_leaves", "bricks", "cobblestone", "scales", "hexagons", "circles"]
    6. A brief description of the terrain
    
    Respond ONLY with valid JSON in this format:
    {
        "base_colors": [[r, g, b], [r, g, b], [r, g, b]],
        "detail_colors": [[r, g, b], [r, g, b]],
        "detail_chance": 0.05,
        "special_features": ["feature1", "feature2"],
        "pattern": "pattern_name",
        "description": "Description of the terrain"
    }
    """
    
    user_prompt = f"Create a pixel art terrain configuration for: {prompt}"
    
    try:
        # Make API request to Claude
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 1000,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_prompt}]
            }
        )
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response
            result = response.json()
            content = result.get("content", [])
            if content and isinstance(content, list) and len(content) > 0:
                text = content[0].get("text", "")
                
                # Extract JSON from the response
                try:
                    # Find JSON in the response
                    json_start = text.find("{")
                    json_end = text.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = text[json_start:json_end]
                        print(f"Extracted JSON: {json_str}")
                        terrain_config = json.loads(json_str)
                        
                        # Convert list RGB values to tuples for compatibility
                        if "base_colors" in terrain_config:
                            terrain_config["base_colors"] = [tuple(color) for color in terrain_config["base_colors"]]
                        if "detail_colors" in terrain_config:
                            terrain_config["detail_colors"] = [tuple(color) for color in terrain_config["detail_colors"]]
                        
                        # Add a default pattern if not provided
                        if "pattern" not in terrain_config:
                            terrain_config["pattern"] = "dots"
                        
                        print("Successfully received terrain configuration from Claude!")
                        return terrain_config
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON from Claude's response: {e}")
                    print(f"Raw response text: {text}")
        else:
            print(f"Error from Claude API: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"Error communicating with Claude API: {e}")
    
    # Fallback to predefined configurations if API call fails
    print("Using fallback terrain configuration.")
    
    # Use a more interesting fallback for crystal cavern
    if prompt.lower() == "crystal cavern":
        return {
            "base_colors": [(70, 90, 110), (90, 120, 150), (110, 140, 170)],
            "detail_colors": [(200, 220, 255), (150, 200, 220), (180, 180, 220)],
            "detail_chance": 0.07,
            "special_features": ["crystals"],
            "pattern": "hexagons",
            "description": "A mysterious crystal cavern with blue-gray stone and glowing crystal formations."
        }
    # Check if we have a predefined response for other prompts
    elif prompt.lower() == "dungeon":
        return {
            "base_colors": [(47, 47, 47), (65, 65, 65), (80, 80, 80)],
            "detail_colors": [(30, 30, 30), (100, 100, 100), (20, 20, 40)],
            "detail_chance": 0.08,
            "special_features": ["cracks"],
            "pattern": "cobblestone",
            "description": "A dark stone dungeon floor with cracks and subtle variations in the stone color."
        }
    elif prompt.lower() == "lava":
        return {
            "base_colors": [(255, 0, 0), (255, 69, 0), (255, 140, 0)],
            "detail_colors": [(255, 215, 0), (255, 255, 0)],
            "detail_chance": 0.06,
            "special_features": ["bubbles"],
            "pattern": "waves",
            "description": "Hot molten lava with bright orange and red tones, occasional yellow bubbles and sparks."
        }
    elif prompt.lower() == "ice cave":
        return {
            "base_colors": [(200, 230, 255), (180, 210, 240), (160, 190, 230)],
            "detail_colors": [(255, 255, 255), (130, 170, 220)],
            "detail_chance": 0.05,
            "special_features": ["crystals"],
            "pattern": "scales",
            "description": "A shimmering ice cave floor with pale blue tones and occasional white ice crystals."
        }
    elif prompt.lower() == "ancient temple":
        return {
            "base_colors": [(180, 160, 120), (160, 140, 100), (140, 120, 80)],
            "detail_colors": [(200, 180, 140), (120, 100, 60), (90, 70, 40)],
            "detail_chance": 0.07,
            "special_features": ["hieroglyphs"],
            "pattern": "bricks",
            "description": "Ancient temple floor with worn sandstone tiles, occasional hieroglyphs and carvings."
        }
    else:
        # For any other prompt, return a generic terrain
        return {
            "base_colors": [(100, 100, 100), (120, 120, 120), (140, 140, 140)],
            "detail_colors": [(80, 80, 80), (160, 160, 160)],
            "detail_chance": 0.05,
            "special_features": [],
            "pattern": "dots",
            "description": f"Generated terrain based on '{prompt}' with gray tones and subtle variations."
        }

def generate_special_feature(draw, x, y, feature_type, color, size=32):
    """Generate special features like flowers, cracks, crystals, etc."""
    if feature_type == "flowers":
        generate_simple_flower(draw, x, y, color)
    elif feature_type == "cracks":
        generate_crack(draw, x, y, color, size)
    elif feature_type == "crystals":
        generate_crystal(draw, x, y, color)
    elif feature_type == "hieroglyphs":
        generate_hieroglyph(draw, x, y, color)
    elif feature_type == "bubbles":
        generate_bubble(draw, x, y, color)
    # Add more special features as needed

def generate_simple_flower(draw, x, y, color):
    """Draw a simple flower at the specified position."""
    # Make sure the flower is within bounds
    if x < 2 or y < 2 or x >= 30 or y >= 30:
        return
    
    # Draw the center of the flower
    draw.point((x, y), fill=(255, 255, 0))  # Yellow center
    
    # Draw the petals
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        draw.point((x + dx, y + dy), fill=color)

def generate_crack(draw, x, y, color, size=32):
    """Draw a crack pattern starting from the specified position."""
    # Make sure we're not too close to the edge
    if x < 2 or y < 2 or x >= size-2 or y >= size-2:
        return
    
    # Determine crack length
    length = random.randint(2, 5)
    
    # Choose a direction
    direction = random.choice([(1, 0), (0, 1), (1, 1), (-1, 1)])
    dx, dy = direction
    
    # Draw the crack
    for i in range(length):
        nx, ny = x + i*dx, y + i*dy
        if 0 <= nx < size and 0 <= ny < size:
            draw.point((nx, ny), fill=color)
            
            # Sometimes add a branch
            if random.random() < 0.3:
                branch_dx, branch_dy = -dy, dx  # Perpendicular direction
                branch_x, branch_y = nx + branch_dx, ny + branch_dy
                if 0 <= branch_x < size and 0 <= branch_y < size:
                    draw.point((branch_x, branch_y), fill=color)

def generate_crystal(draw, x, y, color):
    """Draw a small crystal at the specified position."""
    # Make sure we're not too close to the edge
    if x < 2 or y < 2 or x >= 30 or y >= 30:
        return
    
    # Draw a diamond shape
    points = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
    draw.polygon(points, fill=color)

def generate_hieroglyph(draw, x, y, color):
    """Draw a simple hieroglyph-like symbol."""
    # Make sure we're not too close to the edge
    if x < 3 or y < 3 or x >= 29 or y >= 29:
        return
    
    # Choose a simple pattern
    pattern = random.choice([
        # Simple line
        lambda d, x, y, c: d.line([(x-1, y), (x+1, y)], fill=c),
        # Simple square
        lambda d, x, y, c: d.rectangle([(x-1, y-1), (x+1, y+1)], outline=c),
        # Simple circle
        lambda d, x, y, c: d.ellipse([(x-1, y-1), (x+1, y+1)], outline=c),
        # Simple cross
        lambda d, x, y, c: [d.line([(x-1, y), (x+1, y)], fill=c), d.line([(x, y-1), (x, y+1)], fill=c)]
    ])
    
    # Draw the pattern
    pattern(draw, x, y, color)

def generate_bubble(draw, x, y, color):
    """Draw a bubble or spark in lava."""
    # Draw a small circle
    radius = random.randint(1, 2)
    draw.ellipse([(x-radius, y-radius), (x+radius, y+radius)], fill=color)

def generate_pattern(draw, pattern_type, base_color, detail_color, size=32, seed=None):
    """Generate a pattern based on the specified type."""
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        
    if pattern_type == "dots":
        # Random dots pattern
        for _ in range(int(size * size * 0.2)):
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            radius = random.randint(1, 2)
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=detail_color)
            
    elif pattern_type == "stripes":
        # Horizontal stripes
        stripe_width = random.randint(2, 4)
        for y in range(0, size, stripe_width * 2):
            draw.rectangle((0, y, size, y + stripe_width - 1), fill=detail_color)
            
    elif pattern_type == "waves":
        # Wavy pattern
        amplitude = random.randint(2, 4)
        frequency = random.randint(1, 3) / 10.0
        for x in range(size):
            for wave_num in range(0, size, 8):
                y = int(wave_num + amplitude * math.sin(frequency * x))
                if 0 <= y < size:
                    draw.line((x, y, x, y+2), fill=detail_color)
                    
    elif pattern_type == "small_leaves":
        # Small leaf patterns
        for _ in range(15):
            x = random.randint(2, size-3)
            y = random.randint(2, size-3)
            # Draw a small leaf
            points = [(x, y-2), (x+2, y), (x, y+2), (x-2, y)]
            draw.polygon(points, fill=detail_color)
            
    elif pattern_type == "large_leaves":
        # Larger leaf patterns
        for _ in range(5):
            x = random.randint(4, size-5)
            y = random.randint(4, size-5)
            # Draw a larger leaf
            points = [(x, y-4), (x+4, y), (x, y+4), (x-4, y)]
            draw.polygon(points, fill=detail_color)
            
    elif pattern_type == "bricks":
        # Brick pattern
        brick_height = 4
        brick_width = 8
        for y in range(0, size, brick_height):
            offset = (y // brick_height) % 2 * (brick_width // 2)
            for x in range(-brick_width + offset, size, brick_width):
                draw.rectangle((x+1, y+1, x+brick_width-1, y+brick_height-1), outline=detail_color)
                
    elif pattern_type == "cobblestone":
        # Cobblestone pattern
        for _ in range(15):
            x = random.randint(2, size-5)
            y = random.randint(2, size-5)
            w = random.randint(3, 6)
            h = random.randint(3, 6)
            draw.ellipse((x, y, x+w, y+h), outline=detail_color)
            
    elif pattern_type == "scales":
        # Scale pattern
        scale_size = 6
        for row in range(0, size+scale_size, scale_size):
            offset = (row // scale_size) % 2 * (scale_size // 2)
            for col in range(-scale_size + offset, size, scale_size):
                draw.arc((col, row, col+scale_size, row+scale_size), 0, 180, fill=detail_color)
                
    elif pattern_type == "hexagons":
        # Hexagon pattern
        hex_size = 6
        for row in range(0, size, hex_size*2):
            for col in range(0, size, hex_size):
                offset_y = hex_size if (col // hex_size) % 2 == 0 else 0
                y = row + offset_y
                if y < size:
                    points = [
                        (col, y), 
                        (col+hex_size//2, y-hex_size//2),
                        (col+hex_size, y),
                        (col+hex_size, y+hex_size),
                        (col+hex_size//2, y+hex_size*3//2),
                        (col, y+hex_size)
                    ]
                    draw.polygon([(x, y) for x, y in points if 0 <= x < size and 0 <= y < size], outline=detail_color)
                    
    elif pattern_type == "circles":
        # Concentric circles
        for _ in range(3):
            x = random.randint(size//4, size*3//4)
            y = random.randint(size//4, size*3//4)
            for r in range(2, 12, 3):
                draw.ellipse((x-r, y-r, x+r, y+r), outline=detail_color)
    
    else:
        # Default to random dots if pattern not recognized
        for _ in range(int(size * size * 0.1)):
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            draw.point((x, y), fill=detail_color)

def generate_terrain_tile(terrain_config, variation, size=32, seed=None):
    """Generate a terrain tile with the specified parameters."""
    if seed is not None:
        random.seed(seed + variation)  # Add variation to seed for different variations
        np.random.seed(seed + variation)
    
    # Extract terrain configuration
    base_colors = terrain_config["base_colors"]
    detail_colors = terrain_config["detail_colors"]
    detail_chance = terrain_config["detail_chance"]
    special_features = terrain_config.get("special_features", [])
    
    # Create a new image
    img = Image.new('RGB', (size, size), color=base_colors[0])
    draw = ImageDraw.Draw(img)
    
    # Generate noise for the base terrain
    noise = np.random.rand(size, size)
    
    # Fill the image with terrain
    for y in range(size):
        for x in range(size):
            # Determine base color based on noise
            color_idx = int(noise[y, x] * len(base_colors))
            color_idx = min(color_idx, len(base_colors) - 1)
            color = base_colors[color_idx]
            
            # Apply the base color
            draw.point((x, y), fill=color)
            
            # Add details with a certain probability
            if random.random() < detail_chance:
                detail_color = random.choice(detail_colors)
                
                # Check if we should add a special feature
                if special_features and random.random() < 0.3:  # 30% chance for special feature
                    feature = random.choice(special_features)
                    generate_special_feature(draw, x, y, feature, detail_color, size)
                else:
                    # Just add a detail point
                    draw.point((x, y), fill=detail_color)
    
    return img

def generate_terrain_tiles(terrain_prompt, output_dir="src/assets/images/tiles", seed=None):
    """Generate a set of terrain tiles based on the given prompt."""
    # Set random seed if provided
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    # Get the terrain configuration
    terrain_config = query_claude(terrain_prompt)
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert terrain prompt to filename-friendly format
    terrain_name = terrain_prompt.lower().replace(" ", "_")
    
    # Clear the entire tiles folder
    for file in os.listdir(output_dir):
        if file.endswith('.png'):
            os.remove(os.path.join(output_dir, file))
            print(f"Removed existing tile: {os.path.join(output_dir, file)}")
    
    print(f"\nTerrain Configuration for '{terrain_prompt}':")
    print(f"Description: {terrain_config['description']}")
    print(f"Base Colors: {terrain_config['base_colors']}")
    print(f"Detail Colors: {terrain_config['detail_colors']}")
    print(f"Detail Chance: {terrain_config['detail_chance']}")
    print(f"Special Features: {terrain_config['special_features']}")
    print(f"Pattern: {terrain_config.get('pattern', 'dots')}")
    print()
    
    # Generate 3 variations of the terrain
    print(f"Generating '{terrain_prompt}' terrain tiles...")
    generated_files = []
    
    # Generate 3 regular variations
    for i in range(1, 4):
        print(f"Generating variation {i}...")
        # Generate the terrain tile
        img = generate_terrain_tile(terrain_config, variation=i, seed=seed)
        
        # Save the tile
        filename = os.path.join(output_dir, f"{terrain_name}_{i}.png")
        img.save(filename)
        generated_files.append(filename)
        print(f"Generated tile: {filename}")
    
    # Generate the pattern variation (4th tile)
    print("Generating pattern variation...")
    pattern_type = terrain_config.get('pattern', 'dots')
    
    # Create a new image for the pattern
    pattern_img = Image.new('RGBA', (32, 32), random.choice(terrain_config['base_colors']))
    draw = ImageDraw.Draw(pattern_img)
    
    # Generate the pattern
    detail_color = random.choice(terrain_config['detail_colors'])
    generate_pattern(draw, pattern_type, random.choice(terrain_config['base_colors']), detail_color, seed=seed)
    
    # Save the pattern tile
    pattern_filename = os.path.join(output_dir, f"{terrain_name}_pattern.png")
    pattern_img.save(pattern_filename)
    generated_files.append(pattern_filename)
    print(f"Generated pattern tile: {pattern_filename}")
    
    print(f"Generated {len(generated_files)} terrain tiles:")
    for file in generated_files:
        print(f"  - {file}")
    
    print("Terrain tile generation complete!")
    return generated_files

def main():
    """Main function to parse arguments and generate tiles."""
    parser = argparse.ArgumentParser(description="Generate terrain tiles for the Evolve game using Claude AI.")
    parser.add_argument("--terrain", required=True, help="Terrain description (e.g., 'dungeon', 'lava', 'ice cave')")
    parser.add_argument("--output-dir", default="src/assets/images/tiles", help="Output directory for tiles")
    parser.add_argument("--seed", type=int, help="Seed for reproducible generation")
    
    args = parser.parse_args()
    
    # Get project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print(f"Project root: {project_root}")
    
    # Set output directory
    output_dir = os.path.join(project_root, args.output_dir)
    print(f"Tiles directory: {output_dir}")
    
    # Generate tiles
    generate_terrain_tiles(args.terrain, output_dir, seed=args.seed)
    
    # Update the tile list JSON file
    print("\nUpdating tile list for the game...")
    try:
        # Run the Node.js script to generate the tile list
        import subprocess
        tile_list_script = os.path.join(os.path.dirname(__file__), "generate_tile_list.js")
        result = subprocess.run(["node", tile_list_script], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
            print("Tile list updated successfully!")
        else:
            print(f"Error updating tile list: {result.stderr}")
            print("You may need to run 'node generate_tile_list.js' manually.")
    except Exception as e:
        print(f"Error running tile list generator: {e}")
        print("You may need to run 'node generate_tile_list.js' manually.")

if __name__ == "__main__":
    main() 