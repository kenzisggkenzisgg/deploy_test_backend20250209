import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker

# 環境変数の読み込み
base_path = Path(__file__).parents[1]  # backendディレクトリへのパス
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

# データベース接続情報
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '3306')  # デフォルト値を設定
DB_NAME = os.getenv('DB_NAME')

# SSL証明書のパス
ssl_cert = str(base_path / 'DigiCertGlobalRootCA.crt.pem')

# MySQLのURL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジンの作成（SSL設定を追加）
engine = create_engine(
   DATABASE_URL,
   connect_args={
       "ssl": {
           "ssl_ca": ssl_cert
       }
   },
   echo=True,
   pool_pre_ping=True,
   pool_recycle=3600
)

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