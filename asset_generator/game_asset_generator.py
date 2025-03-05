#!/usr/bin/env python3
"""
Game Asset Generator - A Python module for generating pixel art game assets using the PixelLab API.
Specialized for creating game assets with consistent styling.
"""

import os
import argparse
import pixellab
from dotenv import load_dotenv
from PIL import Image
import base64
import io
import random
import time
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

def save_base64_image(base64_data, output_path=None):
    """
    Save a base64 encoded image to a file or return the PIL Image object.
    
    Args:
        base64_data (str): The base64 encoded image data.
        output_path (str, optional): The path to save the image to. If None, the PIL Image object is returned.
        
    Returns:
        PIL.Image.Image or str: The PIL Image object if output_path is None, otherwise the path to the saved image.
    """
    # Extract the base64 data part (remove the data:image/png;base64, prefix if present)
    if "base64," in base64_data:
        base64_data = base64_data.split("base64,")[1]
    
    # Decode the base64 data
    image_data = base64.b64decode(base64_data)
    
    # Create a PIL Image from the decoded data
    image = Image.open(io.BytesIO(image_data))
    
    # If output_path is provided, save the image
    if output_path:
        image.save(output_path)
        print(f"Image saved to {output_path}")
        return output_path
    
    # Otherwise, return the PIL Image object
    return image

def generate_pixel_art(description, width=128, height=128, output_path=None, 
                       negative_description=None, outline=None, shading=None, 
                       detail=None, view=None, direction=None, isometric=False, 
                       no_background=False, seed=None, api_token=None,
                       text_guidance_scale=None, init_image=None, init_image_strength=None,
                       color_image=None):
    """
    Generate pixel art using the PixelLab API.
    
    Args:
        description (str): Text description of the image to generate.
        width (int, optional): Width of the image in pixels. Defaults to 128.
        height (int, optional): Height of the image in pixels. Defaults to 128.
        output_path (str, optional): Output file path for the generated image. If None, the PIL Image object is returned.
        negative_description (str, optional): Text description of what to avoid in the generated image.
        outline (str, optional): Outline style for the pixel art. One of: "single color black outline", "single color outline", "selective outline", "lineless".
        shading (str, optional): Shading style for the pixel art. One of: "flat shading", "basic shading", "medium shading", "detailed shading", "highly detailed shading".
        detail (str, optional): Detail level for the pixel art. One of: "low detail", "medium detail", "highly detailed".
        view (str, optional): View perspective for the pixel art. One of: "side", "low top-down", "high top-down".
        direction (str, optional): Direction for the pixel art. One of: "north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west".
        isometric (bool, optional): Generate in isometric view. Defaults to False.
        no_background (bool, optional): Generate with transparent background. Defaults to False.
        seed (int, optional): Seed for the generation process.
        api_token (str, optional): PixelLab API token. If None, it will be read from the PIXELLAB_API_TOKEN environment variable.
        text_guidance_scale (int, optional): How closely to follow the text description (1-20). Higher values follow the description more closely.
        init_image (dict, optional): Initial image to use as a base. Format: {"type": "base64", "base64": "base64_encoded_string"}.
        init_image_strength (int, optional): Strength of the initial image influence (1-999).
        color_image (dict, optional): Image to use for color palette. Format: {"type": "base64", "base64": "base64_encoded_string"}.
        
    Returns:
        PIL.Image.Image or str: The PIL Image object if output_path is None, otherwise the path to the saved image.
        
    Raises:
        ValueError: If the API token is not provided and not found in the environment variables.
        ValueError: If the image size is invalid (area must be between 32x32 and 400x400 pixels).
    """
    # Validate image size
    if width * height < 32 * 32:
        raise ValueError("Image area must be at least 32x32 pixels")
    if width * height > 400 * 400:
        raise ValueError("Image area must be at most 400x400 pixels")
    
    # Get API token from parameter or environment variable
    if not api_token:
        api_token = os.getenv("PIXELLAB_API_TOKEN")
    if not api_token:
        raise ValueError("API token not found. Please provide an API token or set the PIXELLAB_API_TOKEN environment variable.")
    
    # Initialize the PixelLab client
    client = pixellab.Client(secret=api_token)
    
    # Prepare parameters for the API call
    params = {
        "description": description,
        "image_size": {"width": width, "height": height}
    }
    
    # Add optional parameters if provided
    if negative_description:
        params["negative_description"] = negative_description
    if outline:
        params["outline"] = outline
    if shading:
        params["shading"] = shading
    if detail:
        params["detail"] = detail
    if view:
        params["view"] = view
    if direction:
        params["direction"] = direction
    if isometric:
        params["isometric"] = isometric
    
    # Ensure no_background is properly set
    params["no_background"] = True if no_background else False
    
    if seed:
        params["seed"] = seed
    if text_guidance_scale:
        params["text_guidance_scale"] = text_guidance_scale
    if init_image:
        params["init_image"] = init_image
    if init_image_strength:
        params["init_image_strength"] = init_image_strength
    if color_image:
        params["color_image"] = color_image
    
    # Generate the image
    print(f"Generating pixel art with description: '{description}'...")
    response = client.generate_image_pixflux(**params)
    
    # Save the image or return the PIL Image object
    if output_path:
        return save_base64_image(response.image.base64, output_path)
    else:
        return save_base64_image(response.image.base64)

def generate_game_asset(asset_type, description, output_path=None, width=None, height=None, seed=None, api_token=None, no_background=None):
    """
    Generate a game asset with styling appropriate for a Vampire Survivors-like game.
    
    Args:
        asset_type (str): Type of asset to generate. One of: "character", "enemy", "weapon", "item", "environment", "effect".
        description (str): Text description of the asset to generate.
        output_path (str, optional): Output file path for the generated image. If None, the PIL Image object is returned.
        width (int, optional): Width of the image in pixels. If None, a default size based on asset_type will be used.
        height (int, optional): Height of the image in pixels. If None, a default size based on asset_type will be used.
        seed (int, optional): Seed for the generation process. If None, a random seed will be used.
        api_token (str, optional): PixelLab API token. If None, it will be read from the PIXELLAB_API_TOKEN environment variable.
        no_background (bool, optional): Force transparent background. If None, defaults to True for game assets.
        
    Returns:
        PIL.Image.Image or str: The PIL Image object if output_path is None, otherwise the path to the saved image.
    """
    # Set default sizes based on asset type
    if width is None or height is None:
        if asset_type == "character":
            width = width or 64
            height = height or 64
        elif asset_type == "enemy":
            width = width or 64
            height = height or 64
        elif asset_type == "weapon":
            width = width or 32
            height = height or 32
        elif asset_type == "item":
            width = width or 32
            height = height or 32
        elif asset_type == "environment":
            width = width or 128
        elif asset_type == "effect":
            width = width or 64
            height = height or 64
        else:
            width = width or 64
            height = height or 64
    
    # Use a random seed if none provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    # Set common parameters for all assets
    common_params = {
        "no_background": True if no_background is None else no_background,  # Transparent background for all game assets
        "text_guidance_scale": 12,  # Follow description closely
        "seed": seed
    }
    
    # Set asset-specific parameters
    if asset_type == "character":
        common_params.update({
            "outline": "single color black outline",
            "shading": "medium shading",
            "detail": "medium detail",
            "view": "side",
            "direction": "east",  # Always face east
            "negative_description": "blurry, low quality, realistic, 3D, complex background, floor, shadows, ground, standing on ground, shadow under feet, shadow beneath character"
        })
    elif asset_type == "enemy":
        common_params.update({
            "outline": "single color black outline",
            "shading": "medium shading",
            "detail": "medium detail",
            "view": "side",
            "direction": "east",  # Always face east
            "negative_description": "blurry, low quality, realistic, 3D, complex background, floor, shadows, ground, standing on ground, shadow under feet, shadow beneath character, portrait, bust, headshot, face only, dark background, checkered background, close-up"
        })
    elif asset_type == "weapon":
        common_params.update({
            "outline": "single color black outline",
            "shading": "basic shading",
            "detail": "medium detail",
            "view": "side",
            "negative_description": "blurry, low quality, realistic, 3D, complex background, hands holding it"
        })
    elif asset_type == "item":
        common_params.update({
            "outline": "single color black outline",
            "shading": "basic shading",
            "detail": "low detail",
            "view": "side",
            "negative_description": "blurry, low quality, realistic, 3D, complex background"
        })
    elif asset_type == "environment":
        common_params.update({
            "outline": "selective outline",
            "shading": "medium shading",
            "detail": "medium detail",
            "view": "low top-down",
            "negative_description": "blurry, low quality, realistic, 3D, characters, creatures"
        })
    elif asset_type == "effect":
        common_params.update({
            "outline": "lineless",
            "shading": "basic shading",
            "detail": "low detail",
            "negative_description": "blurry, low quality, realistic, 3D, complex background"
        })
    
    # Enhance the description with pixel art styling
    enhanced_description = f"pixel art {description}, for a vampire survivors style game, pixelated, game asset"
    
    # Enhance the description based on asset type
    if "pixel art" not in enhanced_description.lower():
        enhanced_description = f"pixel art {enhanced_description}"
    
    if "game sprite" not in enhanced_description.lower():
        enhanced_description = f"{enhanced_description} game sprite"
    
    # Only add "full body" for character and enemy assets
    if asset_type in ["character", "enemy"]:
        if "full body" not in enhanced_description.lower():
            enhanced_description = f"full body {enhanced_description}"
    
    # Generate the asset
    return generate_pixel_art(
        description=enhanced_description,
        width=width,
        height=height,
        output_path=output_path,
        api_token=api_token,
        **common_params
    )

def generate_character_set(character_description, output_dir="src/assets/images", seed=None, api_token=None):
    """
    Generate a character asset with consistent styling and save directly to the game's src folder.
    
    Args:
        character_description (str): Description of the character.
        output_dir (str, optional): Directory to save the character asset to. Defaults to "src/assets/images".
        seed (int, optional): Seed for the generation process. If None, a random seed will be used.
        api_token (str, optional): PixelLab API token. If None, it will be read from the PIXELLAB_API_TOKEN environment variable.
        
    Returns:
        str: File path to the generated character asset.
    """
    # Use a random seed if none provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate idle character asset
    character_path = os.path.join(output_dir, "player.png")
    
    # Generate the character
    result = generate_game_asset(
        asset_type="character",
        description=f"full body pixel art {character_description} standing idle game sprite character facing right",
        output_path=character_path,
        seed=seed,
        api_token=api_token,
        no_background=True  # Explicitly ensure transparent background
    )
    
    print(f"Generated character asset: {character_path}")
    return character_path

def generate_enemy_set(enemy_type, output_dir="src/assets/images", count=1, seed=None, api_token=None):
    """
    Generate an enemy asset and save directly to the game's src folder.
    
    Args:
        enemy_type (str): Type of enemy to generate (e.g., "zombie", "skeleton", "vampire").
        output_dir (str, optional): Directory to save the enemy assets to. Defaults to "src/assets/images".
        count (int, optional): Number of variations to generate. Defaults to 1.
        seed (int, optional): Seed for the generation process. If None, a random seed will be used.
        api_token (str, optional): PixelLab API token. If None, it will be read from the PIXELLAB_API_TOKEN environment variable.
        
    Returns:
        list: List of file paths to the generated enemy assets.
    """
    # Use a random seed if none provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate enemy assets
    assets = []
    
    # Generate the main enemy asset (will be used as enemy.png)
    enemy_path = os.path.join(output_dir, "enemy.png")
    asset = generate_game_asset(
        asset_type="enemy",
        description=f"full body pixel art {enemy_type} game sprite character facing right",
        output_path=enemy_path,
        seed=seed,
        api_token=api_token,
        no_background=True  # Explicitly ensure transparent background
    )
    
    assets.append(asset)
    print(f"Generated main enemy asset: {enemy_path}")
    
    # Generate additional variations if requested
    if count > 1:
        for i in range(1, count):
            # Add variations to the description
            if i == 1:
                description = f"full body pixel art larger {enemy_type} game sprite character facing right"
            else:
                description = f"full body pixel art elite {enemy_type} with special features game sprite character facing right"
            
            # Generate enemy asset
            variation_path = os.path.join(output_dir, f"enemy_{i}.png")
            asset = generate_game_asset(
                asset_type="enemy",
                description=description,
                output_path=variation_path,
                seed=seed + i,  # Use a different but related seed for each variation
                api_token=api_token,
                no_background=True  # Explicitly ensure transparent background
            )
            
            assets.append(asset)
            print(f"Generated enemy variation: {variation_path}")
    
    return assets

def generate_weapon_set(weapon_type, output_dir="src/assets/images/weapons", output_filename=None, seed=None, api_token=None):
    """
    Generate a weapon asset.
    
    Args:
        weapon_type (str): Type of weapon to generate (e.g., "sword", "axe", "wand").
        output_dir (str, optional): Directory to save the weapon asset to. Defaults to "src/assets/images/weapons".
        output_filename (str, optional): Filename to use for the weapon. If None, a filename will be generated from the weapon type.
        seed (int, optional): Seed for the generation process. If None, a random seed will be used.
        api_token (str, optional): PixelLab API token. If None, it will be read from the PIXELLAB_API_TOKEN environment variable.
        
    Returns:
        str: File path to the generated weapon asset.
    """
    # Use a random seed if none provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate weapon asset
    if output_filename is None:
        weapon_filename = f"{weapon_type.replace(' ', '_')}.png"
    else:
        weapon_filename = output_filename
    
    weapon_path = os.path.join(output_dir, weapon_filename)
    
    # Generate the weapon
    result = generate_game_asset(
        asset_type="weapon",
        description=f"isolated {weapon_type}, simple pixel art icon, small weapon icon, no character, top-down view, small size",
        output_path=weapon_path,
        seed=seed,
        api_token=api_token,
        no_background=True,  # Explicitly ensure transparent background
        width=32,
        height=32
    )
    
    print(f"Generated weapon asset: {weapon_path}")
    return weapon_path

def generate_item_set(item_type, variations=["standard", "rare", "epic"], output_dir="src/assets/images/items", seed=None, api_token=None):
    """
    Generate a set of item assets with variations.
    
    Args:
        item_type (str): Type of item to generate (e.g., "potion", "coin", "powerup").
        variations (list, optional): List of variations to generate. Defaults to ["standard", "rare", "epic"].
        output_dir (str, optional): Directory to save the item assets to. Defaults to "src/assets/images/items".
        seed (int, optional): Seed for the generation process. If None, a random seed will be used.
        api_token (str, optional): PixelLab API token. If None, it will be read from the PIXELLAB_API_TOKEN environment variable.
        
    Returns:
        dict: Dictionary mapping variation names to file paths of the generated item assets.
    """
    # Use a random seed if none provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate item assets for each variation
    assets = {}
    
    for i, variation in enumerate(variations):
        # Create a description based on the variation
        if variation == "standard":
            description = f"{item_type}"
        elif variation == "rare":
            description = f"rare {item_type} with enhanced appearance"
        elif variation == "epic":
            description = f"epic {item_type} with glowing effect"
        else:
            description = f"{variation} {item_type}"
        
        # Generate item asset
        item_filename = f"{item_type}_{variation}.png"
        item_path = os.path.join(output_dir, item_filename)
        
        result = generate_game_asset(
            asset_type="item",
            description=description,
            output_path=item_path,
            seed=seed + i,  # Use a different but related seed for each variation
            api_token=api_token,
            no_background=True  # Explicitly ensure transparent background
        )
        
        assets[variation] = item_path
        print(f"Generated {variation} {item_type} asset: {item_path}")
    
    return assets

def generate_item(item_description, output_dir="src/assets/images/items", output_filename=None, seed=None, api_token=None):
    """
    Generate a single item asset.
    
    Args:
        item_description (str): Description of the item.
        output_dir (str, optional): Directory to save the item asset to. Defaults to "src/assets/images/items".
        output_filename (str, optional): Filename to use for the item. If None, a filename will be generated from the item description.
        seed (int, optional): Seed for the generation process. If None, a random seed will be used.
        api_token (str, optional): PixelLab API token. If None, it will be read from the PIXELLAB_API_TOKEN environment variable.
        
    Returns:
        str: File path to the generated item asset.
    """
    # Use a random seed if none provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate item asset
    if output_filename is None:
        item_filename = f"{item_description.replace(' ', '_')}.png"
    else:
        item_filename = output_filename
    
    item_path = os.path.join(output_dir, item_filename)
    
    # Generate the item
    result = generate_game_asset(
        asset_type="item",
        description=f"isolated {item_description}, simple pixel art icon, small item icon, no character, top-down view, small size",
        output_path=item_path,
        seed=seed,
        api_token=api_token,
        no_background=True,  # Explicitly ensure transparent background
        width=32,
        height=32
    )
    
    print(f"Generated item asset: {item_path}")
    return item_path

def generate_character_animation(character_description, action="walk", view="side", direction="east", 
                               n_frames=4, reference_image_path=None, output_dir="src/assets/images/player", 
                               output_format="frames", seed=None, api_token=None):
    """
    Generate an animated version of a character and save directly to the game's src folder.
    
    Args:
        character_description (str): Description of the character.
        action (str, optional): Action for the animation (e.g., "walk", "run", "attack"). Defaults to "walk".
        view (str, optional): View perspective for the animation. One of: "side", "low top-down", "high top-down". Defaults to "side".
        direction (str, optional): Direction for the animation. One of: "north", "north-east", "east", "south-east", 
                                  "south", "south-west", "west", "north-west". Defaults to "east".
        n_frames (int, optional): Number of frames in the animation. Defaults to 4.
        reference_image_path (str, optional): Path to the reference image. If None, a new character will be generated.
        output_dir (str, optional): Directory to save the animation to. Defaults to "src/assets/images/player".
        output_format (str, optional): Format to save the animation in. One of: "spritesheet", "gif", "frames". Defaults to "frames".
        seed (int, optional): Seed for the generation process. If None, a random seed will be used.
        api_token (str, optional): PixelLab API token. If None, it will be read from the PIXELLAB_API_TOKEN environment variable.
        
    Returns:
        str: Path to the generated animation file or directory.
    """
    # Use a random seed if none provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    # Always use east direction regardless of what's passed in
    direction = "east"
    
    # Get API token from parameter or environment variable
    if not api_token:
        api_token = os.getenv("PIXELLAB_API_TOKEN")
    if not api_token:
        raise ValueError("API token not found. Please provide an API token or set the PIXELLAB_API_TOKEN environment variable.")
    
    # If no reference image is provided, generate one and save it to the main player.png location
    if reference_image_path is None:
        print(f"No reference image provided. Generating a new character...")
        reference_image_path = generate_character_set(
            character_description=character_description,
            output_dir="src/assets/images",  # Save to main images directory
            seed=seed,
            api_token=api_token
        )
    
    # Load the reference image as PIL Image
    reference_pil_image = Image.open(reference_image_path)
    
    # Initialize the PixelLab client
    client = pixellab.Client(secret=api_token)
    
    print(f"Generating {action} animation for '{character_description}'...")
    
    # Prepare API parameters
    api_params = {
        "description": f"full body pixel art {character_description} game sprite character facing right moving right",
        "action": action,
        "view": view,
        "direction": direction,
        "image_size": {"width": 64, "height": 64},
        "reference_image": reference_pil_image,
        "n_frames": n_frames,
        "seed": seed,
        "negative_description": "blurry, low quality, realistic, 3D, complex background, floor, shadows, ground, standing on ground, shadow under feet, shadow beneath character, portrait, bust, headshot, face only, dark background, checkered background, close-up, facing left, facing forward, facing back, moving left"
    }
    
    # Call the animation API
    try:
        response = client.animate_with_text(**api_params)
        
        # Get the animation frames
        frames = []
        for image in response.images:
            if hasattr(image, 'pil_image'):
                # Use the pil_image method if available
                frames.append(image.pil_image())
            else:
                # Fall back to manual conversion
                img_data = image.base64.split("base64,")[1] if "base64," in image.base64 else image.base64
                frames.append(Image.open(io.BytesIO(base64.b64decode(img_data))))
        
        # Create the walk directory if it doesn't exist
        walk_dir = os.path.join(output_dir, action)
        os.makedirs(walk_dir, exist_ok=True)
        
        # Save the animation in the requested format
        if output_format == "frames":
            # Save individual frames in the walk directory
            frame_paths = []
            for i, frame in enumerate(frames):
                frame_path = os.path.join(walk_dir, f"frame_{i+1}.png")
                frame.save(frame_path)
                frame_paths.append(frame_path)
            
            print(f"Saved {len(frame_paths)} animation frames to {walk_dir}")
            return walk_dir
        elif output_format == "spritesheet":
            # Create a spritesheet
            spritesheet_path = os.path.join(output_dir, f"{character_description.replace(' ', '_')}_{action}_spritesheet.png")
            create_spritesheet(frames, spritesheet_path)
            print(f"Saved animation spritesheet to {spritesheet_path}")
            return spritesheet_path
        elif output_format == "gif":
            # Create a GIF
            gif_path = os.path.join(output_dir, f"{character_description.replace(' ', '_')}_{action}.gif")
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                optimize=False,
                duration=100,  # 100ms per frame
                loop=0  # Loop forever
            )
            print(f"Saved animation GIF to {gif_path}")
            return gif_path
        else:
            raise ValueError(f"Invalid output format: {output_format}. Must be one of: 'spritesheet', 'gif', 'frames'.")
    
    except Exception as e:
        print(f"Error generating animation: {e}")
        raise
    
    return None

def generate_enemy_animation(enemy_type, action="walk", view="side", direction="east", 
                           n_frames=4, reference_image_path=None, output_dir="src/assets/images/enemies", 
                           output_format="frames", seed=None, api_token=None):
    """
    Generate an animated version of an enemy and save directly to the game's src folder.
    
    Args:
        enemy_type (str): Type of enemy to generate (e.g., "zombie", "skeleton", "vampire").
        action (str, optional): Action for the animation (e.g., "idle", "attack", "walk"). Defaults to "walk".
        view (str, optional): View perspective for the animation. One of: "side", "low top-down", "high top-down". Defaults to "side".
        direction (str, optional): Direction for the animation. One of: "north", "north-east", "east", "south-east", 
                                  "south", "south-west", "west", "north-west". Defaults to "east".
        n_frames (int, optional): Number of frames in the animation. Defaults to 4.
        reference_image_path (str, optional): Path to the reference image. If None, a new enemy will be generated.
        output_dir (str, optional): Directory to save the animation to. Defaults to "src/assets/images/enemies".
        output_format (str, optional): Format to save the animation in. One of: "spritesheet", "gif", "frames". Defaults to "frames".
        seed (int, optional): Seed for the generation process. If None, a random seed will be used.
        api_token (str, optional): PixelLab API token. If None, it will be read from the PIXELLAB_API_TOKEN environment variable.
        
    Returns:
        str: Path to the generated animation file or directory.
    """
    # Use a random seed if none provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    # Always use east direction regardless of what's passed in
    direction = "east"
    
    # Get API token from parameter or environment variable
    if not api_token:
        api_token = os.getenv("PIXELLAB_API_TOKEN")
    if not api_token:
        raise ValueError("API token not found. Please provide an API token or set the PIXELLAB_API_TOKEN environment variable.")
    
    # If no reference image is provided, generate one and save it to the main enemy.png location
    if reference_image_path is None:
        print(f"No reference image provided. Generating a new enemy...")
        # Generate a basic enemy and use the first variation
        enemy_assets = generate_enemy_set(
            enemy_type=enemy_type,
            output_dir="src/assets/images",  # Save to main images directory
            count=1,  # Just generate one enemy
            seed=seed,
            api_token=api_token
        )
        reference_image_path = enemy_assets[0]
    
    # Load the reference image as PIL Image
    reference_pil_image = Image.open(reference_image_path)
    
    # Initialize the PixelLab client
    client = pixellab.Client(secret=api_token)
    
    print(f"Generating {action} animation for '{enemy_type}'...")
    
    # Prepare API parameters
    api_params = {
        "description": f"full body pixel art {enemy_type} game sprite character facing right moving right",
        "action": action,
        "view": view,
        "direction": direction,
        "image_size": {"width": 64, "height": 64},
        "reference_image": reference_pil_image,
        "n_frames": n_frames,
        "seed": seed,
        "negative_description": "blurry, low quality, realistic, 3D, complex background, floor, shadows, ground, standing on ground, shadow under feet, shadow beneath character, portrait, bust, headshot, face only, dark background, checkered background, close-up, facing left, facing forward, facing back, moving left"
    }
    
    # Call the animation API
    try:
        response = client.animate_with_text(**api_params)
        
        # Get the animation frames
        frames = []
        for image in response.images:
            if hasattr(image, 'pil_image'):
                # Use the pil_image method if available
                frames.append(image.pil_image())
            else:
                # Fall back to manual conversion
                img_data = image.base64.split("base64,")[1] if "base64," in image.base64 else image.base64
                frames.append(Image.open(io.BytesIO(base64.b64decode(img_data))))
        
        # Create the walk directory if it doesn't exist
        walk_dir = os.path.join(output_dir, action)
        os.makedirs(walk_dir, exist_ok=True)
        
        # Save the animation in the requested format
        if output_format == "frames":
            # Save individual frames in the walk directory
            frame_paths = []
            for i, frame in enumerate(frames):
                frame_path = os.path.join(walk_dir, f"frame_{i+1}.png")
                frame.save(frame_path)
                frame_paths.append(frame_path)
            
            print(f"Saved {len(frame_paths)} animation frames to {walk_dir}")
            return walk_dir
        elif output_format == "spritesheet":
            # Create a spritesheet
            spritesheet_path = os.path.join(output_dir, f"{enemy_type.replace(' ', '_')}_{action}_spritesheet.png")
            create_spritesheet(frames, spritesheet_path)
            print(f"Saved animation spritesheet to {spritesheet_path}")
            return spritesheet_path
        elif output_format == "gif":
            # Create a GIF
            gif_path = os.path.join(output_dir, f"{enemy_type.replace(' ', '_')}_{action}.gif")
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                optimize=False,
                duration=100,  # 100ms per frame
                loop=0  # Loop forever
            )
            print(f"Saved animation GIF to {gif_path}")
            return gif_path
        else:
            raise ValueError(f"Invalid output format: {output_format}. Must be one of: 'spritesheet', 'gif', 'frames'.")
    
    except Exception as e:
        print(f"Error generating animation: {e}")
        raise
    
    return None

def create_spritesheet(frames, output_path):
    """
    Create a spritesheet from a list of frames.
    
    Args:
        frames (list): List of PIL Image objects.
        output_path (str): Path to save the spritesheet to.
        
    Returns:
        str: Path to the saved spritesheet.
    """
    # Create a spritesheet (horizontal strip of frames)
    width, height = frames[0].size
    spritesheet = Image.new("RGBA", (width * len(frames), height))
    
    for i, frame in enumerate(frames):
        spritesheet.paste(frame, (i * width, 0))
    
    spritesheet.save(output_path)
    return output_path

def generate_projectile(projectile_type, weapon_name, output_dir="src/assets/images/weapons/projectiles", output_filename=None, seed=None, api_token=None):
    """
    Generate a projectile asset for a weapon.
    
    Args:
        projectile_type (str): Type of projectile to generate (e.g., "arrow", "fireball", "bullet").
        weapon_name (str): Name of the weapon this projectile is for.
        output_dir (str, optional): Directory to save the projectile asset to. Defaults to "src/assets/images/weapons/projectiles".
        output_filename (str, optional): Filename to use for the projectile. If None, a filename will be generated from the projectile type.
        seed (int, optional): Seed for the generation process. If None, a random seed will be used.
        api_token (str, optional): PixelLab API token. If None, it will be read from the PIXELLAB_API_TOKEN environment variable.
        
    Returns:
        str: File path to the generated projectile asset.
    """
    # Use a random seed if none provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate projectile asset
    if output_filename is None:
        projectile_filename = f"{projectile_type.replace(' ', '_')}.png"
    else:
        projectile_filename = output_filename
    
    projectile_path = os.path.join(output_dir, projectile_filename)
    
    # Generate the projectile
    result = generate_game_asset(
        asset_type="projectile",
        description=f"isolated {projectile_type} projectile for {weapon_name}, simple pixel art icon, small projectile, no character, top-down view, small size",
        output_path=projectile_path,
        seed=seed,
        api_token=api_token,
        no_background=True,  # Explicitly ensure transparent background
        width=24,
        height=24
    )
    
    print(f"Generated projectile asset: {projectile_path}")
    return projectile_path

def generate_weapon_with_projectile(weapon_type, projectile_type=None, output_dir="src/assets/images/weapons", weapon_filename=None, projectile_filename=None, seed=None, api_token=None):
    """
    Generate a weapon asset and its projectile.
    
    Args:
        weapon_type (str): Type of weapon to generate (e.g., "sword", "bow", "wand").
        projectile_type (str, optional): Type of projectile to generate. If None, will use the weapon type.
        output_dir (str, optional): Directory to save the weapon asset to. Defaults to "src/assets/images/weapons".
        weapon_filename (str, optional): Filename to use for the weapon. If None, a filename will be generated from the weapon type.
        projectile_filename (str, optional): Filename to use for the projectile. If None, a filename will be generated from the projectile type.
        seed (int, optional): Seed for the generation process. If None, a random seed will be used.
        api_token (str, optional): PixelLab API token. If None, it will be read from the PIXELLAB_API_TOKEN environment variable.
        
    Returns:
        tuple: (weapon_path, projectile_path) - File paths to the generated weapon and projectile assets.
    """
    # Use a random seed if none provided
    if seed is None:
        seed = random.randint(1, 1000000)
    
    # Generate weapon
    weapon_path = generate_weapon_set(
        weapon_type=weapon_type,
        output_dir=output_dir,
        output_filename=weapon_filename,
        seed=seed,
        api_token=api_token
    )
    
    # Determine projectile type if not provided
    if projectile_type is None:
        if "bow" in weapon_type.lower():
            projectile_type = "arrow"
        elif "gun" in weapon_type.lower() or "pistol" in weapon_type.lower():
            projectile_type = "bullet"
        elif "wand" in weapon_type.lower() or "staff" in weapon_type.lower():
            projectile_type = "magic orb"
        elif "throw" in weapon_type.lower():
            projectile_type = weapon_type  # For throwable weapons, the projectile is the weapon itself
        else:
            projectile_type = f"{weapon_type} projectile"
    
    # Generate projectile
    projectile_path = generate_projectile(
        projectile_type=projectile_type,
        weapon_name=weapon_type,
        output_filename=projectile_filename,
        seed=seed + 1,  # Use a different but related seed
        api_token=api_token
    )
    
    return (weapon_path, projectile_path)

def main():
    """Main function to parse command-line arguments and generate pixel art."""
    parser = argparse.ArgumentParser(description="Generate pixel art game assets using the PixelLab API.")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Parser for the 'generate' command (original functionality)
    generate_parser = subparsers.add_parser("generate", help="Generate a single pixel art image")
    generate_parser.add_argument("--description", "-d", required=True, help="Text description of the image to generate")
    generate_parser.add_argument("--width", "-w", type=int, default=128, help="Width of the image in pixels (default: 128)")
    generate_parser.add_argument("--height", "-ht", type=int, default=128, help="Height of the image in pixels (default: 128)")
    generate_parser.add_argument("--output", "-o", help="Output file path for the generated image")
    generate_parser.add_argument("--negative", "-n", help="Text description of what to avoid in the generated image")
    generate_parser.add_argument("--outline", choices=["single color black outline", "single color outline", "selective outline", "lineless"], 
                        help="Outline style for the pixel art")
    generate_parser.add_argument("--shading", choices=["flat shading", "basic shading", "medium shading", "detailed shading", "highly detailed shading"], 
                        help="Shading style for the pixel art")
    generate_parser.add_argument("--detail", choices=["low detail", "medium detail", "highly detailed"], 
                        help="Detail level for the pixel art")
    generate_parser.add_argument("--view", choices=["side", "low top-down", "high top-down"], 
                        help="View perspective for the pixel art")
    generate_parser.add_argument("--direction", choices=["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"], 
                        help="Direction for the pixel art")
    generate_parser.add_argument("--isometric", action="store_true", help="Generate in isometric view")
    generate_parser.add_argument("--no-background", action="store_true", help="Generate with transparent background")
    generate_parser.add_argument("--seed", type=int, help="Seed for the generation process")
    generate_parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    generate_parser.add_argument("--guidance-scale", type=int, help="How closely to follow the text description (1-20)")
    
    # Parser for the 'asset' command (game asset generation)
    asset_parser = subparsers.add_parser("asset", help="Generate a game asset")
    asset_parser.add_argument("--type", "-t", required=True, 
                             choices=["character", "enemy", "weapon", "item", "environment", "effect"],
                             help="Type of asset to generate")
    asset_parser.add_argument("--description", "-d", required=True, help="Text description of the asset to generate")
    asset_parser.add_argument("--output", "-o", help="Output file path for the generated asset")
    asset_parser.add_argument("--width", "-w", type=int, help="Width of the asset in pixels")
    asset_parser.add_argument("--height", "-ht", type=int, help="Height of the asset in pixels")
    asset_parser.add_argument("--seed", type=int, help="Seed for the generation process")
    asset_parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    # Parser for the 'character-set' command
    character_set_parser = subparsers.add_parser("character-set", help="Generate a character asset")
    character_set_parser.add_argument("--description", "-d", required=True, help="Description of the character")
    character_set_parser.add_argument("--output-dir", "-o", default="src/assets/images", help="Directory to save the character asset to")
    character_set_parser.add_argument("--seed", type=int, help="Seed for the generation process")
    character_set_parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    # Parser for the 'character-animation' command
    character_animation_parser = subparsers.add_parser("character-animation", help="Generate a character animation")
    character_animation_parser.add_argument("--description", "-d", required=True, help="Description of the character")
    character_animation_parser.add_argument("--action", "-a", default="walk", help="Action for the animation (e.g., walk, run, attack)")
    character_animation_parser.add_argument("--view", "-v", default="side", choices=["side", "low top-down", "high top-down"], help="View perspective for the animation")
    character_animation_parser.add_argument("--direction", "-dir", default="east", 
                                          choices=["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"], 
                                          help="Direction for the animation")
    character_animation_parser.add_argument("--frames", "-f", type=int, default=4, help="Number of frames in the animation")
    character_animation_parser.add_argument("--reference", "-r", help="Path to the reference image")
    character_animation_parser.add_argument("--output-dir", "-o", default="src/assets/images/player", help="Directory to save the animation to")
    character_animation_parser.add_argument("--format", "-fmt", default="frames", choices=["spritesheet", "gif", "frames"], 
                                          help="Format to save the animation in")
    character_animation_parser.add_argument("--seed", type=int, help="Seed for the generation process")
    character_animation_parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    # Parser for the 'enemy-set' command
    enemy_set_parser = subparsers.add_parser("enemy-set", help="Generate a set of enemy assets")
    enemy_set_parser.add_argument("--type", "-t", required=True, help="Type of enemy to generate (e.g., zombie, skeleton)")
    enemy_set_parser.add_argument("--output-dir", "-o", default="src/assets/images", help="Directory to save the enemy assets to")
    enemy_set_parser.add_argument("--count", "-c", type=int, default=1, help="Number of variations to generate")
    enemy_set_parser.add_argument("--seed", type=int, help="Seed for the generation process")
    enemy_set_parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    # Parser for the 'enemy-animation' command
    enemy_animation_parser = subparsers.add_parser("enemy-animation", help="Generate an animated enemy")
    enemy_animation_parser.add_argument("--type", "-t", required=True, help="Type of enemy to generate (e.g., zombie, skeleton)")
    enemy_animation_parser.add_argument("--action", "-a", default="walk", help="Action for the animation (e.g., idle, attack, walk)")
    enemy_animation_parser.add_argument("--view", "-v", default="side", choices=["side", "low top-down", "high top-down"], help="View perspective for the animation")
    enemy_animation_parser.add_argument("--direction", "-d", default="east", 
                                      choices=["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"], 
                                      help="Direction for the animation")
    enemy_animation_parser.add_argument("--frames", "-f", type=int, default=4, help="Number of frames in the animation")
    enemy_animation_parser.add_argument("--reference", "-r", help="Path to the reference image (optional)")
    enemy_animation_parser.add_argument("--output-dir", "-o", default="src/assets/images/enemies", help="Directory to save the animation to")
    enemy_animation_parser.add_argument("--format", default="frames", choices=["spritesheet", "gif", "frames"], 
                                      help="Format to save the animation in")
    enemy_animation_parser.add_argument("--seed", type=int, help="Seed for the generation process")
    enemy_animation_parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    # Parser for the 'weapon-set' command
    weapon_set_parser = subparsers.add_parser("weapon-set", help="Generate a set of weapon assets")
    weapon_set_parser.add_argument("--type", "-t", required=True, help="Type of weapon to generate (e.g., sword, axe)")
    weapon_set_parser.add_argument("--output-dir", "-o", default="src/assets/images/weapons", help="Directory to save the weapon assets to")
    weapon_set_parser.add_argument("--output-filename", "-fn", help="Filename to use for the weapon")
    weapon_set_parser.add_argument("--seed", type=int, help="Seed for the generation process")
    weapon_set_parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    # Parser for the 'item-set' command
    item_set_parser = subparsers.add_parser("item-set", help="Generate a set of item assets with variations")
    item_set_parser.add_argument("--type", "-t", required=True, help="Type of item to generate (e.g., potion, coin, powerup)")
    item_set_parser.add_argument("--variations", "-v", nargs="+", default=["standard", "rare", "epic"], 
                               help="List of variations to generate (default: standard, rare, epic)")
    item_set_parser.add_argument("--output-dir", "-o", default="src/assets/images/items", help="Directory to save the item assets to")
    item_set_parser.add_argument("--seed", type=int, help="Seed for the generation process")
    item_set_parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    # Parser for the 'item' command
    item_parser = subparsers.add_parser("item", help="Generate a single item asset")
    item_parser.add_argument("--description", "-d", required=True, help="Description of the item to generate")
    item_parser.add_argument("--output-dir", "-o", default="src/assets/images/items", help="Directory to save the item asset to")
    item_parser.add_argument("--output-filename", "-fn", help="Filename to use for the item")
    item_parser.add_argument("--seed", type=int, help="Seed for the generation process")
    item_parser.add_argument("--token", help="PixelLab API token (overrides environment variable)")
    
    args = parser.parse_args()
    
    # Execute the appropriate command
    if args.command == "generate" or args.command is None:
        # Default to 'generate' if no command is specified
        result = generate_pixel_art(
            description=args.description if hasattr(args, 'description') else None,
            width=args.width if hasattr(args, 'width') else 128,
            height=args.height if hasattr(args, 'height') else 128,
            output_path=args.output if hasattr(args, 'output') else None,
            negative_description=args.negative if hasattr(args, 'negative') else None,
            outline=args.outline if hasattr(args, 'outline') else None,
            shading=args.shading if hasattr(args, 'shading') else None,
            detail=args.detail if hasattr(args, 'detail') else None,
            view=args.view if hasattr(args, 'view') else None,
            direction=args.direction if hasattr(args, 'direction') else None,
            isometric=args.isometric if hasattr(args, 'isometric') else False,
            no_background=args.no_background if hasattr(args, 'no_background') else False,
            seed=args.seed if hasattr(args, 'seed') else None,
            api_token=args.token if hasattr(args, 'token') else None,
            text_guidance_scale=args.guidance_scale if hasattr(args, 'guidance_scale') else None
        )
        
        # If no output path was provided, display the image
        if not hasattr(args, 'output') or not args.output:
            if hasattr(result, 'show'):
                result.show()
    
    elif args.command == "asset":
        result = generate_game_asset(
            asset_type=args.type,
            description=args.description,
            output_path=args.output,
            width=args.width,
            height=args.height,
            seed=args.seed,
            api_token=args.token
        )
        
        # If no output path was provided, display the image
        if not args.output and hasattr(result, 'show'):
            result.show()
    
    elif args.command == "character-set":
        character_path = generate_character_set(
            character_description=args.description,
            output_dir=args.output_dir,
            seed=args.seed,
            api_token=args.token
        )
    
    elif args.command == "character-animation":
        animation_path = generate_character_animation(
            character_description=args.description,
            action=args.action,
            view=args.view,
            direction=args.direction,
            n_frames=args.frames,
            reference_image_path=args.reference,
            output_dir=args.output_dir,
            output_format=args.format,
            seed=args.seed,
            api_token=args.token
        )
    
    elif args.command == "enemy-set":
        assets = generate_enemy_set(
            enemy_type=args.type,
            output_dir=args.output_dir,
            count=args.count,
            seed=args.seed,
            api_token=args.token
        )
        print(f"Generated {len(assets)} enemy variations")
    
    elif args.command == "enemy-animation":
        animation_path = generate_enemy_animation(
            enemy_type=args.type,
            action=args.action,
            view=args.view,
            direction=args.direction,
            n_frames=args.frames,
            reference_image_path=args.reference,
            output_dir=args.output_dir,
            output_format=args.format,
            seed=args.seed,
            api_token=args.token
        )
        print(f"Generated enemy animation: {animation_path}")
    
    elif args.command == "weapon-set":
        weapon_path = generate_weapon_set(
            weapon_type=args.type,
            output_dir=args.output_dir,
            output_filename=args.output_filename,
            seed=args.seed,
            api_token=args.token
        )
        print(f"Generated weapon asset: {weapon_path}")
    
    elif args.command == "item-set":
        item_assets = generate_item_set(
            item_type=args.type,
            variations=args.variations,
            output_dir=args.output_dir,
            seed=args.seed,
            api_token=args.token
        )
        print(f"Generated {len(item_assets)} item variations")
    
    elif args.command == "item":
        item_path = generate_item(
            item_description=args.description,
            output_dir=args.output_dir,
            output_filename=args.output_filename,
            seed=args.seed,
            api_token=args.token
        )
        print(f"Generated item asset: {item_path}")

if __name__ == "__main__":
    main() 