import Phaser from 'phaser';

export default class GameOverScene extends Phaser.Scene {
  constructor() {
    super('GameOverScene');
    
    // UI style constants to match UIScene
    this.styles = {
      boxFill: 0x000000,
      boxOutlineWidth: 2,
      boxOutlineColor: 0xffffff,
      textSize: '20px',
      textColor: '#ffffff',
      headerTextSize: '42px',
      headerTextColor: '#ffffff',
      buttonFill: 0x000000,
      buttonHoverFill: 0x333333,
      buttonTextColor: '#ffffff'
    };
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
    
    // Create main panel with outline - pure black
    const panelWidth = 400;
    const panelHeight = 350;
    const panel = this.add.rectangle(centerX, centerY, panelWidth, panelHeight, 0x000000, 1)
      .setOrigin(0.5);
    
    // Add white outline to panel
    const outline = this.add.rectangle(centerX, centerY, panelWidth + this.styles.boxOutlineWidth, panelHeight + this.styles.boxOutlineWidth, this.styles.boxOutlineColor, 1)
      .setOrigin(0.5)
      .setStrokeStyle(this.styles.boxOutlineWidth, this.styles.boxOutlineColor);
    
    // Create title text
    const titleText = this.victory ? 'VICTORY!' : 'GAME OVER';
    const titleColor = this.victory ? '#ffff00' : '#ff0000';
    
    this.add.text(centerX, centerY - 100, titleText, {
      font: 'bold ' + this.styles.headerTextSize + ' Arial',
      fill: titleColor
    }).setOrigin(0.5);
    
    // Create stats text
    const minutes = Math.floor(this.time / 60000);
    const seconds = Math.floor((this.time % 60000) / 1000);
    const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    this.add.text(centerX, centerY, `Level Reached: ${this.level}`, {
      font: this.styles.textSize + ' Arial',
      fill: this.styles.textColor
    }).setOrigin(0.5);
    
    this.add.text(centerX, centerY + 40, `Time Survived: ${timeString}`, {
      font: this.styles.textSize + ' Arial',
      fill: this.styles.textColor
    }).setOrigin(0.5);
    
    // Create restart button with outline - pure black
    const buttonWidth = 200;
    const buttonHeight = 50;
    const restartButton = this.add.rectangle(centerX, centerY + 120, buttonWidth, buttonHeight, 0x000000, 1)
      .setInteractive({ useHandCursor: true });
    
    // Add white outline to button
    const buttonOutline = this.add.rectangle(centerX, centerY + 120, buttonWidth + this.styles.boxOutlineWidth, buttonHeight + this.styles.boxOutlineWidth, this.styles.boxOutlineColor, 1)
      .setStrokeStyle(this.styles.boxOutlineWidth, this.styles.boxOutlineColor);
    
    this.add.text(centerX, centerY + 120, 'Play Again', {
      font: 'bold 18px Arial',
      fill: this.styles.buttonTextColor
    }).setOrigin(0.5);
    
    // Add hover effect
    restartButton.on('pointerover', () => {
      restartButton.fillColor = this.styles.buttonHoverFill;
    });
    
    restartButton.on('pointerout', () => {
      restartButton.fillColor = 0x000000; // Reset to pure black
    });
    
    // Add click event
    restartButton.on('pointerdown', () => {
      this.scene.start('BootScene');
    });
  }
} 