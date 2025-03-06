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
  }

  create() {
    console.log('Boot scene loaded');
    
    // Start the game scene
    this.scene.start('GameScene');
    
    // Start the UI scene in parallel
    this.scene.launch('UIScene');
  }
} 