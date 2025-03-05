import Phaser from 'phaser';

export default class GameScene extends Phaser.Scene {
  constructor() {
    super('GameScene');
    
    // Game state
    this.player = null;
    this.enemies = null;
    this.crystals = null;
    this.projectiles = null;
    this.joystick = null;
    this.joystickPointer = null;
    this.joystickKeys = null;
    
    // Player stats
    this.playerLevel = 1;
    this.playerXP = 0;
    this.playerMaxXP = 100;
    this.playerSpeed = 150;
    this.playerHealth = 100;
    this.playerMaxHealth = 100;
    
    // Weapons configuration - will be populated dynamically
    this.weapons = {};
    
    // Default weapon templates - used to create new weapons
    this.weaponTemplates = {
      'rock': {
        name: 'Rock',
        damage: 20,
        fireRate: 1000, // ms between shots
        projectileSpeed: 300,
        projectileKey: 'rock', // The image key for the projectile
        projectileScale: 1,
        effectScale: 0,  // No effect for rock
        effectDuration: 0,
        unlockLevel: 1
      },
      'bow': {
        name: 'Bow',
        damage: 35,
        fireRate: 1500, // ms between shots
        projectileSpeed: 450,
        projectileKey: 'arrow', // The image key for the projectile
        projectileScale: 1,
        effectScale: 0.8, // Show the bow when firing
        effectDuration: 300,
        unlockLevel: 3
      },
      'axe': {
        name: 'Throwing Axe',
        damage: 45,
        fireRate: 2000, // ms between shots
        projectileSpeed: 350,
        projectileKey: 'axe_projectile', // The image key for the projectile
        projectileScale: 1,
        effectScale: 0,  // No effect for axe (it is thrown)
        effectDuration: 0,
        rotation: true,   // Axe rotates when thrown
        unlockLevel: 5
      }
    };
    
    // Current weapon
    this.currentWeapon = null;
    this.lastFired = 0;
    
    // Available weapons (will be populated based on loaded assets)
    this.availableWeapons = [];
    
    // Game settings
    this.gameTime = 0;
    this.gameMaxTime = 600000; // 10 minutes in ms
    this.waveNumber = 1;
    this.enemiesPerWave = 5;
    this.enemySpawnRate = 3000; // ms between enemy spawns
    this.lastEnemySpawn = 0;
    this.enemySpeed = 75;
    this.enemyHealth = 50;
    this.enemyDamage = 10;
    
    // Map settings
    this.mapWidth = 1600;
    this.mapHeight = 1200;
  }

  init(data) {
    // Initialize weapons based on loaded assets
    if (data && data.loadedAssets) {
      this.configureWeapons(data.loadedAssets);
    }
  }

  create() {
    // Create game elements
    this.createBackground();
    this.createPlayer();
    
    // Create enemy animations
    this.anims.create({
      key: 'enemy_walk',
      frames: [
        { key: 'enemy_walk_1' },
        { key: 'enemy_walk_2' },
        { key: 'enemy_walk_3' },
        { key: 'enemy_walk_4' }
      ],
      frameRate: 8,
      repeat: -1
    });
    
    // Create game objects
    this.enemies = this.physics.add.group();
    this.crystals = this.physics.add.group();
    this.projectiles = this.physics.add.group();
    
    // Setup controls and collisions
    this.setupControls();
    this.setupCollisions();
    
    // Setup camera to follow player
    this.cameras.main.setBounds(0, 0, this.mapWidth, this.mapHeight);
    this.cameras.main.startFollow(this.player);
    
    // Setup game events
    this.events.on('player-level-up', this.onPlayerLevelUp, this);
    
    // Set world bounds
    this.physics.world.setBounds(0, 0, this.mapWidth, this.mapHeight);
    
    // Start game timer
    this.time.addEvent({
      delay: 1000,
      callback: this.updateGameTime,
      callbackScope: this,
      loop: true
    });
    
    // Start wave timer
    this.time.addEvent({
      delay: 30000, // 30 seconds between waves
      callback: this.increaseWave,
      callbackScope: this,
      loop: true
    });
    
    // Emit initial events to UI
    this.events.emit('update-player-health', this.playerHealth, this.playerMaxHealth);
    this.events.emit('update-player-xp', this.playerXP, this.playerMaxXP);
    this.events.emit('update-player-level', this.playerLevel);
    this.events.emit('update-game-time', this.gameTime, this.gameMaxTime);
    this.events.emit('update-wave', this.waveNumber);
    this.events.emit('update-weapon', this.currentWeapon);
  }

  update(time, delta) {
    // Handle player movement
    this.handlePlayerMovement();
    
    // Handle weapon firing
    this.handleWeaponFiring(time);
    
    // Spawn enemies
    this.handleEnemySpawning(time);
    
    // Update enemy movement
    this.updateEnemies();
  }

  createBackground() {
    // Create a tiled background using the generated terrain tiles
    
    // Create a group for the background tiles
    this.backgroundTiles = this.add.group();
    
    // Tile size (assuming 32x32 pixels)
    const tileSize = 32;
    
    // Calculate number of tiles needed
    const tilesX = Math.ceil(this.mapWidth / tileSize);
    const tilesY = Math.ceil(this.mapHeight / tileSize);
    
    // Create a 2D array to represent the terrain map
    this.terrainMap = this.createTerrainMap(tilesX, tilesY);
    
    // Place tiles based on the terrain map
    for (let y = 0; y < tilesY; y++) {
      for (let x = 0; x < tilesX; x++) {
        const terrainType = this.terrainMap[y][x];
        
        // Randomly select a variation (1-3) of this terrain type
        const variation = Math.floor(Math.random() * 3) + 1;
        const tileKey = `${terrainType}_${variation}`;
        
        // Create the tile sprite
        const tile = this.add.sprite(
          x * tileSize + tileSize / 2,
          y * tileSize + tileSize / 2,
          tileKey
        );
        
        // Add to the background group
        this.backgroundTiles.add(tile);
      }
    }
  }
  
  createTerrainMap(width, height) {
    // Create a 2D array filled with the default terrain (grass)
    const map = Array(height).fill().map(() => Array(width).fill('grass'));
    
    // Add some terrain variety
    // This is a simple implementation - could be expanded with more complex terrain generation
    
    // Add a desert area
    this.addTerrainArea(map, 'desert', 0.2, 0.2, 0.3, 0.3);
    
    // Add a water area (like a lake or river)
    this.addTerrainArea(map, 'water', 0.6, 0.4, 0.2, 0.4);
    
    // Add some stone patches
    this.addTerrainArea(map, 'stone', 0.1, 0.7, 0.15, 0.15);
    this.addTerrainArea(map, 'stone', 0.8, 0.1, 0.1, 0.1);
    
    return map;
  }
  
  addTerrainArea(map, terrainType, centerX, centerY, sizeX, sizeY) {
    // Convert relative positions to actual indices
    const centerXIdx = Math.floor(centerX * map[0].length);
    const centerYIdx = Math.floor(centerY * map.length);
    const sizeXTiles = Math.floor(sizeX * map[0].length);
    const sizeYTiles = Math.floor(sizeY * map.length);
    
    // Calculate area boundaries
    const startX = Math.max(0, centerXIdx - Math.floor(sizeXTiles / 2));
    const endX = Math.min(map[0].length - 1, centerXIdx + Math.floor(sizeXTiles / 2));
    const startY = Math.max(0, centerYIdx - Math.floor(sizeYTiles / 2));
    const endY = Math.min(map.length - 1, centerYIdx + Math.floor(sizeYTiles / 2));
    
    // Fill the area with the specified terrain type
    for (let y = startY; y <= endY; y++) {
      for (let x = startX; x <= endX; x++) {
        // Add some randomness to the edges for a more natural look
        const distFromCenterX = Math.abs(x - centerXIdx) / (sizeXTiles / 2);
        const distFromCenterY = Math.abs(y - centerYIdx) / (sizeYTiles / 2);
        const distFromCenter = Math.sqrt(distFromCenterX * distFromCenterX + distFromCenterY * distFromCenterY);
        
        // Apply terrain with higher probability near the center
        if (Math.random() > distFromCenter * 0.8) {
          map[y][x] = terrainType;
        }
      }
    }
  }

  createPlayer() {
    // Create player at center of map
    this.player = this.physics.add.sprite(
      this.mapWidth / 2,
      this.mapHeight / 2,
      'player'
    );
    
    // Set player properties
    this.player.setCollideWorldBounds(true);
    this.player.setSize(48, 48);
    this.player.setDepth(10);
    this.player.body.setCircle(24);
    this.player.setFlipX(false); // Default facing right
    
    // Create player animations
    this.anims.create({
      key: 'player_walk',
      frames: [
        { key: 'player_walk_1' },
        { key: 'player_walk_2' },
        { key: 'player_walk_3' },
        { key: 'player_walk_4' }
      ],
      frameRate: 8,
      repeat: -1
    });
    
    // Add player data
    this.player.health = this.playerHealth;
  }

  setupControls() {
    // Set up keyboard controls
    this.joystickKeys = this.input.keyboard.addKeys({
      up: Phaser.Input.Keyboard.KeyCodes.W,
      down: Phaser.Input.Keyboard.KeyCodes.S,
      left: Phaser.Input.Keyboard.KeyCodes.A,
      right: Phaser.Input.Keyboard.KeyCodes.D
    });
    
    // Set up touch/mouse controls
    this.input.on('pointerdown', (pointer) => {
      this.joystickPointer = pointer;
      this.joystick = this.add.image(pointer.x, pointer.y, 'joystick');
      this.joystick.setScrollFactor(0);
      this.joystick.setDepth(100);
      this.joystick.setAlpha(0.7);
    });
    
    this.input.on('pointermove', (pointer) => {
      if (this.joystickPointer && this.joystickPointer.id === pointer.id) {
        // Update joystick position
      }
    });
    
    this.input.on('pointerup', (pointer) => {
      if (this.joystickPointer && this.joystickPointer.id === pointer.id) {
        this.joystickPointer = null;
        if (this.joystick) {
          this.joystick.destroy();
          this.joystick = null;
        }
      }
    });
  }

  setupCollisions() {
    // Player collisions
    this.physics.add.overlap(
      this.player,
      this.enemies,
      this.enemyHitPlayer,
      null,
      this
    );
    
    this.physics.add.overlap(
      this.player,
      this.crystals,
      this.collectCrystal,
      null,
      this
    );
    
    // Weapon collisions
    this.physics.add.overlap(
      this.projectiles,
      this.enemies,
      this.projectileHitEnemy,
      null,
      this
    );
  }

  handlePlayerMovement() {
    // Reset velocity
    this.player.setVelocity(0);
    
    let dirX = 0;
    let dirY = 0;
    
    // Handle keyboard input
    if (this.joystickKeys.left.isDown) {
      dirX = -1;
    } else if (this.joystickKeys.right.isDown) {
      dirX = 1;
    }
    
    if (this.joystickKeys.up.isDown) {
      dirY = -1;
    } else if (this.joystickKeys.down.isDown) {
      dirY = 1;
    }
    
    // Handle touch/mouse input
    if (this.joystickPointer && this.joystick) {
      const dx = this.joystickPointer.x - this.joystick.x;
      const dy = this.joystickPointer.y - this.joystick.y;
      
      if (Math.abs(dx) > 10 || Math.abs(dy) > 10) {
        const distance = Math.sqrt(dx * dx + dy * dy);
        dirX = dx / distance;
        dirY = dy / distance;
      }
    }
    
    // Normalize and apply velocity
    if (dirX !== 0 || dirY !== 0) {
      const length = Math.sqrt(dirX * dirX + dirY * dirY);
      dirX = dirX / length;
      dirY = dirY / length;
      
      this.player.setVelocity(
        dirX * this.playerSpeed,
        dirY * this.playerSpeed
      );
      
      // Play walk animation when moving
      if (!this.player.anims.isPlaying) {
        this.player.play('player_walk');
      }
      
      // Flip player sprite based on horizontal movement direction
      if (dirX < 0) {
        // Moving left, flip sprite
        this.player.setFlipX(true);
      } else if (dirX > 0) {
        // Moving right, don't flip sprite
        this.player.setFlipX(false);
      }
      // If only moving vertically, keep current flip state
    } else {
      // Stop animation when not moving
      if (this.player.anims.isPlaying) {
        this.player.anims.stop();
        this.player.setTexture('player');
      }
    }
  }

  handleWeaponFiring(time) {
    // Get the current weapon's configuration
    const weaponConfig = this.weapons[this.currentWeapon];
    
    if (time > this.lastFired + weaponConfig.fireRate) {
      const nearestEnemy = this.findNearestEnemy();
      
      if (nearestEnemy) {
        // Make player face the enemy when firing
        if (nearestEnemy.x < this.player.x) {
          // Enemy is to the left, face left
          this.player.setFlipX(true);
        } else {
          // Enemy is to the right, face right
          this.player.setFlipX(false);
        }
        
        this.fireWeapon(nearestEnemy, weaponConfig);
        this.lastFired = time;
      }
    }
  }

  findNearestEnemy() {
    let nearestEnemy = null;
    let nearestDistance = Infinity;
    
    this.enemies.getChildren().forEach((enemy) => {
      const distance = Phaser.Math.Distance.Between(
        this.player.x, this.player.y,
        enemy.x, enemy.y
      );
      
      if (distance < nearestDistance) {
        nearestDistance = distance;
        nearestEnemy = enemy;
      }
    });
    
    return nearestEnemy;
  }

  fireWeapon(target, weaponConfig) {
    // Create projectile
    const projectile = this.projectiles.create(this.player.x, this.player.y, weaponConfig.projectileKey);
    projectile.setDepth(5);
    projectile.setScale(weaponConfig.projectileScale);
    
    // Set weapon type for collision handling
    projectile.weaponType = this.currentWeapon;
    
    // Calculate direction to target
    const dx = target.x - this.player.x;
    const dy = target.y - this.player.y;
    const angle = Math.atan2(dy, dx);
    
    // Set projectile properties
    projectile.rotation = angle;
    projectile.damage = weaponConfig.damage;
    
    // Add rotation animation for certain weapons (like axes)
    if (weaponConfig.rotation) {
      this.tweens.add({
        targets: projectile,
        rotation: angle + Math.PI * 4, // Rotate 720 degrees (2 full rotations)
        duration: 1000,
        repeat: -1
      });
    }
    
    // Add a visual effect when firing if configured
    if (weaponConfig.effectScale > 0) {
      const weaponEffect = this.add.image(this.player.x, this.player.y, this.currentWeapon);
      weaponEffect.setDepth(4);
      weaponEffect.setScale(weaponConfig.effectScale);
      weaponEffect.rotation = angle;
      
      // Fade out and remove the weapon effect
      this.tweens.add({
        targets: weaponEffect,
        alpha: 0,
        duration: weaponConfig.effectDuration,
        onComplete: () => {
          weaponEffect.destroy();
        }
      });
    }
    
    // Set velocity
    projectile.setVelocity(
      Math.cos(angle) * weaponConfig.projectileSpeed,
      Math.sin(angle) * weaponConfig.projectileSpeed
    );
    
    // Destroy projectile after 2 seconds
    this.time.delayedCall(2000, () => {
      if (projectile.active) {
        projectile.destroy();
      }
    });
  }

  handleEnemySpawning(time) {
    if (time > this.lastEnemySpawn + this.enemySpawnRate) {
      this.spawnEnemy();
      this.lastEnemySpawn = time;
    }
  }

  spawnEnemy() {
    // Determine spawn position (outside camera view)
    const side = Phaser.Math.Between(0, 3); // 0: top, 1: right, 2: bottom, 3: left
    let x, y;
    
    const cameraX = this.cameras.main.scrollX;
    const cameraY = this.cameras.main.scrollY;
    const cameraWidth = this.cameras.main.width;
    const cameraHeight = this.cameras.main.height;
    
    const buffer = 100; // Spawn outside camera view
    
    switch (side) {
      case 0: // Top
        x = Phaser.Math.Between(cameraX - buffer, cameraX + cameraWidth + buffer);
        y = cameraY - buffer;
        break;
      case 1: // Right
        x = cameraX + cameraWidth + buffer;
        y = Phaser.Math.Between(cameraY - buffer, cameraY + cameraHeight + buffer);
        break;
      case 2: // Bottom
        x = Phaser.Math.Between(cameraX - buffer, cameraX + cameraWidth + buffer);
        y = cameraY + cameraHeight + buffer;
        break;
      case 3: // Left
        x = cameraX - buffer;
        y = Phaser.Math.Between(cameraY - buffer, cameraY + cameraHeight + buffer);
        break;
    }
    
    // Ensure spawn is within world bounds
    x = Phaser.Math.Clamp(x, 0, this.mapWidth);
    y = Phaser.Math.Clamp(y, 0, this.mapHeight);
    
    // Create enemy
    const enemy = this.enemies.create(x, y, 'enemy');
    enemy.setDepth(5);
    
    // Set enemy properties
    enemy.health = this.enemyHealth;
    enemy.damage = this.enemyDamage;
    enemy.speed = this.enemySpeed;
    enemy.setSize(40, 40);
    enemy.body.setCircle(20);
    
    // Play walk animation
    enemy.play('enemy_walk');
  }

  updateEnemies() {
    this.enemies.getChildren().forEach((enemy) => {
      // Move towards player
      const dx = this.player.x - enemy.x;
      const dy = this.player.y - enemy.y;
      const angle = Math.atan2(dy, dx);
      
      // We don't need rotation since we're using sprites now
      // enemy.rotation = angle;
      
      enemy.setVelocity(
        Math.cos(angle) * enemy.speed,
        Math.sin(angle) * enemy.speed
      );
      
      // Flip enemy sprite based on player position
      if (this.player.x < enemy.x) {
        // Player is to the left, face left
        enemy.setFlipX(true);
      } else {
        // Player is to the right, face right
        enemy.setFlipX(false);
      }
    });
  }

  collectCrystal(player, crystal) {
    crystal.destroy();
    
    // Add XP
    this.playerXP += 40;
    
    // Check for level up
    if (this.playerXP >= this.playerMaxXP) {
      this.playerXP -= this.playerMaxXP;
      this.events.emit('player-level-up');
    }
    
    // Update UI
    this.events.emit('update-player-xp', this.playerXP, this.playerMaxXP);
  }

  projectileHitEnemy(projectile, enemy) {
    // Apply damage
    enemy.health -= projectile.damage;
    
    // Destroy projectile
    projectile.destroy();
    
    // Check if enemy is defeated
    if (enemy.health <= 0) {
      // Spawn crystal
      this.spawnCrystal(enemy.x, enemy.y);
      
      // Destroy enemy
      enemy.destroy();
    }
  }

  spawnCrystal(x, y) {
    const crystal = this.crystals.create(x, y, 'crystal');
    crystal.setDepth(3);
  }

  enemyHitPlayer(player, enemy) {
    // Apply damage to player (only once per second)
    if (this.time.now - (player.lastDamageTime || 0) > 1000) {
      player.health -= enemy.damage;
      player.lastDamageTime = this.time.now;
      
      // Update UI
      this.events.emit('update-player-health', player.health, this.playerMaxHealth);
      
      // Flash player to indicate damage
      this.tweens.add({
        targets: player,
        alpha: 0.5,
        duration: 100,
        yoyo: true,
        repeat: 3
      });
      
      // Check for game over
      if (player.health <= 0) {
        this.gameOver();
      }
    }
  }

  onPlayerLevelUp() {
    // Increase player level
    this.playerLevel++;
    
    // Increase player stats
    this.playerMaxHealth += 20;
    this.playerHealth = this.playerMaxHealth;
    this.playerSpeed += 10;
    
    // Increase weapon stats
    Object.keys(this.weapons).forEach(weaponKey => {
      const weapon = this.weapons[weaponKey];
      
      // Increase damage based on weapon type
      if (weaponKey === 'bow') {
        weapon.damage += 8;
      } else if (weaponKey === 'axe') {
        weapon.damage += 10;
      } else {
        weapon.damage += 5;
      }
      
      // Improve fire rate based on weapon type
      let fireRateReduction = 100;
      let minFireRate = 200;
      
      if (weaponKey === 'bow') {
        fireRateReduction = 75;
        minFireRate = 300;
      } else if (weaponKey === 'axe') {
        fireRateReduction = 100;
        minFireRate = 500;
      }
      
      weapon.fireRate = Math.max(minFireRate, weapon.fireRate - fireRateReduction);
    });
    
    // Check for weapon unlocks
    let newWeaponUnlocked = false;
    this.availableWeapons.forEach(weaponKey => {
      const weapon = this.weapons[weaponKey];
      if (weapon.unlockLevel === this.playerLevel) {
        this.currentWeapon = weaponKey;
        newWeaponUnlocked = true;
        console.log(`Unlocked new weapon: ${weapon.name}`);
      }
    });
    
    // Update UI if weapon changed
    if (newWeaponUnlocked) {
      this.events.emit('update-weapon', this.currentWeapon);
    }
    
    // Increase XP required for next level
    this.playerMaxXP += 50;
    
    // Update UI
    this.events.emit('update-player-level', this.playerLevel);
    this.events.emit('update-player-health', this.playerHealth, this.playerMaxHealth);
    this.events.emit('update-player-xp', this.playerXP, this.playerMaxXP);
  }

  increaseWave() {
    // Increase wave number
    this.waveNumber++;
    
    // Increase enemy stats
    this.enemyHealth += 10;
    this.enemyDamage += 2;
    this.enemySpeed += 5;
    
    // Increase spawn rate
    this.enemiesPerWave += 2;
    this.enemySpawnRate = Math.max(500, this.enemySpawnRate - 300);
    
    // Update UI
    this.events.emit('update-wave', this.waveNumber);
  }

  updateGameTime() {
    // Increase game time
    this.gameTime += 1000;
    
    // Update UI
    this.events.emit('update-game-time', this.gameTime, this.gameMaxTime);
    
    // Check for victory
    if (this.gameTime >= this.gameMaxTime) {
      this.victory();
    }
  }

  gameOver() {
    // Stop physics
    this.physics.pause();
    
    // Switch to game over scene
    this.scene.start('GameOverScene', { 
      victory: false, 
      level: this.playerLevel,
      time: this.gameTime
    });
  }

  victory() {
    // Stop physics
    this.physics.pause();
    
    // Switch to game over scene
    this.scene.start('GameOverScene', { 
      victory: true, 
      level: this.playerLevel,
      time: this.gameTime
    });
  }

  configureWeapons(loadedAssets) {
    // Clear existing weapons
    this.weapons = {};
    this.availableWeapons = [];
    
    // Process loaded weapons
    loadedAssets.weapons.forEach(weaponKey => {
      // Check if we have a template for this weapon
      if (this.weaponTemplates[weaponKey]) {
        // Create a copy of the template
        this.weapons[weaponKey] = { ...this.weaponTemplates[weaponKey] };
        
        // Add to available weapons
        this.availableWeapons.push(weaponKey);
      } else {
        // Create a generic weapon configuration if no template exists
        this.weapons[weaponKey] = {
          name: weaponKey.charAt(0).toUpperCase() + weaponKey.slice(1),
          damage: 30,
          fireRate: 1200,
          projectileSpeed: 350,
          projectileKey: weaponKey, // Default to using the weapon itself as projectile
          projectileScale: 1,
          effectScale: 0,
          effectDuration: 0,
          unlockLevel: 1 // Available from the start
        };
        
        // Add to available weapons
        this.availableWeapons.push(weaponKey);
      }
    });
    
    // Match projectiles with weapons
    loadedAssets.projectiles.forEach(projectile => {
      if (this.weapons[projectile.weapon]) {
        this.weapons[projectile.weapon].projectileKey = projectile.key;
      }
    });
    
    // Set initial weapon
    if (this.availableWeapons.length > 0) {
      // Find the lowest level weapon
      let lowestLevelWeapon = this.availableWeapons[0];
      let lowestLevel = this.weapons[lowestLevelWeapon].unlockLevel || 1;
      
      this.availableWeapons.forEach(weaponKey => {
        const weaponLevel = this.weapons[weaponKey].unlockLevel || 1;
        if (weaponLevel < lowestLevel) {
          lowestLevel = weaponLevel;
          lowestLevelWeapon = weaponKey;
        }
      });
      
      this.currentWeapon = lowestLevelWeapon;
    } else {
      console.warn('No weapons available!');
    }
    
    console.log('Configured weapons:', this.weapons);
    console.log('Current weapon:', this.currentWeapon);
  }
} 