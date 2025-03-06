import Phaser from 'phaser';
import axios from 'axios';

export default class GameScene extends Phaser.Scene {
  constructor() {
    super('GameScene');
    
    // Game state
    this.player = null;
    this.joystick = null;
    this.joystickPointer = null;
    this.joystickKeys = null;
    
    // Player stats
    this.playerSpeed = 150;
    
    // Manifesto text
    this.manifestoText = '';
    this.manifestoLines = [];
    this.textObjects = [];
    
    // Map settings
    this.mapWidth = 1600;
    this.mapHeight = 2000;
    
    // Evolution history
    this.evolutionHistory = [];

    // Items system
    this.items = null;
    this.itemsCollected = 0;
    this.totalItems = 0;
  }

  init() {
    // Nothing to initialize
  }

  preload() {
    // Load manifesto text
    this.load.text('manifesto', 'assets/manifesto.txt');
    
    // Try to load commit history if it exists
    try {
      this.load.json('commit-history', 'assets/commit-history.json');
    } catch (error) {
      console.log('No commit history found, will create one if needed');
    }
  }

  create() {
    // Set background to black
    this.cameras.main.setBackgroundColor('#000000');
    
    // Load manifesto text
    this.manifestoText = this.cache.text.get('manifesto');
    this.manifestoLines = this.manifestoText.split('\n');
    
    // Create player animations
    this.createPlayerAnimations();
    
    // Create the manifesto as part of the game world
    this.createManifestoWorld();
    
    // Create player
    this.player = this.physics.add.sprite(this.mapWidth / 2, 250, 'player');
    this.player.setCollideWorldBounds(true);
    this.player.setDepth(10);
    
    // Set up camera to follow player
    this.cameras.main.setBounds(0, 0, this.mapWidth, this.mapHeight);
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);
    
    // Set up keyboard controls
    this.joystickKeys = this.input.keyboard.addKeys({
      up: Phaser.Input.Keyboard.KeyCodes.W,
      down: Phaser.Input.Keyboard.KeyCodes.S,
      left: Phaser.Input.Keyboard.KeyCodes.A,
      right: Phaser.Input.Keyboard.KeyCodes.D
    });
    
    // Set up touch/mouse joystick
    this.setupJoystick();
    
    // Set world bounds
    this.physics.world.setBounds(0, 0, this.mapWidth, this.mapHeight);
    
    // Initialize items group
    this.items = this.physics.add.group();
    
    // Add evolution description text (will be updated when commit history loads)
    this.evolutionText = this.add.text(
      this.cameras.main.width - 30,
      this.cameras.main.height - 60,
      '',
      {
        fontSize: '12px',
        color: '#aaaaaa',
        align: 'right',
        wordWrap: { width: 300 }
      }
    );
    this.evolutionText.setScrollFactor(0);
    this.evolutionText.setOrigin(1, 1);
    this.evolutionText.setDepth(100);
    
    // Load commit history and character evolution data
    this.loadCommitHistory();

    // Set up collision between player and items
    this.physics.add.overlap(this.player, this.items, this.collectItem, null, this);
  }
  
  createPlayerAnimations() {
    // Create player walk animation if it doesn't exist
    if (!this.anims.exists('player_walk')) {
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
    }
  }
  
  createManifestoWorld() {
    // Split the manifesto into lines
    const lines = this.manifestoLines;
    
    // Calculate the center of the map width
    const centerX = this.mapWidth / 2;
    
    // Start position for the text
    let yPosition = 300; // Start a bit down from the top
    
    // Add each line with spacing
    lines.forEach((line, index) => {
      // Skip empty lines but add spacing
      if (line.trim() === '') {
        yPosition += 30; // Reduced from 40
        return;
      }
      
      // Create text object
      const textStyle = {
        fontFamily: 'Arial',
        fontSize: '20px',
        color: '#ffffff',
        align: 'center'
      };
      
      // Make title larger
      if (index === 0) {
        textStyle.fontSize = '36px';
        textStyle.fontStyle = 'bold';
        yPosition += 15; // Reduced from 20
      }
      
      const textObject = this.add.text(centerX, yPosition, line, textStyle);
      textObject.setOrigin(0.5, 0);
      
      // Store reference to text object
      this.textObjects.push(textObject);
      
      // Increment y position for next line
      yPosition += 35; // Reduced from 45
    });
    
    // Add instructions at the top
    const instructionText = this.add.text(
      centerX, 
      100, 
      "This is a living game.\nUse WASD or touch to move.\nExplore the manifesto.\nWith every commit PotNoodleDev will evolve.", 
      {
        fontSize: '12px',
        color: '#aaaaaa',
        align: 'center',
        lineSpacing: 5,
        wordWrap: { 
          width: 400,
          useAdvancedWrap: true 
        }
      }
    );
    instructionText.setOrigin(0.5, 0);

    // Calculate total height needed and update map bounds
    const lastTextObject = this.textObjects[this.textObjects.length - 1];
    const totalTextHeight = lastTextObject.y + lastTextObject.height;
    // Add padding at the bottom
    this.mapHeight = totalTextHeight + 300;
    
    // Update physics and camera bounds
    this.physics.world.setBounds(0, 0, this.mapWidth, this.mapHeight);
    this.cameras.main.setBounds(0, 0, this.mapWidth, this.mapHeight);
  }
  
  setupJoystick() {
    this.input.on('pointerdown', (pointer) => {
      this.joystickPointer = pointer;
      this.joystick = {
        x: pointer.x,
        y: pointer.y
      };
      
      // Create joystick visual
      if (this.joystickGraphics) {
        this.joystickGraphics.destroy();
      }
      
      this.joystickGraphics = this.add.graphics();
      this.joystickGraphics.setScrollFactor(0);
      this.joystickGraphics.fillStyle(0x888888, 0.5);
      this.joystickGraphics.fillCircle(this.joystick.x, this.joystick.y, 20);
    });
    
    this.input.on('pointermove', (pointer) => {
      if (this.joystickPointer && this.joystickPointer.id === pointer.id) {
        // Update joystick position
        if (this.joystickGraphics) {
          this.joystickGraphics.clear();
          this.joystickGraphics.fillStyle(0x888888, 0.5);
          this.joystickGraphics.fillCircle(this.joystick.x, this.joystick.y, 20);
          this.joystickGraphics.fillStyle(0xaaaaaa, 0.8);
          this.joystickGraphics.fillCircle(pointer.x, pointer.y, 10);
        }
      }
    });
    
    this.input.on('pointerup', (pointer) => {
      if (this.joystickPointer && this.joystickPointer.id === pointer.id) {
        this.joystickPointer = null;
        this.joystick = null;
        
        if (this.joystickGraphics) {
          this.joystickGraphics.destroy();
          this.joystickGraphics = null;
        }
      }
    });
  }
  
  async loadCommitHistory() {
    try {
      // Try to load commit history from cache
      let commitHistory = null;
      
      try {
        commitHistory = this.cache.json.get('commit-history');
        this.game.events.emit('terminal-message', "Commit history loaded");
      } catch (error) {
        this.game.events.emit('terminal-message', "No cached commit history found");
      }
      
      // If no cached history, try to fetch from GitHub
      if (!commitHistory) {
        this.game.events.emit('terminal-message', "Fetching commits from GitHub...");
        
        try {
          const response = await axios.get(
            `https://api.github.com/search/commits`,
            {
              params: { q: `author:potnoodledev` },
              headers: {
                Accept: 'application/vnd.github.cloak-preview',
              },
            }
          );
          
          if (response.data.items && response.data.items.length > 0) {
            this.game.events.emit('terminal-message', `Found ${response.data.items.length} commits`);
            
            // Display the most recent commits
            const recentCommits = response.data.items.slice(0, 5);
            this.game.events.emit('terminal-message', "-------------------");
            this.game.events.emit('terminal-message', "Recent commits:");
            
            recentCommits.forEach(commit => {
              const date = new Date(commit.commit.author.date);
              const dateStr = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
              const shortMessage = commit.commit.message.split('\n')[0].substring(0, 30);
              this.game.events.emit('terminal-message', `${dateStr}: ${shortMessage}...`);
            });
          } else {
            this.game.events.emit('terminal-message', "No commits found");
          }
        } catch (error) {
          this.game.events.emit('terminal-message', "Error fetching commits");
          console.error("Error fetching commits:", error);
        }
      }
      
      // Store evolution history
      if (commitHistory && commitHistory.evolutionHistory) {
        this.evolutionHistory = commitHistory.evolutionHistory;
        console.log(`Loaded ${this.evolutionHistory.length} evolution entries`);
      }
      
      // Display character evolution information
      this.game.events.emit('terminal-message', "-------------------");
      this.game.events.emit('terminal-message', "Character Evolution:");
      
      if (commitHistory) {
        const { currentCharacterDescription, evolutionLevel, totalCommits } = commitHistory;
        // Emit the total commits count to update the UI
        this.game.events.emit('update-commit-count', totalCommits);
        
        // Spawn items based on total commits
        this.spawnItems(totalCommits);
        
        this.game.events.emit('terminal-message', `Level: ${evolutionLevel} (${totalCommits} commits)`);
        this.game.events.emit('terminal-message', `Current: ${currentCharacterDescription}`);
        this.game.events.emit('terminal-message', `Next evolution: 1 more commit`);
        this.game.events.emit('terminal-message', `Evolution type: Subtle, gradual changes`);
        
        // Add evolution history
        if (this.evolutionHistory.length > 0) {
          this.game.events.emit('terminal-message', "-------------------");
          this.game.events.emit('terminal-message', "EVOLUTION HISTORY:");
          
          this.evolutionHistory.forEach((evolution, index) => {
            const date = new Date(evolution.commitDate);
            const dateStr = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
            
            this.game.events.emit('terminal-message', `[${index + 1}] ${dateStr}`);
            this.game.events.emit('terminal-message', `Commit: ${evolution.commitMessage}`);
            this.game.events.emit('terminal-message', evolution.newDescription);
            this.game.events.emit('terminal-message', "-------------------");
          });
        }

        // Update evolution text with current description from commit history
        if (this.evolutionText) {
          this.evolutionText.setText(`Current evolution: ${currentCharacterDescription}`);
        }
      } else {
        // When no commit history, emit 0 commits
        this.game.events.emit('update-commit-count', 0);
        
        this.game.events.emit('terminal-message', "Level: 0");
        this.game.events.emit('terminal-message', "Character: simple wanderer with plain clothes");
        this.game.events.emit('terminal-message', `Next evolution: 1 more commit`);
        this.game.events.emit('terminal-message', `Evolution type: Subtle, gradual changes`);

        // Update evolution text
        if (this.evolutionText) {
          this.evolutionText.setText('Current evolution: Loading...');
        }
      }
      
    } catch (error) {
      console.error("Error loading commit history:", error);
      this.game.events.emit('terminal-message', "Error loading evolution data");
    }
  }

  spawnItems(totalCommits) {
    // Clear existing items
    this.items.clear(true, true);
    this.itemsCollected = 0;
    this.totalItems = totalCommits;

    // Spawn an item for each commit
    for (let i = 0; i < totalCommits; i++) {
      const x = Phaser.Math.Between(100, this.mapWidth - 100);
      const y = Phaser.Math.Between(100, this.mapHeight - 100);
      
      const item = this.items.create(x, y, 'pot_noodle');
      item.setScale(1.5);
      item.setDepth(5);
      
      // Add a floating animation
      this.tweens.add({
        targets: item,
        y: y + 10,
        duration: 1500,
        yoyo: true,
        repeat: -1,
        ease: 'Sine.easeInOut'
      });
    }

    // Reset counter at start
    this.game.events.emit('reset-counter', totalCommits);
  }

  collectItem(player, item) {
    // Disable collision to prevent multiple collections of the same item
    item.body.enable = false;
    
    // Play collection animation
    this.tweens.add({
      targets: item,
      scale: 0,
      alpha: 0,
      duration: 200,
      ease: 'Power2',
      onComplete: () => {
        item.destroy();
      }
    });

    // Simply increment counter by 1
    this.game.events.emit('increment-counter');
  }

  update() {
    // Handle player movement
    this.handlePlayerMovement();
  }

  handlePlayerMovement() {
    // Reset velocity
    this.player.setVelocity(0);
    
    // Variables to track movement direction
    let moveX = 0;
    let moveY = 0;
    
    // Handle keyboard input
    if (this.joystickKeys.left.isDown) {
      moveX = -1;
    } else if (this.joystickKeys.right.isDown) {
      moveX = 1;
    }
    
    if (this.joystickKeys.up.isDown) {
      moveY = -1;
    } else if (this.joystickKeys.down.isDown) {
      moveY = 1;
    }
    
    // Handle touch/mouse joystick
    if (this.joystick && this.joystickPointer) {
      const dx = this.joystickPointer.x - this.joystick.x;
      const dy = this.joystickPointer.y - this.joystick.y;
      
      // Only apply joystick movement if it's moved enough
      if (Math.sqrt(dx * dx + dy * dy) > 10) {
        moveX = dx;
        moveY = dy;
        
        // Normalize
        const length = Math.sqrt(moveX * moveX + moveY * moveY);
        moveX = moveX / length;
        moveY = moveY / length;
      }
    }
    
    // Apply movement
    if (moveX !== 0 || moveY !== 0) {
      // Normalize diagonal movement
      if (moveX !== 0 && moveY !== 0) {
        const length = Math.sqrt(moveX * moveX + moveY * moveY);
        moveX = moveX / length;
        moveY = moveY / length;
      }
      
      this.player.setVelocity(moveX * this.playerSpeed, moveY * this.playerSpeed);
      
      // Play walk animation when moving
      if (!this.player.anims.isPlaying) {
        this.player.play('player_walk');
      }
      
      // Flip player sprite based on horizontal movement direction
      if (moveX < 0) {
        this.player.setFlipX(true);
      } else if (moveX > 0) {
        this.player.setFlipX(false);
      }
    } else {
      // Stop animation when not moving
      if (this.player.anims.isPlaying) {
        this.player.anims.stop();
        this.player.setTexture('player');
      }
    }
  }
} 