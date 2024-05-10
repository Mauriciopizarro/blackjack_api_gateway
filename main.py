from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import infrastructure.injector # no remove this dependecy
from infrastructure.event_managers.rabbit_conection import RabbitConnection
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
    reset_password_controller,
    make_bet_controller,
    get_wallet_controller
)

queues = ["password_updated_send_email",
          "user_created_send_email",
          "create_new_wallet"
          ]
channel = RabbitConnection.get_channel()
RabbitConnection.declare_queues(channel, queues)


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
app.include_router(make_bet_controller.router)
app.include_router(get_wallet_controller.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
