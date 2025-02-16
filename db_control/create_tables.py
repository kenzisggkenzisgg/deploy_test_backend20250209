#SQLiteにつなぐ場合
'''
from mymodels import Base  # User, Comment
from connect import engine

import platform
print(platform.uname())


print("Creating tables >>> ")
Base.metadata.create_all(bind=engine)
'''

#MySQLにつなぐ場合
# 20250216 3行追記
import os
from pathlib import Path
from dotenv import load_dotenv

from db_control.mymodels import Base
from db_control.connect import engine
from sqlalchemy import inspect

# 環境変数の読み込み 20250216追記
base_path = Path(__file__).parents[1]  # backendディレクトリへのパス
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)


def init_db():
    # インスペクターを作成
    inspector = inspect(engine)

    # 既存のテーブルを取得
    existing_tables = inspector.get_table_names()

    print("Checking tables...")

    # customersテーブルが存在しない場合は作成
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