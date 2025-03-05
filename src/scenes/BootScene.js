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
    // Display loading text
    const loadingText = this.add.text(
      this.cameras.main.width / 2,
      this.cameras.main.height / 2 - 50,
      'Loading...',
      {
        font: '20px Arial',
        fill: '#ffffff'
      }
    );
    loadingText.setOrigin(0.5);

    // Create loading bar
    const progressBar = this.add.graphics();
    const progressBox = this.add.graphics();
    progressBox.fillStyle(0x222222, 0.8);
    progressBox.fillRect(
      this.cameras.main.width / 2 - 160,
      this.cameras.main.height / 2,
      320,
      50
    );

    // Loading progress events
    this.load.on('progress', (value) => {
      progressBar.clear();
      progressBar.fillStyle(0xffffff, 1);
      progressBar.fillRect(
        this.cameras.main.width / 2 - 150,
        this.cameras.main.height / 2 + 10,
        300 * value,
        30
      );
    });

    this.load.on('complete', () => {
      progressBar.destroy();
      progressBox.destroy();
      loadingText.destroy();
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
    
    // Dynamically load weapons
    this.loadWeapons();
    
    // Dynamically load projectiles
    this.loadProjectiles();
    
    // Dynamically load items
    this.loadItems();
  }

  create() {
    console.log('Loaded weapons:', this.loadedAssets.weapons);
    console.log('Loaded projectiles:', this.loadedAssets.projectiles);
    console.log('Loaded items:', this.loadedAssets.items);
    
    // Pass loaded assets to the GameScene
    this.scene.start('GameScene', { loadedAssets: this.loadedAssets });
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
      
      // Load the item image (already loaded above, but included for completeness)
      if (key !== 'crystal') { // Skip crystal as it's already loaded
        this.load.image(key, path);
      }
      
      // Add to loaded items list
      this.loadedAssets.items.push(key);
    });
  }
} 