import Phaser from 'phaser';

export default class BootScene extends Phaser.Scene {
  constructor() {
    super('BootScene');
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

    // Load game assets
    this.load.image('player', 'assets/images/player.png');
    this.load.image('enemy', 'assets/images/enemy.png');
    this.load.image('crystal', 'assets/images/items/crystal.png');
    
    // Load weapons and projectiles
    this.load.image('rock', 'assets/images/weapons/rock.png');
    this.load.image('bow', 'assets/images/weapons/bow.png');
    this.load.image('axe', 'assets/images/weapons/axe.png');
    this.load.image('arrow', 'assets/images/weapons/projectiles/arrow.png');
    this.load.image('axe_projectile', 'assets/images/weapons/projectiles/axe.png');
    
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
  }

  create() {
    this.scene.start('GameScene');
    this.scene.launch('UIScene');
  }
} 