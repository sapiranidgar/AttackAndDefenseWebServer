from typing import Generic, TypeVar

from overrides import override

T = TypeVar('T')


class Response(Generic[T]):
    def __init__(self, data: T = None, error_msg: str = "", status_code: int = 200):
        self.__error_msg = error_msg
        self.__status_code = status_code
        self._data = data

    def get_error_msg(self) -> str:
        return self.__error_msg

    def get_status_code(self) -> int:
        return self.__status_code

    def get_data(self) -> T:
        raise Exception("This is an error response. No data available.")

    def is_successful(self) -> bool:
        return False


class DataResponse(Response):
    def __init__(self, data: T):
        super().__init__(data)

    @override
    def get_data(self) -> T:
        return self._data

    @override
    def get_error_msg(self) -> str:
        raise Exception("This is a data response, no error message.")

    @override
    def is_successful(self) -> bool:
        return True
