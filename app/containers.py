from dependency_injector import containers, providers
from app.application.services.client_service import ClientService
from app.infrastructure.repositories.client_repository import ClientRepository

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    client_repository = providers.Factory(ClientRepository)
    client_service = providers.Factory(
        ClientService,
        repository=client_repository
    )