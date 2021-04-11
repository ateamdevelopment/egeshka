from src.utils import image_base
from tests.conftest import parameterize


@parameterize('folder', (None, '/test_folder'))
def test_image_base(test_image, folder):
    url = image_base.save(
        image_data=test_image.read(),
        folder=folder,
        id=-1
    )
    image_base.delete(url)
