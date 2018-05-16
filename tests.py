from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_password_hashing(self):
		u = User(username='kim')
		u.set_password('kim')
		self.assertFalse(u.check_password('mik'))
		self.assertTrue(u.check_password('kim'))

	def test_follow(self):
		u1 = User(username='bob')
		u2 = User(username='kim')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		self.assertEqual(u1.followed.all(), [])
		self.assertEqual(u1.followers.all(), [])

		u1.follow(u2)
		db.session.commit()
		self.assertTrue(u1.is_following(u2))
		self.assertEqual(u1.followed.count(), 1)
		self.assertEqual(u1.followed.first().username, 'kim')
		self.assertEqual(u2.followers.count(), 1)
		self.assertEqual(u2.followers.first().username, 'bob')

		u1.unfollow(u2)
		db.session.commit()
		self.assertFalse(u1.is_following(u2))
		self.assertEqual(u1.followed.count(), 0)
		self.assertEqual(u2.followers.count(), 0)

	def test_follow_posts(self):
		# create test users
		u1 = User(username='bob')
		u2 = User(username='kim')
		u3 = User(username='sam')
		u4 = User(username='joey')
		db.session.add_all([u1, u2, u3, u4])

		# create test posts
		now = datetime.utcnow()
		p1 = Post(author=u1, body="post from bob", timestamp=now + timedelta(seconds=1))
		p2 = Post(author=u2, body="post from kim", timestamp=now + timedelta(seconds=2))
		p3 = Post(author=u3, body="post from sam", timestamp=now + timedelta(seconds=3))
		p4 = Post(author=u4, body="post from joey", timestamp=now + timedelta(seconds=4))
		db.session.add_all([p1, p2, p3, p4])
		db.session.commit()

		# set up followers
		u1.follow(u2) # bob follows kim
		u1.follow(u4) # bob follows joey
		u2.follow(u3) # kim follows sam
		u3.follow(u4) # sam follows joey
		db.session.commit()

		# check the followed fosts of each user
		f1 = u1.followed_posts().all()
		f2 = u2.followed_posts().all()
		f3 = u3.followed_posts().all()
		f4 = u4.followed_posts().all()
		self.assertEqual(f1, [p4, p2, p1])
		self.assertEqual(f2, [p3, p2])
		self.assertEqual(f3, [p4, p3])
		self.assertEqual(f4, [p4])

if __name__ == '__main__':
	unittest.main(verbosity=2)
