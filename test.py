from main import app
import unittest
import json

class flaskTestCase(unittest.TestCase):	
	
	def test_1(self):
		tester = app.test_client(self)
		response = tester.get('/', content_type='html/text')
		self.assertEqual(response.status_code, 200)
	#expecting a 302 as /home can only be accessed when a user is in session
	def test_2(self):
		tester = app.test_client(self)
		response = tester.get('/home', content_type='html/text')
		self.assertEqual(response.status_code, 302)
		
	def test_3(self):
		tester = app.test_client(self)
		response = tester.get('/register', content_type='html/text')
		self.assertEqual(response.status_code, 200)
		
	def test_4(self):
		tester = app.test_client(self)
		response = tester.get('/registerS', content_type='html/text')
		self.assertEqual(response.status_code, 200)
	#This tests whether or not the user signIn works for a specified lecturer
	def test_5(self):
		tester = app.test_client(self)
		response = tester.post('/signIn', data=dict(username="philipe.moser@mumail.ie", password="test"),follow_redirects=True)
		return response.data

	def test_6(self):
		tester = app.test_client(self)
		response = tester.get('/invalidURL', content_type='html/text')
		self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
	unittest.main()
