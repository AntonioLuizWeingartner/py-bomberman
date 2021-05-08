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

        pass

    def stop_listening(self, message: str, callback: Callable, sender: Any = None):
        """
        Remove o interesse de um método pela mensagem identificada pelo parâmetro message.
        """
        pass

    def broadcast(self, message: str, *args: List[Any], **kwargs: Dict[str, Any]):
        """
        Executa todos os métodos que tem interesse na mensagem identificada pelo parâmetro message.
        """
        pass