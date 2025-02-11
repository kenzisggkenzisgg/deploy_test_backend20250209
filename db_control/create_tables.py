#from mymodels import Base  # User, Comment
from db_control.mymodels_MySQL import Base #20250211修正
from connect import engine

import platform
print(platform.uname())


print("Creating tables >>> ")
Base.metadata.create_all(bind=engine)
