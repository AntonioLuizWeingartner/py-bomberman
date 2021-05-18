from typing import Callable, List, Dict, Any

class EventSystem:

    """
    Esta classe representa um sistema de eventos. O principal objetivo desta classe é fornecer uma interface unificada pela qual
    diferentes objetos podem se comunicar de forma indireta.
    """

    def __init__(self):
        self.__registered_methods: Dict[str, List[Callable]] = dict()

    def listen(self, message: str, callback: Callable, sender: Any = None):
        """
        Registra um método para responder a mensagens do tipo indicado pelo parâmetro message.
        """
        message = message + str(id(sender)) if sender is not None else message
        if message in self.__registered_methods:
            if callback not in self.__registered_methods[message]:
                self.__registered_methods[message].append(callback)
        else:
            callback_list: List[Callable] = list()
            callback_list.append(callback)
            self.__registered_methods[message] = callback_list

    def stop_listening(self, message: str, callback: Callable, sender: Any = None):
        """
        Remove o interesse de um método pela mensagem identificada pelo parâmetro message.
        """
        message = message + str(id(sender)) if sender is not None else message
        if message in self.__registered_methods:
            if callback in self.__registered_methods[message]:
                self.__registered_methods[message].remove(callback)
                if not self.__registered_methods[message]:
                    del self.__registered_methods[message]

    def broadcast(self, message: str, sender: Any = None, *args: List[Any], **kwargs):
        """
        Executa todos os métodos que tem interesse na mensagem identificada pelo parâmetro message.
        """
        message = message + str(id(sender)) if sender is not None else message
        if message in self.__registered_methods:
            for callback in self.__registered_methods[message]:
                callback(*args, **kwargs)