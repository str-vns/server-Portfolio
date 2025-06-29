from portfolio.utils.Firebase.database import storage, storageFire
from portfolio.utils.Firebase.token import token

import uuid


def upload_helper(image):
    uuidV4 = str(uuid.uuid4()).replace("-", "")
    storageFire.child(f"Portfolio/{uuidV4 + image.name}").put(image, token)

    url = storageFire.child(f"Portfolio/{uuidV4 + image.name}").get_url(token)
    public_id = uuidV4 + image.name
    original_name = image.name

    return {"public_id": public_id, "url": url, "original_name": original_name}

def delete_image_helper(image):
    if not image:
        return {"message": "No image provided to delete"}

    try:
        full_path = f"Portfolio/{image}"
        print("Full path to delete:", full_path)

        bucket = storage  
        blob = bucket.blob(full_path)
        blob.delete()

        return {"message": "Image deleted successfully"}
    except Exception as e:
        print("Error:", e)
        return {"message": f"Error deleting image: {str(e)}"}