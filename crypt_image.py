from os import PathLike
import hashlib
from consts import ENCODING
from Crypto.Cipher import AES

from PIL import Image


class CryptImage:
    def __init__(self, image: Image, key_hash: bytes | None = None):
        self.image = image
        self.key_hash = key_hash

    @classmethod
    def create_from_path(cls, path: str | PathLike):
        return CryptImage(Image.open(path))

    def _hash(self, b):
        return hashlib.sha256(b).digest()

    def encrypt(self, key: str) -> None:
        self.key_hash = self._hash(self._hash(bytes(key, ENCODING)))

        raw_image = self.image.tobytes()
        aes = AES.new(self._hash(bytes(key, ENCODING)), AES.MODE_EAX, nonce=b"arazim")
        encrypted_raw = aes.encrypt(raw_image)

        self.image = Image.frombytes("RGB", self.image.size, encrypted_raw)

    def decrypt(self, key: str):
        hash = self._hash(self._hash(bytes(key, ENCODING)))
        if hash != self.key_hash:
            return False

        raw_encrypted = self.image.tobytes()
        aes = AES.new(self._hash(bytes(key, ENCODING)), AES.MODE_EAX, nonce=b"arazim")
        raw = aes.decrypt(raw_encrypted)

        self.image = Image.frombytes("RGB", self.image.size, raw)
        self.key = None

        return True

    def serialize(self) -> bytes:
        if self.key_hash is None:
            raise ValueError("Image must be encrypted before serialization")

        height_bytes = self.image.height.to_bytes(4, "little")
        width_bytes = self.image.width.to_bytes(4, "little")
        image_bytes = self.image.tobytes()

        return height_bytes + width_bytes + image_bytes + self.key_hash

    @classmethod
    def deserialize(cls, b: bytes):
        height = int.from_bytes(b[:4], "little")
        width = int.from_bytes(b[4:8], "little")
        image_bytes = b[8:-32]
        key_hash = b[-32:]

        image = Image.frombytes("RGB", (width, height), image_bytes)
        return CryptImage(image, key_hash)


if __name__ == "__main__":
    ci = CryptImage(Image.open("secret.jpg"))
    ci.encrypt("0" * 16, ENCODING)
    ci.decrypt("0" * 16, ENCODING)
    ci.image.save("copy.jpg")
