from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from db_control import crud, mymodels


# UUIDを生成するためのライブラリをインポート
import uuid


# MySQLのテーブル作成
from db_control.create_tables import init_db

# # アプリケーション初期化時にテーブルを作成
init_db()


class Customer(BaseModel):
    #customer_id: str  # customer_idを除外（自動生成するため）
    customer_name: str
    age: int
    gender: str


app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "FastAPI top page!"}

'''
@app.post("/customers")
def create_customer(customer: Customer):
    values = customer.dict()
    tmp = crud.myinsert(mymodels.Customers, values)
    result = crud.myselect(mymodels.Customers, values.get("customer_id"))

    if result:
        result_obj = json.loads(result)
        return result_obj if result_obj else None
    return None
'''


@app.get("/customers")
def read_one_customer(customer_id: str = Query(...)):
    result = crud.myselect(mymodels.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

@app.get("/allcustomers")
def read_all_customer():
    result = crud.myselectAll(mymodels.Customers)
    # 結果がNoneの場合は空配列を返す
    if not result:
        return []
    # JSON文字列をPythonオブジェクトに変換
    return json.loads(result)

@app.post("/customers")
def create_customer(customer: Customer):

    # 最大試行回数を設定
    MAX_ATTEMPTS = 3
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        # 試行回数をインクリメント
        attempts += 1

        # UUIDを生成
        generated_id = str(uuid.uuid4())
        print(f"Attempt {attempts}: generated_id: {generated_id}")

        # IDが存在しない場合のみ処理を続行
        if generated_id != crud.myselect(mymodels.Customers, generated_id):
            # 受け取ったデータにcustomer_idを追加
            values = customer.dict()
            values["customer_id"] = generated_id
            print("values:", values)

            # データベースに保存
            tmp = crud.myinsert(mymodels.Customers, values)
            result = crud.myselect(mymodels.Customers, generated_id)

            if result:
                result_obj = json.loads(result)
                return result_obj[0] if result_obj else None
            return None

    # 最大試行回数を超えた場合はエラーを返す
    raise HTTPException(
        status_code=500,
        detail="Failed to generate unique ID after maximum attempts"
    )

'''   
@app.put("/customers")
def update_customer(customer: Customer):
'''
@app.put("/customers/{customer_id}")
def update_customer(customer_id: str, customer: CustomerUpdate): #20250209修正
    values = customer.dict()
    values_original = values.copy()
    tmp = crud.myupdate(mymodels.Customers, values)
    result = crud.myselect(mymodels.Customers, values_original.get("customer_id"))
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None


@app.delete("/customers")
def delete_customer(customer_id: str = Query(...)):
    result = crud.mydelete(mymodels.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"customer_id": customer_id, "status": "deleted"}


@app.get("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json()
