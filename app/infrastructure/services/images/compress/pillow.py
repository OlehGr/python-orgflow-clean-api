import io
from pathlib import Path
from typing import ClassVar

from PIL import Image

from app.core.application.dto.file import ImagerCompressResult
from app.core.application.interfaces.services.file import IImageCompressor


class PillowImageCompressor(IImageCompressor):
    quality: ClassVar[int] = 75

    async def compress_image(self, *, image_data: bytes, image_name: str) -> ImagerCompressResult:

        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        optimized_bytes = self._optimize_image(image)

        return ImagerCompressResult(
            optimized_data=optimized_bytes,
            file_name=str(Path(image_name).with_suffix(".webp")),
            content_type="image/webp",
        )

    def _optimize_image(self, image: Image.Image) -> bytes:
        optimized_buffer = io.BytesIO()
        image.thumbnail((1280, 1280))
        image.save(
            optimized_buffer,
            format="WEBP",
            quality=self.quality,
            optimize=True,
        )
        return optimized_buffer.getvalue()
