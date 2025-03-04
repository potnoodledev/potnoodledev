import Phaser from 'phaser';

export default class GameOverScene extends Phaser.Scene {
  constructor() {
    super('GameOverScene');
  }

  init(data) {
    this.victory = data.victory || false;
    this.level = data.level || 1;
    this.time = data.time || 0;
  }

  create() {
    // Calculate center of screen
    const centerX = this.cameras.main.width / 2;
    const centerY = this.cameras.main.height / 2;
    
    // Create background
    this.add.rectangle(0, 0, this.cameras.main.width, this.cameras.main.height, 0x000000, 0.8)
      .setOrigin(0, 0);
    
    // Create title text
    const titleText = this.victory ? 'VICTORY!' : 'GAME OVER';
    const titleColor = this.victory ? '#ffff00' : '#ff0000';
    
    this.add.text(centerX, centerY - 100, titleText, {
      font: 'bold 48px Arial',
      fill: titleColor
    }).setOrigin(0.5);
    
    // Create stats text
    const minutes = Math.floor(this.time / 60000);
    const seconds = Math.floor((this.time % 60000) / 1000);
    const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    this.add.text(centerX, centerY, `Level Reached: ${this.level}`, {
      font: '24px Arial',
      fill: '#ffffff'
    }).setOrigin(0.5);
    
    this.add.text(centerX, centerY + 40, `Time Survived: ${timeString}`, {
      font: '24px Arial',
      fill: '#ffffff'
    }).setOrigin(0.5);
    
    // Create restart button
    const restartButton = this.add.rectangle(centerX, centerY + 120, 200, 50, 0x4a90e2)
      .setInteractive({ useHandCursor: true });
    
    this.add.text(centerX, centerY + 120, 'Play Again', {
      font: 'bold 20px Arial',
      fill: '#ffffff'
    }).setOrigin(0.5);
    
    // Add hover effect
    restartButton.on('pointerover', () => {
      restartButton.fillColor = 0x2c3e50;
    });
    
    restartButton.on('pointerout', () => {
      restartButton.fillColor = 0x4a90e2;
    });
    
    // Add click event
    restartButton.on('pointerdown', () => {
      this.scene.start('BootScene');
    });
  }
} 