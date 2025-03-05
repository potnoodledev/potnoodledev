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
    
    // Weapons configuration
    this.weapons = {
      'rock': {
        name: 'Rock',
        damage: 20,
        fireRate: 1000, // ms between shots
        projectileSpeed: 300,
        projectileKey: 'rock', // The image key for the projectile
        projectileScale: 1,
        effectScale: 0,  // No effect for rock
        effectDuration: 0
      },
      'bow': {
        name: 'Bow',
        damage: 35,
        fireRate: 1500, // ms between shots
        projectileSpeed: 450,
        projectileKey: 'arrow', // The image key for the projectile
        projectileScale: 1,
        effectScale: 0.8, // Show the bow when firing
        effectDuration: 300
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
        rotation: true   // Axe rotates when thrown
      }
    };
    
    // Current weapon
    this.currentWeapon = 'rock';
    this.lastFired = 0;
    
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
    // Create a simple grid background
    const graphics = this.add.graphics();
    graphics.lineStyle(1, 0x333333, 0.8);
    
    // Draw vertical lines
    for (let x = 0; x <= this.mapWidth; x += 64) {
      graphics.moveTo(x, 0);
      graphics.lineTo(x, this.mapHeight);
    }
    
    // Draw horizontal lines
    for (let y = 0; y <= this.mapHeight; y += 64) {
      graphics.moveTo(0, y);
      graphics.lineTo(this.mapWidth, y);
    }
    
    graphics.strokePath();
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
      
      // Increase damage
      weapon.damage += weaponKey === 'bow' ? 8 : (weaponKey === 'axe' ? 10 : 5);
      
      // Improve fire rate
      const fireRateReduction = weaponKey === 'bow' ? 75 : (weaponKey === 'axe' ? 100 : 100);
      const minFireRate = weaponKey === 'bow' ? 300 : (weaponKey === 'axe' ? 500 : 200);
      weapon.fireRate = Math.max(minFireRate, weapon.fireRate - fireRateReduction);
    });
    
    // Unlock weapons at specific levels
    if (this.playerLevel === 3 && this.currentWeapon === 'rock') {
      this.currentWeapon = 'bow';
      this.events.emit('update-weapon', this.currentWeapon);
    } else if (this.playerLevel === 5) {
      this.currentWeapon = 'axe';
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
} 