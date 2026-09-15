from os import PathLike

from crypt_image import CryptImage
from consts import ENCODING


class Card:
    def __init__(
        self,
        name: str,
        creator: str,
        image: CryptImage,
        riddle: str,
        solution: str | None,
    ):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self):
        return f"<Card name={self.name}, creator={self.creator}>"

    def __str__(self):
        return f"Card {self.name} by {self.creator}\nriddle: {self.riddle}\nsolution: {self.solution if self.solution is not None else 'unsolved'}"

    @classmethod
    def create_from_path(
        cls, name: str, creator: str, path: str | PathLike, riddle: str, solution: str
    ):
        return Card(name, creator, CryptImage.create_from_path(path), riddle, solution)

    def serialize(self) -> bytes:
        name_length = len(self.name).to_bytes(4, "little")
        name = bytes(self.name, ENCODING)
        ceator_length = len(self.creator).to_bytes(4, "little")
        creator = bytes(self.creator, ENCODING)
        image_bytes = self.image.serialize()
        image_length = len(image_bytes).to_bytes(4, "little")
        riddle_length = len(self.riddle).to_bytes(4, "little")
        riddle = bytes(self.riddle, ENCODING)

        return (
            name_length
            + name
            + ceator_length
            + creator
            + image_length
            + image_bytes
            + riddle_length
            + riddle
        )

    @classmethod
    def deserialize(cls, b: bytes):
        name_length = int.from_bytes(b[:4], "little")
        name = b[4 : 4 + name_length].decode(ENCODING)
        creator_length = int.from_bytes(b[4 + name_length : 8 + name_length], "little")
        creator = b[8 + name_length : 8 + name_length + creator_length].decode(ENCODING)
        image_length = int.from_bytes(
            b[8 + name_length + creator_length : 12 + name_length + creator_length],
            "little",
        )
        image_bytes = b[
            12 + name_length + creator_length : 12
            + name_length
            + creator_length
            + image_length
        ]
        image = CryptImage.deserialize(image_bytes)
        riddle_length = int.from_bytes(
            b[
                12 + name_length + creator_length + image_length : 16
                + name_length
                + creator_length
                + image_length
            ],
            "little",
        )
        riddle = b[
            16 + name_length + creator_length + image_length : 16
            + name_length
            + creator_length
            + image_length
            + riddle_length
        ].decode(ENCODING)

        return Card(name, creator, image, riddle, None)


if __name__ == "__main__":
    name = "card1"
    creator = "eitan"
    riddle = "this is a riddle"
    solution = "this is the solution"
    path = "secret.jpg"

    card = Card.create_from_path(name, creator, path, riddle, solution)
    card.image.encrypt(card.solution)
    data = card.serialize()

    card2 = Card.deserialize(data)
    if card2.image.decrypt(solution):
        card2.solution = solution
    assert repr(card) == repr(card2)
    card2.image.image.show()
