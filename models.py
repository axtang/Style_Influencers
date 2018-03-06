import os
import sys
from flask import Blueprints
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


class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key = True)
	username = Column(String(250), nullable=False)
	picture = Column(String(250))
	email = Column(String(250), nullable=False)


engine = create_engine('sqlite:///styleInfluencers.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


CLIENT_ID = json.loads(
	open('client_secrets.json','r').read())['web']['client_id']