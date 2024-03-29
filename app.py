import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


#buscar lojas
@app.get("/store")
def get_stores():
    return {"stores":list(stores.value())}
    
@app.get("/store<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404,message="Storage not found")
        

#criar lojas
@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex #f5f564564165ff8684d6
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201
    

#criar itens
@app.post("/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    abort(404,message="Storage not found")
    

#buscar items em uma loja especifica   
@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    abort(404,message="Storage not found")
    
    
    
        
if __name__ == '__main__':
    app.run(debug=True, port=8000)