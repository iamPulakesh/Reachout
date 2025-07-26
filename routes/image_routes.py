from flask import Blueprint, redirect
from db.connection import s3, BUCKET

image_bp = Blueprint('image', __name__)

@image_bp.route('/view-image/<image_name>')
def view_image(image_name):
    try:
        signed_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET, 'Key': image_name},
            ExpiresIn=300
        )
        return redirect(signed_url)
    except Exception as e:
        return f"Error generating signed URL: {e}"
