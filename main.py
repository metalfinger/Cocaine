import kivy
kivy.require('1.0.7')

import random
from glob import glob
from os.path import join, dirname

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.video import Video
from kivy.graphics.vertex_instructions import Line, BorderImage, Ellipse
from kivy.vector import Vector
from kivy.clock import Clock
import math


class Animationn(Animation):

	def on_progress(self, *ins):
		if ins[0].y > Window.height-30 and ins[0].up == 0:
			self.stop(ins[0])
			ins[0].up = 1
			#print "Up is up"
			if ins[0].theta > math.pi/2:
				ins[0].theta = 2*math.pi - ins[0].theta
			elif ins[0].theta < math.pi/2:
				ins[0].theta = 2*math.pi - ins[0].theta
			elif ins[0].theta == math.pi/2:
				ins[0].theta = 3*math.pi/2

		if ins[0].y < Window.height-30 and ins[0].up == 1:
			ins[0].up = 0
			ins[0].speed += 2
			ins[0].score += 1
			#print "Up is Downsdfsdfsdfsdfsdfsdfsddsfdf"

		if ins[0].x > Window.width-30 and ins[0].right == 0:
			self.stop(ins[0])
			#print "Right is up"
			ins[0].right = 1
			ins[0].control = 1
			if ins[0].theta > 3*math.pi/2:
				#print "Baby has arrived"
				ins[0].theta = 3*math.pi - ins[0].theta
			elif ins[0].theta < 3*math.pi/2:
				ins[0].theta = math.pi - ins[0].theta
			elif ins[0].theta == 0:
				ins[0].theta = math.pi

		if ins[0].x < Window.width-30 and ins[0].right == 1:
			ins[0].right = 0
			ins[0].speed += 2
			ins[0].score += 1
			#print "Right is down"


		if ins[0].x < 0 and ins[0].down == 0:
			self.stop(ins[0])
			#print "Down is up"
			ins[0].down = 1
			if ins[0].theta > math.pi:
				ins[0].theta = 3*math.pi - ins[0].theta
			elif ins[0].theta < math.pi:
				ins[0].theta = math.pi - ins[0].theta
			elif ins[0].theta == math.pi:
				ins[0].theta = 0
		if ins[0].x > 0 and ins[0].down == 1:
			ins[0].down = 0
			ins[0].speed += 2
			ins[0].score += 1
			#print "Down is down"

class Ball(Widget):
	theta = math.pi/6
	speed = 20
	up = 0
	down = 0
	right = 0
	left = 0
	score = 0
	anim = Animationn()

	def hiren(self):
		Clock.schedule_interval(self.my_callback, 0.05)

	def my_callback(self, *la):
		self.anim = Animationn(x=self.x+(self.speed*math.cos(self.theta)), y=self.y+(self.speed*math.sin(self.theta)), d=0.05)
		if self.y > 0:
			self.anim.start(self)


class player1(FloatLayout):
	a=Vector(0,0)
	id = 0
	b=Vector(0,0)
	c=0
	d=Vector(0,0)
	touched = 0
	stick_len = 200

	ball = Ball()


	def add_ball(self):
		self.ball = Ball()
		self.ball.pos=(100, 100)
		self.ball.hiren()
		Clock.schedule_interval(self.collide, 0.025)
		return self.ball

	def on_touch_down(self, touch):
		self.c += 1
		if self.c == 1:
			self.id = touch.uid
			self.a = touch.pos
		if self.c == 2:
			if self.id == touch.uid:
				self.a = touch.pos
			else:
				self.b = touch.pos
			if self.b[0] != 0 and self.b[1] != 0 and Vector(self.a).distance(self.b) < self.stick_len:
				with self.canvas:
					Line(points=(self.a[0],self.a[1],self.b[0],self.b[1]))
		if self.c > 2:
			content = Button(text='You are not allowed to have more than 2 touches ! Game Over ! I want to play again. Your score was : '+str(self.ball.score))
			popup = Popup(title='Ooopsssss',size_hint=(None, None), size=(Window.width, 400),content=content, auto_dismiss=True)
			def ohh(ins):
				popup.dismiss(force=True)
				self.ball.anim.stop(self.ball)
				self.ball.x = 100
				self.ball.y = 100
				self.ball.theta = math.pi/4
				self.score = 0
			content.bind(on_press=ohh)
			popup.open()


	def on_touch_up(self, touch):
		self.c -= 1
		if self.c == 1:
			self.canvas.clear()
			self.b = (0,0)


	def on_touch_move(self, touch):
		self.canvas.clear()
		self.ret()
		if self.c == 1:
			self.a = touch.pos
			self.id = touch.uid
		if self.c == 2:
			if self.id == touch.uid:
				self.a = touch.pos
			else:
				self.b = touch.pos


	def ret(self):
		if self.b[0] != 0 and self.b[1] != 0 and Vector(self.a).distance(self.b) < self.stick_len:
			with self.canvas:
				Line(points=(self.a[0],self.a[1],self.b[0],self.b[1]))

	def collide(self, *la):
		if self.b[0] != 0 and self.b[1] != 0 and Vector(self.a).distance(self.b) < self.stick_len:
			if self.a[1] > self.b[1]:
				yb = self.a[1]
				ys = self.b[1]
				xb = self.a[0]
				xs = self.b[0]
			else:
				ys = self.a[1]
				yb = self.b[1]
				xs = self.a[0]
				xb = self.b[0]
			test_theta = 0
			if (self.b[0]-self.a[0]) != 0:
				test_theta=math.atan((self.b[1]-self.a[1])/(self.b[0]-self.a[0]))
				if test_theta < 0:
					test_theta += math.pi
			if self.a[0] != self.ball.x:
				collide_theta = math.atan(((self.a[1]-self.ball.y)/(self.a[0]-self.ball.x)))
				if collide_theta < 0:
					collide_theta = math.pi + collide_theta
			else:
				collide_theta = 0

			ymin = 0
			ymax = 0
			xmax = 0
			xmin = 0

			if self.b[1] > self.a[1]:
				ymax = self.b[1]
				ymin = self.a[1]
			else:
				ymin = self.b[1]
				ymax = self.a[1]
			if self.b[0] > self.a[0]:
				xmax = self.b[0]
				xmin = self.a[0]
			else:
				xmin = self.b[0]
				xmax = self.a[0]

			if (xmin < self.ball.x and self.ball.x < xmax) and (ymin < self.ball.y and self.ball.y < ymax):
				if ((collide_theta*180/math.pi) < (test_theta*180/math.pi)+10) and ((collide_theta*180/math.pi) > (test_theta*180/math.pi)-10):
					if self.touched == 0:
						self.ball.anim.stop(self.ball)
						self.touched = 1
						self.ball.theta = 2*test_theta - self.ball.theta
						if self.ball.theta < 0:
							self.ball.theta += 2*math.pi

			if ((collide_theta*180/math.pi) > (test_theta*180/math.pi)+10) or ((collide_theta*180/math.pi) < (test_theta*180/math.pi)-10):
				if self.touched == 1:
					self.touched = 0

		if self.ball.y < 0:
			content = Button(text='Close me! I want to play again. Your score was : '+str(self.ball.score))
			popup = Popup(title='Ooopsssss',size_hint=(None, None), size=(400, 400),content=content, auto_dismiss=True)
			def ohh(ins):
				self.ball.anim.stop(self.ball)
				self.ball.x = 100
				self.ball.y = 100
				self.ball.theta = math.pi/4
				self.score = 0
				popup.dismiss(force=True)
			content.bind(on_press=ohh)
			popup.open()


class TestApp(App):

	def build(self):
		content = Button(text='-> You have to save ball from falling down.\n-> Length of stick is limited.\n-> A Player can\'t have more than 2 touches, otherwise game will over.\n-> As time will pass, speed of ball will increase.\n\n-> Let\'s see, How much you can score')
		popup = Popup(title='Instructions : ',size_hint=(None, None), size=(Window.width, Window.height),content=content, auto_dismiss=True)
		root = FloatLayout()
		main1 = player1()
		root.add_widget(main1)
		def ohh(ins):
			popup.dismiss(force=True)
			root.add_widget(main1.add_ball())
		content.bind(on_press=ohh)
		popup.open()

		return root



if __name__ in ('__main__', '__android__'):
    TestApp().run()

