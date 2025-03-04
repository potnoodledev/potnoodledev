import Phaser from 'phaser';

export default class GameScene extends Phaser.Scene {
  constructor() {
    super('GameScene');
    
    // Game state
    this.player = null;
    this.enemies = null;
    this.crystals = null;
    this.rocks = null;
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
    
    // Weapon stats
    this.weaponDamage = 20;
    this.weaponFireRate = 1000; // ms between shots
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
    // Create world bounds
    this.physics.world.setBounds(0, 0, this.mapWidth, this.mapHeight);
    
    // Create background
    this.createBackground();
    
    // Create player
    this.createPlayer();
    
    // Create groups
    this.enemies = this.physics.add.group();
    this.crystals = this.physics.add.group();
    this.rocks = this.physics.add.group();
    
    // Set up collisions
    this.setupCollisions();
    
    // Set up camera
    this.cameras.main.setBounds(0, 0, this.mapWidth, this.mapHeight);
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);
    
    // Set up controls
    this.setupControls();
    
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
    
    // Register events
    this.events.on('player-level-up', this.onPlayerLevelUp, this);
    
    // Emit initial events to UI
    this.events.emit('update-player-health', this.playerHealth, this.playerMaxHealth);
    this.events.emit('update-player-xp', this.playerXP, this.playerMaxXP);
    this.events.emit('update-player-level', this.playerLevel);
    this.events.emit('update-game-time', this.gameTime, this.gameMaxTime);
    this.events.emit('update-wave', this.waveNumber);
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
    // Player collects crystals
    this.physics.add.overlap(
      this.player,
      this.crystals,
      this.collectCrystal,
      null,
      this
    );
    
    // Rocks hit enemies
    this.physics.add.overlap(
      this.rocks,
      this.enemies,
      this.rockHitEnemy,
      null,
      this
    );
    
    // Enemies hit player
    this.physics.add.overlap(
      this.player,
      this.enemies,
      this.enemyHitPlayer,
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
    }
  }

  handleWeaponFiring(time) {
    if (time > this.lastFired + this.weaponFireRate) {
      const nearestEnemy = this.findNearestEnemy();
      
      if (nearestEnemy) {
        this.fireRock(nearestEnemy);
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

  fireRock(target) {
    const rock = this.rocks.create(this.player.x, this.player.y, 'rock');
    rock.setDepth(5);
    
    // Calculate direction to target
    const dx = target.x - this.player.x;
    const dy = target.y - this.player.y;
    const angle = Math.atan2(dy, dx);
    
    // Set rock properties
    rock.rotation = angle;
    rock.damage = this.weaponDamage;
    
    // Set velocity
    const speed = 300;
    rock.setVelocity(
      Math.cos(angle) * speed,
      Math.sin(angle) * speed
    );
    
    // Destroy rock after 2 seconds
    this.time.delayedCall(2000, () => {
      if (rock.active) {
        rock.destroy();
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
  }

  updateEnemies() {
    this.enemies.getChildren().forEach((enemy) => {
      // Move towards player
      const dx = this.player.x - enemy.x;
      const dy = this.player.y - enemy.y;
      const angle = Math.atan2(dy, dx);
      
      enemy.rotation = angle;
      
      enemy.setVelocity(
        Math.cos(angle) * enemy.speed,
        Math.sin(angle) * enemy.speed
      );
    });
  }

  collectCrystal(player, crystal) {
    crystal.destroy();
    
    // Add XP
    this.playerXP += 10;
    
    // Check for level up
    if (this.playerXP >= this.playerMaxXP) {
      this.playerXP -= this.playerMaxXP;
      this.events.emit('player-level-up');
    }
    
    // Update UI
    this.events.emit('update-player-xp', this.playerXP, this.playerMaxXP);
  }

  rockHitEnemy(rock, enemy) {
    // Apply damage
    enemy.health -= rock.damage;
    
    // Destroy rock
    rock.destroy();
    
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
    this.weaponDamage += 5;
    this.weaponFireRate = Math.max(200, this.weaponFireRate - 100);
    
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