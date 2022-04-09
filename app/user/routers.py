from .schemas import UserSchema, UserSchemaUpdate, UserSchemaDelete, UserSchemaCreate
from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from util.serializer import MongoId
from typing import Optional


router_user = APIRouter(tags=["USER"], prefix="/user")


@router_user.post(
    "/add", response_description="Add new user", response_model=UserSchema
)
async def create_user(request: Request, user: UserSchemaCreate):
    user = jsonable_encoder(user)
    await request.app.mongodb["user"].insert_one(user)
    user = MongoId.serializerMongoId(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=user)


@router_user.get(
    "/list", response_description="List all users", response_model=list[UserSchema]
)
async def list_users(request: Request, limit: Optional[int] = None):
    user_collection = request.app.mongodb["user"]
    count = await user_collection.count_documents({})
    users = await user_collection.find().to_list(limit or count)
    users = MongoId.serializerMongoId(users, is_empty="There is not user")
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)


@router_user.get(
    "/retrieve/{_id}", response_description="Retrieve user", response_model=UserSchema
)
async def retrieve_user(request: Request, _id: str):
    user = await request.app.mongodb["user"].find_one({"_id": MongoId(_id)})
    user = MongoId.serializerMongoId(
        user, is_empty=f"There is not user with this id: {_id}"
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@router_user.patch(
    "/update/{_id}", description="Update user", response_model=UserSchema
)
async def update_user(request: Request, user: UserSchemaUpdate, _id: str):
    user_collection = request.app.mongodb["user"]
    user_db = await user_collection.find_one({"_id": MongoId(_id)})
    user_db = MongoId.serializerMongoId(
        user_db, is_empty=f"There is not user with this id: {_id}"
    )

    user_update = jsonable_encoder(user)
    user_update = {
        key: value
        for key, value in user_update.items()
        if not isinstance(value, type(None))
    }
    user_db.update(user_update)

    await user_collection.update_one(
        {"_id": MongoId(_id)},
        {"$set": {key: value for key, value in user_db.items()}},
    )
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=user_db)


@router_user.delete(
    "/delete/{_id}", description="Delete user", response_model=UserSchemaDelete
)
async def delete_user(request: Request, _id: str):
    user_collection = request.app.mongodb["user"]
    user_db = await user_collection.find_one({"_id": MongoId(_id)})
    user_db = MongoId.serializerMongoId(
        user_db, is_empty=f"There is not user with this id: {_id}"
    )

    await user_collection.delete_one({"_id": MongoId(_id)})
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"detail": f"User {_id} deleted"}
    )
