import imp
from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        
        if store:
            return store.json()
        else:
            return {'message': 'Store not found'}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        
        if store:
            return {'message': f'A store with name {name} already exists.'}, 400
        else:
            new_store = StoreModel(name)
            try:
                new_store.save_to_db()
            except:
                return {'message': 'An error occured inserting the item.'}, 500

            return new_store.json(), 201    

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': f'Delete {name} store successfully'}, 200
        else:
            return {'message': f'There is no {name} store.'}, 204


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda store: store.json(), StoreModel.query.all()))}


