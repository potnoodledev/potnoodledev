import Phaser from 'phaser';

export default class GameOverScene extends Phaser.Scene {
  constructor() {
    super('GameOverScene');
  }

  create() {
    // We don't need a game over scene for our minimalist experience
    // Just return to the game scene
    this.scene.start('GameScene');
  }
} 