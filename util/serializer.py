from fastapi import HTTPException, status
from bson.errors import InvalidId
from bson import ObjectId


class MongoId(ObjectId):
    """
    Manage ObjectId (MongoId by default) and converted to native Python datatypes
    """

    def __init__(self, id: str) -> None:
        try:
            super().__init__(id)
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="it must be a 12-byte input or a 24-character hex string",
            )

    @staticmethod
    def serializerMongoId(collection, is_empty="Not found"):
        if not collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=is_empty)

        if isinstance(collection, dict):
            collection["id"] = str(collection["_id"])
            del collection["_id"]
            return collection

        if isinstance(collection, list):
            list_collection: list = []
            for row in collection:
                row["id"] = str(row["_id"])
                del row["_id"]
                list_collection.append(row)
            return list_collection

        raise Exception(
            f"You are implementing {MongoId.serializerMongoId.__name__!r} wrong."
        )

    def __str__(self) -> str:
        return super().__str__()
