import Phaser from 'phaser';

export default class BootScene extends Phaser.Scene {
  constructor() {
    super('BootScene');
  }

  preload() {
    // Load player character and animations
    this.load.image('player', 'assets/images/player.png');
    this.load.image('player_walk_1', 'assets/images/player/walk/frame_1.png');
    this.load.image('player_walk_2', 'assets/images/player/walk/frame_2.png');
    this.load.image('player_walk_3', 'assets/images/player/walk/frame_3.png');
    this.load.image('player_walk_4', 'assets/images/player/walk/frame_4.png');

    // Load items
    this.load.image('pot_noodle', 'assets/images/items/pot_noodle_packet.png');

    // Load background images
    this.load.image('bg_potnoods', 'assets/images/background/potnoods.png');
    this.load.image('bg_potnoods2', 'assets/images/background/potnoods2.png');
    this.load.image('bg_potnoods3', 'assets/images/background/potnoods3.png');
    this.load.image('bg_potnoods4', 'assets/images/background/potnoods4.png');

    // Load background videos
    this.load.video('bg_video5', 'assets/images/background/potnoods5.mp4', 'canplay', true, false);
    this.load.video('bg_video6', 'assets/images/background/potnoods6.mp4', 'canplay', true, false);
    this.load.video('bg_video7', 'assets/images/background/potnoods7.mp4', 'canplay', true, false);
  }

  create() {
    console.log('Boot scene loaded');
    
    // Start the game scene
    this.scene.start('GameScene');
    
    // Start the UI scene in parallel
    this.scene.launch('UIScene');
  }
} 