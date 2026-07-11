"""Registry for independently extensible presentation presenters."""


class PresentationRegistry:
    def __init__(self): self._presenters: dict[str, object] = {}
    def register(self, name: str, presenter: object) -> None: self._presenters[name] = presenter
    def get(self, name: str): return self._presenters[name]
