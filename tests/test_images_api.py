from app.images.models import Image
from app.images.schemas import ImageSchema
from app.main import app


class TestImageAPI:

    def test_file_url(self, client):
        image = Image.query.first()
        file_id = image.file["file_id"]
        resp = client.get(f"/images/{file_id}")
        assert resp.status_code == 200

    def test_list_images(self, client):
        images = Image.query.all()
        with app.test_request_context():
            resp = client.get("/images/?page=1")
            assert resp.status_code == 200
            assert resp.json == ImageSchema(many=True).dump(images)
            assert len(resp.json) == len(images)
