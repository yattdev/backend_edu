from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator


class Customer(models.Model):
    """ Model for customer/user """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='media/profile_pic',
                                    null=True,
                                    blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    country = models.CharField(max_length=20, null=False, blank=True)
    company = models.CharField(max_length=20, null=False, blank=True)
    city = models.CharField(max_length=20, null=False, blank=True)
    state = models.CharField(max_length=20, null=False, blank=True)
    zip_code = models.IntegerField(blank=True, default="1")
    telephone = models.IntegerField(blank=True, default="1")

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name


class Category(models.Model):
    parent = models.ForeignKey('self',
                               related_name='children',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title',
                         unique=True,
                         null=False,
                         editable=True)
    logo = models.ImageField(upload_to='media/catlogo',
                             blank=True,
                             null=True,
                             help_text='Optional')
    top_three_cat = models.BooleanField(default=False)
    more = models.BooleanField(default=False,
                               blank=True,
                               verbose_name="For Add In Right Menu")
    created_at = models.DateTimeField(auto_now_add=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')
    hit = models.PositiveIntegerField(default=0, verbose_name="nombre de hits")

    def post_count(self):
        return self.posts.all().count()

    class Meta:
        #enforcing that there can not be two categories under a parent with same slug
        # __str__ method elaborated later in post.  use __unicode__ in place of

        unique_together = (
            'slug',
            'parent',
        )
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    #  Return category full path
    @property
    def full_path(self):
        full_path = [self.title]
        k = self.parent

        while k is not None:
            full_path.append(k.title)
            k = k.parent

        return full_path[::-1]


class Subcat(models.Model):
    parent = models.ForeignKey(Category,
                               on_delete=models.CASCADE,
                               related_name='Subcat',
                               blank=True,
                               null=True,
                               help_text='Select Only Sub Category')
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')

    class Meta:
        # enforcing that there can not be two categories under a parent with same slug

        # __str__ method elaborated later in post.  use __unicode__ in place of

        unique_together = (
            'slug',
            'parent',
        )
        #This is for outside or main which shows outside panel.
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.title

    @property
    def full_path(self):
        full_path = [self.title]
        k = self.parent

        while k is not None:
            full_path.append(k.title)
            k = k.parent

        return full_path[::-1]


class MainCourse(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title',
                         unique=True,
                         null=False,
                         editable=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')

    def __str__(self):
        return self.title


class Post(models.Model):
    """ """
    title = models.CharField(max_length=500)
    meta_tags = models.CharField(max_length=2000, blank=True)
    meta_desc = models.TextField(max_length=2000, blank=True)
    slug = AutoSlugField(populate_from='title',
                         max_length=500,
                         unique=True,
                         null=False)
    image = models.ImageField(upload_to='media/post')
    image_alt_name = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(
        upload_to='media/post'
    )  #If user want to add university logo(Slider and Post)
    desc = RichTextField(blank=True, null=True)
    #for live classes or offline classes
    badge = models.CharField(max_length=70,
                             verbose_name="For live class or offline")
    youtube = models.URLField(max_length=500, default='')
    # TODO: create auth user with permission and associat with author field
    author = models.CharField(max_length=20, default="admin")
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 default=1,
                                 related_name="posts")
    subcategory = models.ForeignKey(Subcat,
                                    on_delete=models.CASCADE,
                                    related_name="Subcat",
                                    blank=True,
                                    null=True)
    hit = models.PositiveIntegerField(
        default=0)  #This field is for popular posts
    button_text = models.CharField(
        max_length=20, default="Apply Now")  #Apply Now and enroll button text
    slider_post = models.BooleanField(default=False, blank=True)
    maincourse = models.ManyToManyField(MainCourse,
                                        blank=True,
                                        related_name='posts')
    price = models.IntegerField(default=0)
    old_price = models.IntegerField(default=0)
    discount = models.IntegerField()
    emi_start_price = models.IntegerField(null=True)
    why_title = models.CharField(max_length=500, blank=True)
    disc = models.BooleanField(default=False, verbose_name='Add In Disclaimer')

    def __str__(self):
        return self.title

    def get_rating(self):
        total = sum(int(review['stars']) for review in self.review.values())

        return total / self.reviews.count()

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.image = self.compressImage(self.image)
    #     super(Upload, self).save(*args, **kwargs)

    # def compressImage(self,image):
    #     imageTemproary = Image.open(image)
    #     outputIoStream = BytesIO()
    #     imageTemproaryResized = imageTemproary.resize( (1300,400) )
    #     imageTemproary.save(outputIoStream , format='JPEG', quality=60)
    #     outputIoStream.seek(0)
    #     image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
    #     return image


class Curriculam(models.Model):
    """ Les modules du cours """
    title = models.CharField(max_length=500)
    Post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='Accroche_posts')
    content = RichTextField(blank=True, null=True)


class faq(models.Model):
    """ Frequentes Ask question """
    title = models.CharField(max_length=500)
    Post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='faq_posts')
    content = RichTextField(blank=True, null=True)


class timing(models.Model):
    date = models.CharField(max_length=100, blank=True, null=True)
    day_duration = models.CharField(max_length=100, blank=True, null=True)
    time_duration1 = models.CharField(max_length=100, blank=True, null=True)
    time_duration2 = models.CharField(max_length=100, blank=True, null=True)
    Post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='time_posts')


class Certificate(models.Model):
    cert_file = models.FileField(upload_to='media/certificate',
                                 null=True,
                                 blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='cert_posts')


class features(models.Model):
    title = models.CharField(max_length=500)
    Post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='feature_posts')
    content = RichTextField(blank=True, null=True)


class boxes_three(models.Model):
    title = models.CharField(max_length=70)
    slug = AutoSlugField(populate_from='title',
                         unique=True,
                         null=False,
                         editable=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments')
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


class promocode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    # discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    amount = models.FloatField()
    active = models.BooleanField()

    def __str__(self):
        return self.code


class Cart(models.Model):
    cart_id = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='cart')
    item = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='item')
    purchase = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    certificate = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.item}'

    def get_total(self):
        total = self.item.price
        float_total = format(total, '0.2f')

        return float_total


class Order(models.Model):
    method = (
        ('EMI', "EMI"),
        ('ONLINE', "Online"),
    )
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, null=False, default='0')
    coupon = models.ForeignKey(promocode,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True)
    total = models.DecimalField(max_digits=10,
                                default=0,
                                decimal_places=2,
                                verbose_name='INR ORDER TOTAL')
    emailAddress = models.EmailField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, null=True)
    order_id = models.CharField(max_length=100, null=True)

    def get_totals(self):
        total = 0

        for order_item in self.orderitems.all():
            total += float(order_item.get_total())

        if self.coupon:
            total -= self.coupon.amount

        return total


class Reviews(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='reviews')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='reviews')
    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)


class video(models.Model):
    """ Model videos des posts """
    title = models.CharField(max_length=100, null=False)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='videos')
    serial_number = models.IntegerField(null=False)
    video_id = models.CharField(max_length=100)
    is_preview = models.BooleanField(default=False)
    desc = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title


class offers(models.Model):
    off = models.CharField(max_length=100, verbose_name='Total Off')
    title = models.CharField(max_length=100, verbose_name='Title')
    subtitle = models.CharField(max_length=100, verbose_name='Sub Title')
    price = models.CharField(max_length=100, verbose_name='Price')
    desc = models.CharField(max_length=100, verbose_name='Description')
    button_text = models.CharField(max_length=100, verbose_name='Button Text')
    button_url = models.URLField(max_length=500,
                                 default='',
                                 verbose_name='Button Link')
    small_desc = models.CharField(max_length=100,
                                  verbose_name='Small Description')
    active = models.BooleanField(default=False, verbose_name="Status")

    def __str__(self):
        return self.title
