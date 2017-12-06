from database_setup import 
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///styleInfluencers.db', echo=True)


# create a session
Session = sessionmaker(bind=engine)
session = DBSession()

# create Style 

style_1 = Styles(id = "1", name = "Make-Up")
session.add(style_1)

style_2 = Styles(id = "2", name = "Interior Design")
session.add(style_2)

style_3 = Styles(id = "3", name = "Fashion")
session.add(style_3)

# create Influencers
influencer_1 = Influencers(id = 1, name = "Anna Newton", country = "England", blog_name = "The Anna Edit", description = "A twenty-something Brighton-dweller with a love for lipstick, lycra and leaf-print homewares. ", style = )
session.add(influencer_1)

influencer_2 = Influencers(id = 2, name = "Meng Mao", country = "Francce", blog_name = "mmeng.mao", description = "Chinese high end fashion stylist in France.", style_id = )
session.add(influencer_2)

influencer_3 = Influencers(id= 3, name = "Lizzy Hadfield", country = "England", blog_name = "Shot From the Street", description = "A blog by Lizzy Hadifeld.", style_id = )
session.add(influencer_3)

influencer_4 = Influencers(id = 4,name = "Lena", country = "Korea", blog_name = "twinklinglena", description = "Korean Medical Student Vlogger.", style_id = )
session.add(influencer_4)

influencer_5 = Influencers(id = 5, name = "Lily Pebbles", country = "England", blog_name = "Lily Pebbles", description = "A full-time Londoner living in denim, usually found vlogging & taking photos of food.", style_id = )
session.add(influencer_5)

influencer_6 = Influencers(id = 6, name = "Anna", country = "America", blog_name = "SeeAnnaJane", description = "A 32 year old who loves her family, friends, laughing, sarcasm, style, cooking, and the occasional DIY.", style_id = )
session.add(influencer_6)

influencer_7 = Influencers(id = 7, name = "Violette", country = "France", blog_name = "violette_fr", description = "Makeup Artist Violette on the consummate French girl beauty routines.", style_id = )
session.add(influencer_7)

influencer_8 = Influencers(id = 8, name = "Lucy Cuneo", country = "America", blog_name = "Lucy Cuneo", description = "Photographer, artist, content creator. Charleston-based, world traveler. Wife, mom, style lover and natural over-sharer.", style_id = )

# create MakeUp_Looks
mkl_1 = MakeUp_Looks(id = 1, occasions = "The Better Version of Yourself")
session.add(mkl_1)

mkl_2 = MakeUp_Looks(id = 2, occasions = "Work")
session.add(mkl_2)

mkl_3 = MakeUp_Looks(id = 3, occasions = "Date Night" )
session.add(mkl_3)

mkl_4 = MakeUp_Looks(id = 4, occasions = "Party")
session.add(mkl_4)

mkl_5 = MakeUp_Looks(id = 5, occasions = "School")
session.add(mkl_5)

# create Fashion_Looks
fashion_1 = Fashion(id = 1, occasions = "Casual")
session.add(fashion_1)

fashion_2 = Fashoin(id = 2, occassions = "Work")
session.add(fashion_2)

fashion_3 = Fashion(id = 3, occasion = "Date Night")
session.add(fashion_3)

fashion_4 = Fashion(id = 4, occasion = "Party")
session.add(fashion_4)

fashion_5 = Fashion(id = 5, occasion = "Airport/Travel")
session.add(fashion_5)

fashion_6 = Fashion(id = 6, occasion = "Lounge Wear")
session.add(fashion_6)

fashion_7 = Fashion(id = 7, occasion = "Sports")
session.add(fashion_7)

# create Home Decor

HD_1 = HomeDecor(id = 1, occasion = "Modern")
session.add(HD_1)

HD_2 = HomeDecor(id = 2, occasion = "Vintage/Retro")
session.add(HD_2)

HD_3 = HomeDecor(id = 3, occasion = "Country")
session.add(HD_3)

HD_4 = HomeDecor(id = 4, occasion = "Minimalist")
session.add(HD_4)

HD_5 = HomeDecor(id = 5, occasion = "Luxurious")
session.add(HD_5)


# commit into the database
session.commit()