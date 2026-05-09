from fastapi import FastAPI
from Routes.UserRoutes import router
from Routes.TaskRoutes import routerTask




app = FastAPI()

app.include_router(router, prefix="/users", tags=["Users"])
app.include_router(routerTask, prefix="/tasks", tags=["Tasks"])

