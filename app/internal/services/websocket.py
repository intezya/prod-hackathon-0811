import hashlib
from typing import Optional

from fastapi import WebSocket


def pop_from_dict_by_value[KT_, VT_](dict_instance: dict, value: VT_) -> KT_:
    key = next((k for k, v in dict_instance.items() if v == value), None)

    if key is not None:
        dict_instance.pop(key)
        return key
    raise ValueError("Value not found in dictionary!")


class WebsocketService:
    def __init__(self):
        self.__connections: dict[str, WebSocket] = {}

    @staticmethod
    def __hash(user_name: str, id_from_link: str):
        return hashlib.sha256((user_name + id_from_link).encode()).hexdigest()

    async def connect(
        self,
        websocket: WebSocket,
        user_name: str,
        id_from_link: str,
    ):
        user_unique_value = self.__hash(user_name, id_from_link)

        await websocket.accept()
        self.__connections[user_unique_value] = websocket

    def disconnect(
        self,
        websocket: Optional[WebSocket],
        user_name: Optional[str],
        id_from_link: Optional[str],
    ):
        user_unique_value = self.__hash(user_name, id_from_link)

        if user_name and id_from_link:
            self.__connections.pop(user_unique_value)
        elif websocket:
            pop_from_dict_by_value(
                dict_instance=self.__connections,
                value=websocket,
            )
        else:
            raise ValueError("No user_name and link_id or websocket provided!")

    def get(
        self,
        *,
        user_name: Optional[str],
        id_from_link: Optional[str],
    ) -> WebSocket | None:
        user_unique_value = self.__hash(user_name, id_from_link)
        return self.__connections.get(user_unique_value)


# Global variable
main_websocket_service = WebsocketService()
