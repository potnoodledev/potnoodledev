import Phaser from 'phaser';

export default class BootScene extends Phaser.Scene {
  constructor() {
    super('BootScene');
    
    // Asset directories to scan
    this.assetDirectories = {
      characters: 'assets/images/player',
      enemies: 'assets/images/enemies',
      weapons: 'assets/images/weapons',
      projectiles: 'assets/images/weapons/projectiles',
      items: 'assets/images/items'
    };
    
    // Store loaded assets for reference by other scenes
    this.loadedAssets = {
      weapons: [],
      projectiles: [],
      items: []
    };
  }

  preload() {
    // Create loading bar
    const progressBar = this.add.graphics();
    const progressBox = this.add.graphics();
    progressBox.fillStyle(0x222222, 0.8);
    progressBox.fillRect(240, 270, 320, 50);
    
    const width = this.cameras.main.width;
    const height = this.cameras.main.height;
    const loadingText = this.add.text(width / 2, height / 2 - 50, 'Loading...', {
      font: '20px monospace',
      fill: '#ffffff'
    });
    loadingText.setOrigin(0.5, 0.5);
    
    // Update loading bar as assets are loaded
    this.load.on('progress', (value) => {
      progressBar.clear();
      progressBar.fillStyle(0xffffff, 1);
      progressBar.fillRect(250, 280, 300 * value, 30);
    });
    
    this.load.on('complete', () => {
      progressBar.destroy();
      progressBox.destroy();
      loadingText.destroy();
    });

    // Load tile files list first
    this.load.json('tileFiles', 'assets/images/tiles/tileFiles.json');
    
    // Add debug callbacks for the tileFiles.json
    this.load.on('filecomplete-json-tileFiles', (key, type, data) => {
      console.log('Successfully loaded tileFiles.json:', data);
      
      // Immediately load all tile images once the JSON is loaded
      if (data && data.files) {
        data.files.forEach(file => {
          const key = file.replace('.png', '');
          const path = `assets/images/tiles/${file}`;
          console.log(`Loading tile image: ${key} from ${path}`);
          this.load.image(key, path);
        });
      }
    });
    
    this.load.on('loaderror', (file) => {
      console.error('Error loading file:', file.key, file.url);
    });

    // Load core game assets
    this.load.image('player', 'assets/images/player.png');
    this.load.image('enemy', 'assets/images/enemy.png');
    this.load.image('crystal', 'assets/images/items/crystal.png');
    this.load.svg('joystick', 'assets/images/joystick.svg');
    
    // Load player animations
    this.load.image('player_walk_1', 'assets/images/player/walk/frame_1.png');
    this.load.image('player_walk_2', 'assets/images/player/walk/frame_2.png');
    this.load.image('player_walk_3', 'assets/images/player/walk/frame_3.png');
    this.load.image('player_walk_4', 'assets/images/player/walk/frame_4.png');
    
    // Load enemy animations
    this.load.image('enemy_walk_1', 'assets/images/enemies/walk/frame_1.png');
    this.load.image('enemy_walk_2', 'assets/images/enemies/walk/frame_2.png');
    this.load.image('enemy_walk_3', 'assets/images/enemies/walk/frame_3.png');
    this.load.image('enemy_walk_4', 'assets/images/enemies/walk/frame_4.png');
    
    // Load weapons, projectiles, and items
    this.loadWeapons();
    this.loadProjectiles();
    this.loadItems();
    
    // We'll load terrain tiles in the create method after tileFiles.json is loaded
  }

  create() {
    console.log('BootScene create method called');
    
    // Extract terrain types from the loaded tiles
    this.tileTypes = [];
    const tileFiles = this.cache.json.get('tileFiles');
    
    if (tileFiles && tileFiles.files) {
      console.log('Processing tile files:', tileFiles.files);
      
      // Define a function to extract terrain type from filename
      const getTerrainType = (filename) => {
        const match = filename.match(/^([a-z_]+)_(\d+|pattern)\.png$/);
        return match ? match[1] : null;
      };
      
      // Process each file to extract terrain types
      tileFiles.files.forEach(file => {
        const terrainType = getTerrainType(file);
        if (terrainType && !this.tileTypes.includes(terrainType)) {
          this.tileTypes.push(terrainType);
          console.log(`Added terrain type: ${terrainType}`);
        }
      });
    }
    
    console.log('Loaded weapons:', this.loadedAssets.weapons);
    console.log('Loaded projectiles:', this.loadedAssets.projectiles);
    console.log('Loaded items:', this.loadedAssets.items);
    console.log('Loaded terrain types:', this.tileTypes);
    
    // Make sure we have at least one terrain type
    if (!this.tileTypes || this.tileTypes.length === 0) {
      console.warn('No terrain types were loaded, using fallback');
      // Extract terrain type from the tileFiles.json directly as a fallback
      const tileFiles = this.cache.json.get('tileFiles');
      if (tileFiles && tileFiles.files && tileFiles.files.length > 0) {
        console.log('Attempting to extract terrain types from tileFiles:', tileFiles.files);
        const getTerrainType = (filename) => {
          const match = filename.match(/^([a-z_]+)_(\d+|pattern)\.png$/);
          return match ? match[1] : null;
        };
        
        const extractedTypes = tileFiles.files
          .map(file => getTerrainType(file))
          .filter(type => type !== null);
          
        // Get unique terrain types
        this.tileTypes = [...new Set(extractedTypes)];
        console.log('Extracted terrain types as fallback:', this.tileTypes);
      }
    }
    
    // Verify that all tile textures are loaded
    if (this.tileTypes && this.tileTypes.length > 0) {
      this.tileTypes.forEach(terrainType => {
        for (let i = 1; i <= 3; i++) {
          const key = `${terrainType}_${i}`;
          console.log(`Checking if texture ${key} is loaded:`, this.textures.exists(key));
        }
        const patternKey = `${terrainType}_pattern`;
        console.log(`Checking if texture ${patternKey} is loaded:`, this.textures.exists(patternKey));
      });
    }
    
    // Pass loaded assets to the GameScene
    console.log('Starting GameScene with terrain types:', this.tileTypes);
    this.scene.start('GameScene', { 
      loadedAssets: this.loadedAssets,
      tileTypes: this.tileTypes 
    });
    this.scene.launch('UIScene');
  }
  
  loadWeapons() {
    // In a real implementation, this would scan the directory
    // For now, we'll manually define the weapons we know exist
    const weapons = ['rock', 'bow', 'axe'];
    
    weapons.forEach(weapon => {
      const key = weapon;
      const path = `assets/images/weapons/${weapon}.png`;
      
      // Load the weapon image
      this.load.image(key, path);
      
      // Add to loaded weapons list
      this.loadedAssets.weapons.push(key);
    });
  }
  
  loadProjectiles() {
    // In a real implementation, this would scan the directory
    // For now, we'll manually define the projectiles we know exist
    const projectiles = [
      { key: 'arrow', weapon: 'bow' },
      { key: 'axe_projectile', weapon: 'axe', file: 'axe.png' }
    ];
    
    projectiles.forEach(projectile => {
      const key = projectile.key;
      const filename = projectile.file || `${projectile.key}.png`;
      const path = `assets/images/weapons/projectiles/${filename}`;
      
      // Load the projectile image
      this.load.image(key, path);
      
      // Add to loaded projectiles list with weapon association
      this.loadedAssets.projectiles.push({
        key: key,
        weapon: projectile.weapon
      });
    });
  }
  
  loadItems() {
    // In a real implementation, this would scan the directory
    // For now, we'll manually define the items we know exist
    const items = ['crystal'];
    
    items.forEach(item => {
      const key = item;
      const path = `assets/images/items/${item}.png`;
      
      // Add to loaded items list
      this.loadedAssets.items.push(key);
    });
  }
} 