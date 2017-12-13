import os
import sys
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()

# Secret key to create and verify tokens
secret_key = ''.join(random.choice(string.ascii_uppercase+string.digits) for x in range(32))

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key = True)
	username = Column(String(250), nullable=False)
	picture = Column(String(250))
	email = Column(String(250), nullable=False)
	"""password_hash = Column(String(64))

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	def generate_auth_token(self, expiration=600):
		s = Serializer(secret_key, expires_in = expiration)
		return s.dumps({'id': self.id})

	# Generate auth tokens
	@staticmethod
	def verify_auth_token(token):
		s = serialize(secret_key)
		try:
			data = s.loads(token)
		except SignatureExpired:
			# Token is valid, but signature expired, so
			return Nones
		except BadSignature:
			# Token is invalid, so
			return None
		user_id = data['id']
		return user_id"""

class Styles(Base):
	__tablename__ = 'style'

	id = Column(Integer, primary_key = True)
	category = Column(String)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
		'id': self.id,
		'category': self.category,
		}

class Influencers(Base):
	__tablename__ = 'Influencers'

	id = Column(Integer, primary_key = True)
	name = Column(String)
	country = Column(String)
	blogName = Column(String)
	description = Column(String)
	picture = Column(String)
	user_id = Column(String, ForeignKey('user.id'))
	user = relationship(user)
	styles_id = Column(Integer, ForeignKey('style.id'))
	styles = relationship(Styles)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
		'name': self.name,
		'country': self.country,
		'blog_name':self.blog_name,
		'description': self.description,
		'picture': self.picture
		}

"""class MakeUp_Looks(Base):
	__tablename__ = 'MakeUp_Looks'

	id = Column(Integer, ForeignKey('MakeUps.id'))
	occasions = Column(String)
	user_id = Column(String, ForeignKey('user.id'))
	user = relationship(user)
	styles_id = Column(Integer, ForeignKey('style.id'))
	styles = relationship(Styles)


class Fashion(Base):
	__tablename__ = 'Fashion'

	id = Column(Integer, ForeignKey('Fashion.id'))
	occasions = Column(String)
	user_id = Column(String, ForeignKey('user.id'))
	user = relationship(user)
	styles_id = Column(Integer, ForeignKey('style.id'))
	styles = relationship(Styles)

class HomeDecor(Base):
	__tablename__ = 'HomeDecor'

	id = Column(Integer, ForeignKey('HomeDecor.id'))
	occasions = Column(String)
	user_id = Column(String, ForeignKey('user.id'))
	user = relationship(user)
	styles_id = Column(Integer, ForeignKey('style.id'))
	styles = relationship(Styles)"""

engine = create_engine('sqlite:///styleInfluencers.db')

Base.metadata.create_all(engine)