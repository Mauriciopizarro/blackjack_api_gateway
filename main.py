import time
from fastapi import FastAPI
from infrastructure.event_managers.rabbit_publisher import RabbitConnection
import infrastructure.injector # no remove this dependecy
from infrastructure.controllers import (
    create_game_controller,
    sign_up_controller,
    start_game_controller,
    deal_card_controller,
    login_controller,
    stand_controller,
    enroll_player_controller,
    status_controller,
    croupier_controller,
    history_controller,
    reset_password_controller
)

time.sleep(20)
RabbitConnection.init_connection()

app = FastAPI()

app.include_router(enroll_player_controller.router)
app.include_router(start_game_controller.router)
app.include_router(status_controller.router)
app.include_router(deal_card_controller.router)
app.include_router(stand_controller.router)
app.include_router(croupier_controller.router)
app.include_router(login_controller.router)
app.include_router(sign_up_controller.router)
app.include_router(create_game_controller.router)
app.include_router(history_controller.router)
app.include_router(reset_password_controller.router)
