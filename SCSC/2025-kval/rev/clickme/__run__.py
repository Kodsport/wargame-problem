from javax.swing import (BoxLayout, ImageIcon, JButton, JFrame, JPanel,
        JPasswordField, JLabel, JTextArea, JTextField, JScrollPane,
        SwingConstants, WindowConstants)
from java.awt import Component, GridLayout

import math

class Game:
    def __init__(self):
        self.frame = JFrame("Reach The Goal!", defaultCloseOperation=JFrame.EXIT_ON_CLOSE, size=(512, 512))
        self.panel = JPanel(GridLayout(0, 2))
        self.frame.add(self.panel)

        self.goal = self.update_new_goal(200)
        self.clicks = 0

        self.counter = JLabel("0/%d" % self.goal)
        self.cookie = JButton("Click me :)", actionPerformed=self.update_clicks)

        self.panel.add(self.counter)
        self.panel.add(self.cookie)

        self.frame.pack()
        self.frame.visible = True
    
    def f(self, x):
        return math.ceil(200 - 0.0009 * x * x + 10 * x)

    def search_x(self, y):
        x = 0
        while True:
            if self.f(x) == y:
                return x
            x += 1

    def decrypt(self, key):
        flag = ""
        s = [21861940822296, 21845502704212, 21843937184028, 21865854666252, 21880727281912, 21867420250948, 21882292858160, 21890903308940, 21868985761180, 21871334092872, 21870551330516, 21858809801608, 21941000445324, 21886206644772, 21858809801608, 21938652170704, 21937086602392, 21881510038108, 21938652170704, 21868203006520, 21937869416060, 21877596194152, 21886206644772, 21941000445324, 21876813439988, 21938652170704, 21941783258976, 21868203006520, 21940217690664, 21858809801608, 21886989464984, 21940217690664, 21937869416060, 21886206644772, 21886206644772, 21937086602392, 21858809801608, 21941000445324, 21870551330516, 21858809801608, 21887772221308, 21882292858160, 21890903308940, 21868985761180, 21871334092872, 21870551330516, 21885423881024]
        for b in s:
            flag += chr(((((b ^ key) // key + 5) // key) ^ key) % 0xff)
        return flag

    def display(self, flag):
        self.frame.dispose()
        self.frame = JFrame("FlagBounty", defaultCloseOperation=JFrame.EXIT_ON_CLOSE, size=(512, 512))
        self.panel = JPanel()
        self.panel.add(JLabel(flag))
        self.frame.add(self.panel)
        self.frame.visible = True

    def update_new_goal(self, prev):
        px = self.search_x(prev)
        new = self.f(px+1)
        if prev > new:
            self.display(self.decrypt(new))
        return self.f(px+1)

    def update_clicks(self, event):
        self.clicks += 1

        if self.clicks >= self.goal:
            self.goal = self.update_new_goal(self.goal)
            self.frame.title = "Getting Tired?"
        self.counter.text = "%d/%d" % (self.clicks, self.goal) 

g = Game()