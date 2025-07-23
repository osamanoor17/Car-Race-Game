# 🚗 Car Racing Game (Pygame)

A simple yet addictive 2D car racing game built with Python and Pygame. Dodge enemy cars, track your score, and compete on the local scoreboard.

---

## 🎮 Features

- Real-time car movement with arrow keys
- Dynamic background scrolling
- Start screen with name input
- Game over screen with restart/quit options
- Local scoreboard (top 5 scores)
- Player name and score tracking in `scores.txt`

---

## 🖼️ Screenshots

> *(Add screenshots of the gameplay and menus here for better visualization)*

---

## 🛠️ Requirements

- Python 3.x  
- Pygame  

### Install Pygame:
```bash
pip install pygame
```
### 📁 Folder Structure

```
project_folder/
├── img/
│   ├── car.png
│   ├── enemy_car_2.png
│   ├── back_ground.jpg
│   └── icon.png
├── scores.txt       # Auto-generated after gameplay
└── main.py          # Main game file
```

### 🚀 How to Run
```bash
python main.py
```
### 🎮 Controls

## Key	Action
```
← / → 	Move car left/right
SPACE   Start game
R	Restart after game over
Q	Quit after game over
```

### 📝 Notes
```
1. Your score is saved in scores.txt after each game.

2. Only the top 5 scores are shown in the Game Over screen.

3. Make sure your image assets are correctly named and placed inside the img/folder.
```
### 📌 Author
Made by Muhammad Osama Noor using Python and Pygame.