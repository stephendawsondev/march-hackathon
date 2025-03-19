from cloudinary_storage.storage import (
    StaticHashedCloudinaryStorage,
    MediaCloudinaryStorage,
)
import logging

logger = logging.getLogger(__name__)


class EmptySafeStaticCloudinaryStorage(StaticHashedCloudinaryStorage):
    """
    Custom storage class that skips empty files when uploading to Cloudinary
    """

    def _save(self, name, content):
        if hasattr(content, "size") and content.size == 0:
            logger.warning(f"Skipping empty file: {name}")
            return name
        return super()._save(name, content)


class EmptySafeMediaCloudinaryStorage(MediaCloudinaryStorage):
    """
    Custom storage class that skips empty files when uploading to Cloudinary
    """

    def _save(self, name, content):
        # Check if the file is empty
        if hasattr(content, "size") and content.size == 0:
            # Just return the name without uploading
            return name

        # If content doesn't have size attribute or isn't empty, upload it
        return super()._save(name, content)
