from api.publications.models import Images, Publication
from utils.imagesS3 import upload_image_to_s3


def get_publication_by_id(publication_id):
    return Publication.objects.get(id=publication_id)


def upload_images(publication_id, images, user_id):
    publication = get_publication_by_id(publication_id)
    owner = publication.owner
    if owner.id != user_id:
        raise Exception("User is not the owner of this publication")
    for file in images.getlist("images"):
        path = "publication/" + str(publication_id) + "/" + file.name
        s3_path = upload_image_to_s3(file, path)
        image = Images(image_path=s3_path, publication_id=publication_id)
        image.save()
    return publication
