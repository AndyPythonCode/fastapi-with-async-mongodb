# Include the router in the tuple and it will be shown in the application

from app.user.routers import router_user

URL_PATTERNS = (router_user,)
