from flask import Blueprint
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///styleInfluencers.db', echo=True)

# create a session
Session = sessionmaker(bind=engine)
session = DBSession()

# create a dummy user
User_1 = User(id = 1,
			username = "Jane Doe",
			picture = "JaneDoe.jpeg",
			email = "abcdefg@gmail.com")

# create Styles table
style_1 = Styles(id = "1",
				type = "MakeUp",
				user_id = 1)
session.add(style_1)
session.commit()

style_2 = Styles(id = "2",
				type = "InteriorDesign",
				user_id = 1)
session.add(style_2)
session.commit()

style_3 = Styles(id = "3",
				type = "Fashion",
				user_id = 1)
session.add(style_3)
session.commit()

"""# create MakeUp_Looks table
mkl_1 = MakeUp_Looks(id = 1,
					occasions = "The Better Version of Yourself",
					style_id = 1)
session.add(mkl_1)
session.commit()

mkl_2 = MakeUp_Looks(id = 2,
					occasions = "Work",
					style_id = 1)
session.add(mkl_2)
session.commit()

mkl_3 = MakeUp_Looks(id = 3, 
					occasions = "Date Night",
					style_id = 1)
session.add(mkl_3)
session.commit()

mkl_4 = MakeUp_Looks(id = 4,
					occasions = "Party",
					style_id = 1)
session.add(mkl_4)
session.commit()

mkl_5 = MakeUp_Looks(id = 5,
					occasions = "School",
					style_id = 1)
session.add(mkl_5)
session.commit()

# create the HomeDecor table
HD_1 = HomeDecor(id = 1,
				occasion = "Modern",
				style_id = 2)
session.add(HD_1)
session.commit()

HD_2 = HomeDecor(id = 2,
				occasion = "Vintage/Retro",
				style_id = 2)
session.add(HD_2)
session.commit()

HD_3 = HomeDecor(id = 3,
				occasion = "Country",
				style_id = 2)
session.add(HD_3)
session.commit()

HD_4 = HomeDecor(id = 4,
				occasion = "Minimalist",
				style_id = 2)
session.add(HD_4)
session.commit()

HD_5 = HomeDecor(id = 5,
				occasion = "Luxurious",
				style_id = 2)
session.add(HD_5)
session.commit()

# create Fashion_Looks table
fashion_1 = Fashion(id = 1,
					occasions = "Casual",
					style_id = 3)
session.add(fashion_1)
session.commit()

fashion_2 = Fashoin(id = 2,
					occassions = "Work",
					style_id = 3)
session.add(fashion_2)
session.commit()

fashion_3 = Fashion(id = 3,
					occasion = "Date Night",
					style_id = 3)
session.add(fashion_3)
session.commit()

fashion_4 = Fashion(id = 4,
					occasion = "Party",
					style_id = 3)
session.add(fashion_4)
session.commit()

fashion_5 = Fashion(id = 5,
					occasion = "Airport/Travel",
					style_id = 3)
session.add(fashion_5)
session.commit()

fashion_6 = Fashion(id = 6,
					occasion = "Lounge Wear",
					style_id = 3)
session.add(fashion_6)
session.commit()

fashion_7 = Fashion(id = 7,
					occasion = "Sports",
					style_id = 3)
session.add(fashion_7)
session.commit()"""

# create Influencers table
influencer_1 = Influencers(id = 1, 
						name = "Anna Newton",
						country = "England",
						blog_name = "The Anna Edit",
						description = "A twenty-something Brighton-dweller with a love for lipstick, lycra and leaf-print homewares. ",
						picture = "influencer_1.jpeg",
						user_id = 1,
						style_id = 1)
session.add(influencer_1)
session.commit()

influencer_2 = Influencers(id = 2,
						name = "Meng Mao",
						country = "France",
						blog_name = "mmeng.mao",
						description = "Chinese high end fashion stylist in France.",
						picture = "influencer_2.jpeg",
						user_id = 1,
						style_id = 3)
session.add(influencer_2)
session.commit()

influencer_3 = Influencers(id= 3,
						name = "Leia Sfez",
						country = "France",
						blog_name = "Leia Sfez",
						description = "A KIND OF JOURNAL, WITH A LOT OF SWEARWORDS",
						picture = "influencer_3.jpeg",
						user_id = 1,
						style_id = 3)
session.add(influencer_3)
session.commit()

influencer_4 = Influencers(id = 4,
						name = "Julia Engel",
						country = "America",
						blog_name = "Gal Meets Glam",
						description = "A Charleston Based Style and Beauty Blog by Julia Engel.",
						picture = "influencer_4.jpeg",
						user_id = 1,
						style_id = 3)
session.add(influencer_4)
session.commit()

influencer_5 = Influencers(id = 5,
						name = "Lily Pebbles",
						country = "England",
						blog_name = "Lily Pebbles",
						description = "A full-time Londoner living in denim, usually found vlogging & taking photos of food.",
						picture = "influencer_5.jpeg",
						user_id = 1,
						style_id = 1)
session.add(influencer_5)
session.commit()

influencer_6 = Influencers(id = 6,
						name = "Anna Jane",
						country = "America",
						blog_name = "SeeAnnaJane",
						description = "A 32 year old who loves her family, friends, laughing, sarcasm, style, cooking, and the occasional DIY.",
						picture = "influencer_6.jpeg",
						user_id = 1,
						style_id = 3)
session.add(influencer_6)
session.commit()

influencer_7 = Influencers(id = 7,
						name = "Violette",
						country = "France",
						blog_name = "violette_fr",
						description = "Makeup Artist Violette on the consummate French girl beauty routines.",
						picture = "influencer_7.jpeg",
						user_id = 1,
						style_id = 1)
session.add(influencer_7)
session.commit()

influencer_8 = Influencers(id = 8,
						name = "Lucy Cuneo",
						country = "America",
						blog_name = "Lucy Cuneo",
						description = "Photographer, artist, content creator. Charleston-based, world traveler. Wife, mom, style lover and natural over-sharer.",
						picture = "influencer_8.jpeg",
						user_id = 1,
						style_id = 2)
session.add(influencer_8)
session.commit()

print ("The Influencers, their Styles, MakeUps, HomeDecors, and Fashion are all here and ready to go!")