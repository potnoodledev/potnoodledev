# Evolve the Game

A top-down action survival game built with Phaser 3.

## Game Description

"Evolve the Game" is a top-down action survival game where the player must survive for 10 minutes against progressively stronger waves of enemies. The player starts with a rock weapon that automatically targets and attacks the nearest enemy. As the player defeats enemies, they drop crystals that can be collected to gain XP and level up, improving the player's stats and weapon.

## Controls

- **Keyboard**: Use WASD keys to move the player character.
- **Mouse/Touch**: Drag anywhere on the screen to create a virtual joystick. The player will move in the direction you drag away from the initial touch point.

## Game Features

- **Automatic Weapon**: The player's rock weapon automatically targets and attacks the nearest enemy.
- **Leveling System**: Collect crystals from defeated enemies to gain XP and level up.
- **Progressive Difficulty**: Enemy waves become stronger over time, with more enemies and increased stats.
- **Timer**: Survive for 10 minutes to win the game.

## Development

### Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```
4. Open your browser and navigate to `http://localhost:8080`

### Building for Production

To build the game for production:

```
npm run build
```

The built files will be in the `dist` directory.

## Technologies Used

- [Phaser 3](https://phaser.io/phaser3) - HTML5 game framework
- [Webpack](https://webpack.js.org/) - Module bundler
- JavaScript (ES6+)

## License

This project is licensed under the ISC License. 