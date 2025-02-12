import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import inspect  # ← こちらのみ残す
from db_control.mymodels_MySQL import Base, Customers  # mymodels_MySQL から Base と Customers をインポート
from db_control.connect_MySQL import engine  # `connect_MySQL.py` から engine を使用

# 環境変数の読み込み
base_path = Path(__file__).parents[1]  # backendディレクトリへのパス
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

def init_db():
    """ データベースのテーブルを作成する関数 """
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    print("Checking tables...")

    # customersテーブルが存在しない場合のみ作成
    if 'customers' not in existing_tables:
        print("Creating tables >>> ")
        try:
            Base.metadata.create_all(bind=engine)
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise
    else:
        print("Tables already exist.")

if __name__ == "__main__":
    init_db()

''' 20250211コメントアウト
# テーブルの定義
class Customer(Base):
   __tablename__ = 'customers'

   id = Column(Integer, primary_key=True, autoincrement=True)
   customer_id = Column(String(50), unique=True, nullable=False)
   customer_name = Column(String(100), nullable=False)
   age = Column(Integer)
   gender = Column(String(10))

   def __repr__(self):
       return f"<Customer(customer_id='{self.customer_id}', name='{self.customer_name}')>"

# テーブルの作成
Base.metadata.create_all(engine)

# セッションの作成
Session = sessionmaker(bind=engine)
session = Session()

def add_test_data():
   # 既存のデータを削除
   with engine.connect() as connection:
       connection.execute(text("DELETE FROM customers"))
       connection.commit()
   
   test_customers = [
       Customer(customer_id='C1111', customer_name='ああ', age=6, gender='男'),
       Customer(customer_id='C110', customer_name='桃太郎', age=30, gender='女')
   ]
   
   for customer in test_customers:
       session.add(customer)
   
   try:
       session.commit()
       print("テストデータを追加しました")
   except Exception as e:
       session.rollback()
       print(f"エラーが発生しました: {e}")
   finally:
       session.close()

# この行を追加
if __name__ == "__main__":
    add_test_data()  # テストデータの追加を実行
'''