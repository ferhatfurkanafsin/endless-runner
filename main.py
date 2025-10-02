from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint

class SimpleGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Player
        self.player_x = 100
        self.player_y = 50
        self.player_size = 60
        self.velocity_y = 20
        self.jumping = False
        
        # Obstacles
        self.obstacles = []
        
        # Coins
        self.coins = []
        
        # Score
        self.score = 0
        self.coins_collected = 0
        
        # Bind keyboard and touch
        Window.bind(on_key_down=self.on_key_down)
        
        # Start game loop
        Clock.schedule_interval(self.update, 1.0/60.0)
        Clock.schedule_interval(self.spawn_obstacle, 1.0)
        Clock.schedule_interval(self.spawn_coin, 2.0)
        
        print("Game Started! Press SPACE or TAP to jump!")
        print("Dodge obstacles, collect coins!")
    
    def on_key_down(self, instance, key, *args):
        if key == 32:  # Spacebar
            self.jump()
    
    def on_touch_down(self, touch):
        self.jump()
        return super().on_touch_down(touch)
    
    def jump(self):
        if not self.jumping:
            self.velocity_y = 15
            self.jumping = True
            print("Jump!")
    
    def spawn_obstacle(self, dt):
        obs = {
            'x': Window.width,
            'y': 50,
            'width': 30,
            'height': randint(40, 100)
        }
        self.obstacles.append(obs)
    
    def spawn_coin(self, dt):
        coin = {
            'x': Window.width,
            'y': randint(100, 250),
            'size': 20,
            'collected': False
        }
        self.coins.append(coin)
    
    def update(self, dt):
        # Update player
        self.velocity_y -= 0.5  # Gravity
        self.player_y += self.velocity_y
        
        # Ground collision
        if self.player_y <= 50:
            self.player_y = 50
            self.velocity_y = 0
            self.jumping = False
        
        # Update obstacles
        for obs in self.obstacles[:]:
            obs['x'] -= 8
            
            # Remove off-screen
            if obs['x'] < -obs['width']:
                self.obstacles.remove(obs)
                self.score += 10
                print(f"Score: {self.score} | Coins: {self.coins_collected}")
            
            # Check collision
            if (self.player_x < obs['x'] + obs['width'] and
                self.player_x + self.player_size > obs['x'] and
                self.player_y < obs['y'] + obs['height'] and
                self.player_y + self.player_size > obs['y']):
                print(f"💥 GAME OVER! Final Score: {self.score} | Coins: {self.coins_collected}")
                self.score = 0
                self.coins_collected = 0
                self.obstacles.clear()
                self.coins.clear()
        
        # Update coins
        for coin in self.coins[:]:
            coin['x'] -= 5
            
            # Remove off-screen
            if coin['x'] < -coin['size']:
                self.coins.remove(coin)
            
            # Check collection
            if (not coin['collected'] and
                self.player_x < coin['x'] + coin['size'] and
                self.player_x + self.player_size > coin['x'] and
                self.player_y < coin['y'] + coin['size'] and
                self.player_y + self.player_size > coin['y']):
                coin['collected'] = True
                self.coins_collected += 1
                self.coins.remove(coin)
                print(f"⭐ Coin collected! Total: {self.coins_collected}")
        
        # Draw everything
        self.canvas.clear()
        with self.canvas:
            # Sky
            Color(0.53, 0.81, 0.92)
            Rectangle(pos=(0, 50), size=(Window.width, Window.height - 50))
            
            # Ground
            Color(0.2, 0.8, 0.2)
            Rectangle(pos=(0, 0), size=(Window.width, 50))
            
            # Player (red square with face)
            Color(1, 0.4, 0.4)
            Rectangle(pos=(self.player_x, self.player_y), 
                     size=(self.player_size, self.player_size))
            # Eyes
            Color(1, 1, 1)
            Rectangle(pos=(self.player_x + 10, self.player_y + 25), size=(8, 8))
            Rectangle(pos=(self.player_x + 22, self.player_y + 25), size=(8, 8))
            
            # Obstacles (brown)
            Color(0.5, 0.2, 0.1)
            for obs in self.obstacles:
                Rectangle(pos=(obs['x'], obs['y']), 
                         size=(obs['width'], obs['height']))
            
            # Coins (gold circles)
            Color(1, 0.84, 0)
            for coin in self.coins:
                if not coin['collected']:
                    Ellipse(pos=(coin['x'], coin['y']), 
                           size=(coin['size'], coin['size']))

class GameApp(App):
    def build(self):
        Window.clearcolor = (0.53, 0.81, 0.92, 1)
        Window.size = (800, 400)
        return SimpleGame()

if __name__ == '__main__':
    GameApp().run()
