#SQLiteにつなぐ場合
'''
from sqlalchemy import create_engine
# import sqlalchemy

import os
# uname() error回避
import platform
print("platform:", platform.uname())


main_path = os.path.dirname(os.path.abspath(__file__))
path = os.chdir(main_path)
print("path:", path)
engine = create_engine("sqlite:///CRM.db", echo=True)
'''

#MySQLにつなぐ場合
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

# 20250216追記
from pathlib import Path

# 環境変数の読み込み
#load_dotenv(dotenv_path="../frontend/.env")
#load_dotenv(".env.local")  20250216コメントアウト

# 環境変数の読み込み 20250216追記
base_path = Path(__file__).parents[1]  # backendディレクトリへのパス
#env_path = base_path / '.env'      
#load_dotenv(dotenv_path=env_path)   


# データベース接続情報
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# SSL証明書のパス 20250216追記
ssl_cert = str(base_path / 'DigiCertGlobalRootCA.crt.pem') 

# MySQLのURL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジンの作成（SSL設定を追加）　20250216追記
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

# エンジンの作成　20250216コメントアウト
'''
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)
'''

print(f"DB_USER: {DB_USER}")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_NAME: {DB_NAME}")
print(f"DATABASE_URL: {DATABASE_URL}")
