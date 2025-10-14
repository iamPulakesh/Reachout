import logging
from typing import Iterable, List
from db.connection import s3, BUCKET

logger = logging.getLogger(__name__)

def delete_object(key: str) -> bool:
    """Delete a single S3 object. Returns True if success, False otherwise."""
    if not key:
        return False
    try:
        s3.delete_object(Bucket=BUCKET, Key=key)
        logger.info("Deleted S3 object", extra={"key": key})
        return True
    except Exception as e:
        logger.error(f"Failed to delete S3 object {key}: {e}")
        return False

def delete_objects(keys: Iterable[str]) -> List[str]:
    """Bulk delete S3 objects. Returns list of keys that failed to delete."""
    failed = []
    batch = [k for k in keys if k]
    if not batch:
        return failed
    # Use multi-object delete for efficiency if more than 1
    if len(batch) > 1:
        try:
            response = s3.delete_objects(
                Bucket=BUCKET,
                Delete={"Objects": [{"Key": k} for k in batch], "Quiet": True},
            )
            errors = response.get("Errors", [])
            for err in errors:
                failed.append(err.get("Key"))
            for k in batch:
                if k not in failed:
                    logger.info("Deleted S3 object", extra={"key": k})
        except Exception as e:
            logger.error(f"Bulk delete failed: {e}")
            return batch  # all considered failed
    else:
        # Single
        if not delete_object(batch[0]):
            failed.append(batch[0])
    return failed
