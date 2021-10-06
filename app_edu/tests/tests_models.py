from PIL import Image
import shutil
import tempfile

from django.test import TestCase, override_settings
from django.conf import settings
from django.contrib.auth.models import User
from app_edu import models
from django.core.files.uploadedfile import SimpleUploadedFile

MEDIA_ROOT = tempfile.mkdtemp()


# Create your tests here.
@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class PostTests(TestCase):
    """ Post Models tests """
    @classmethod
    def setUpTestData(cls):
        # create user
        cls.user = User.objects.create(username="test", password="12345_test")
        cls.user.save()

        #create categorie
        cls.cat = models.Category.objects.create(
            title="La programmation avancée",
            top_three_cat=False,
        )
        cls.cat.save()

        #create post
        post = models.Post.objects.create(
            title="Apprendre a faire des tests en python",
            disc=True,
            badge="Cours en ligne",
            youtube="http://youtube.com/apprendre_a_faire_des_test_python",
            author=f'{cls.user}',
            category=cls.cat,
            image=SimpleUploadedFile('test_post_img.jpg', b'Whatever content'),
            logo=SimpleUploadedFile('test_post_logo.jpg', b'Whatever content'),
            discount=0,
            price=102,
        )
        post.save()

        cls.image_test = post.image
        cls.logo_test = post.logo

    def test_post_content(self):
        post = models.Post.objects.get(id=1)
        author = f'{post.author}'
        cat = f'{post.category}'
        badge = f'{post.badge}'
        youtube = f'{post.youtube}'
        image = f'{post.image.name}'
        logo = f'{post.logo.name}'
        disc = post.disc
        discount = post.discount
        price = post.price

        self.assertEqual(author, f'{self.user}')
        self.assertEqual(cat, f'{self.cat}')
        self.assertEqual(badge, "Cours en ligne")
        self.assertEqual(
            youtube, "http://youtube.com/apprendre_a_faire_des_test_python")
        # TODO: make dynam le media/post/, avec override_settings or tempfile
        self.assertEqual(image, f'{self.image_test}')
        self.assertEqual(logo, f'{self.logo_test}')
        self.assertEqual(disc, True)
        self.assertEqual(discount, 0)
        self.assertEqual(price, 102)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)  # delete the temp dir
        super().tearDownClass()


class CategoryTests(TestCase):
    """ Category Models tests """
    @classmethod
    def setUpTestData(cls):
        # create category
        cls.cat = models.Category.objects.create(title='cat de test',
                                          top_three_cat=False,
                                          more=True,
                                          disc=True)

    def test_cat_content(self):
        # Get category from db test
        cat = models.Category.objects.get(title="cat de test")
        top_three_cat = cat.top_three_cat
        more = cat.more
        disc = cat.disc
        self.assertEqual(top_three_cat, self.cat.top_three_cat)
        self.assertEqual(more, self.cat.more)
        self.assertEqual(disc, self.cat.disc)


class SubCategoryTests(TestCase):
    """ TestCase for Models Subcat """
    @classmethod
    def setUpTestData(cls):
        # create subcategory
        cls.subcatTest = models.Subcat.objects.create(title="sub cat", disc=True)
        cls.subcatTest.save()

    def test_subCat_content(self):
        #  Get subcategory from db test
        scat = models.Subcat.objects.get(id=1)
        self.assertEqual(scat.title, self.subcatTest.title)
        self.assertEqual(scat.disc, self.subcatTest.disc)


class CustomerTests(TestCase):
    """ TestCase for Models Customer """
    @classmethod
    def setUpTestData(cls):
        # create customer
        cls.customerTest = models.Customer.objects.create(
            user=User.objects.create(
                username="yattara",
                password="12345_test"),
            address="Je suis du Mali",
            mobile="0633239422",
            telephone=733239422,
            country="Malienne",
            city="Bamako",
            state="Rive droite",
            zip_code=20200,
        )
        cls.customerTest.save()

    def test_customer_content(self):
        #  Get cusomer from db test
        cus = models.Customer.objects.get(id=1)

        self.assertEqual(f'{cus.user}', f'{self.customerTest.user}')
        self.assertEqual(f'{cus.address}', f'{self.customerTest.address}')
        self.assertEqual(f'{cus.mobile}', f'{self.customerTest.mobile}')
        self.assertEqual(f'{cus.telephone}', f'{self.customerTest.telephone}')
        self.assertEqual(f'{cus.country}', f'{self.customerTest.country}')
        self.assertEqual(f'{cus.city}', f'{self.customerTest.city}')
        self.assertEqual(f'{cus.state}', f'{self.customerTest.state}')
        self.assertEqual(cus.zip_code, self.customerTest.zip_code)
