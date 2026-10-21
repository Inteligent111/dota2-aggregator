from fastapi import FastAPI
from app.api.routers import router as carry_routers



app = FastAPI(title="Dota 2 Carry Stats")


app.include_router(carry_routers)


