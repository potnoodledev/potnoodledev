import Phaser from 'phaser';
import BootScene from './scenes/BootScene';
import GameScene from './scenes/GameScene';
import UIScene from './scenes/UIScene';
import GameOverScene from './scenes/GameOverScene';

// Game configuration
const config = {
  type: Phaser.AUTO,
  parent: 'game-container',
  width: 800,
  height: 600,
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 0 },
      debug: false
    }
  },
  scene: [BootScene, GameScene, UIScene, GameOverScene],
  pixelArt: false,
  roundPixels: true,
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  }
};

// Initialize the game
window.addEventListener('load', () => {
  const game = new Phaser.Game(config);
  
  // Handle resize events
  window.addEventListener('resize', () => {
    game.scale.refresh();
  });
}); 