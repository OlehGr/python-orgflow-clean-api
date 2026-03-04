import io

import blurhash
from PIL import Image

from app.core.application.interfaces.services.file import IImageHasher


class BlurHashImageHasher(IImageHasher):
    async def hash_image(self, image_data: bytes) -> str:
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        image.thumbnail((100, 100))
        return blurhash.encode(image, x_components=4, y_components=3)
