# import npyscreen
# from database import TinyDatabase
# from gui import AmvaApplication
# from getter import MTGetter
# from adapter import MTAdapter
# from converter import MTConverter

# if __name__ == "__main__":
#     myApp = AmvaApplication(TinyDatabase(), MTGetter(),
#                             MTAdapter(), MTConverter())
#                 myApp.run()


import sys
from databases import TinyDatabase

# print(sys.path)

TinyDatabase()
