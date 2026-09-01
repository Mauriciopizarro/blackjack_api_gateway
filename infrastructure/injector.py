from infrastructure.authentication.local_auth_provider import LocalAuthProvider
from infrastructure.http_clients.money_service_http_client import MoneyServiceHttpClient
from infrastructure.repositories.user_mongo_repository import UserMongoRepository
from dependency_injector import containers, providers


class Injector(containers.DeclarativeContainer):

    user_repo = providers.Singleton(UserMongoRepository)
    auth_provider = providers.Factory(LocalAuthProvider)
    money_service_http_client = providers.Singleton(MoneyServiceHttpClient)


injector = Injector()
injector.wire(modules=["application.login_service",
                       "application.sign_up_service",
                       "application.token_service",
                       "application.reset_password_service"
                       ])
