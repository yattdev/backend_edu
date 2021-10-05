from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as loginUser, update_session_auth_hash
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.urls import reverse
import json
from time import time
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def home(request):
    return render(request, 'index.html', {})

def add_post(request):
    posts= PostForm()
    if request.method=='POST':
        posts=PostForm(request.POST, request.FILES)
        if posts.is_valid():
            posts.save()
        messages.success(request, "Posts Added Sucessfully !!")    
        return redirect('allposts')
    return render(request, "webadmin/addpost.html", {'post':posts})

def add_cat(request):
    category= CatForm()
    if request.method=='POST':
        category=CatForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addcat.html", {'category':category})

def add_course(request):
    course= Maincourse()
    if request.method=='POST':
        course=Maincourse(request.POST, request.FILES)
        if course.is_valid():
            course.save()
        messages.success(request, "Course Added Sucessfully !!")    
        return redirect('allcourses')
    return render(request, "webadmin/addcourse.html", {'course':course})

def webadmin(request):
    postcount = Post.objects.all().count()
    catcount = Category.objects.all().count()
    usercount = User.objects.all().count()
    orders = Order.objects.all()
    context = {'postcount':postcount, 'cat':catcount, 'user':usercount,"orders":orders}
    return render(request, 'webadmin/index.html', context)  

def add_curriculam(request):
    category= CatForm()
    if request.method=='POST':
        category=CatForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('webadmin')
    return render(request, "webadmin/addcat.html", {'category':category})

#This is for show all Posts in Custom Admin Panel
def allposts(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'webadmin/allposts.html', context)

#This is for show all Users in Custom Admin Panel
def allusers(request):
    # users = User.objects.all()
    customer = Customer.objects.all()
    context = {
        # 'users':users
    'customer':customer
    }
    return render(request, 'webadmin/allusers.html', context)

def userdetails(request, id):
    customer = Customer.objects.filter(id=id).first()
    context = {'customer':customer}
    return render(request, 'webadmin/user_detail.html', context)

def allorders(request):
    orders = Order.objects.filter(ordered=True)
    carts = Cart.objects.all()
    context = {
    'orders':orders, 'carts':carts,
    }
    return render(request, 'webadmin/allorders.html', context)

def approve_certificates(request, id):
    if request.method == 'POST':
        carts = Cart.objects.get(id=id)
        approve_cert= approve_certForm(request.POST or None, request.FILES or None, instance=carts)
        if approve_cert.is_valid():
            approve_cert.save()
        messages.success(request, "Certificate Is Enable !!")
        return redirect('allorders')
    else:
        carts = Cart.objects.get(id=id)
        approve_cert= approve_certForm(instance=carts)

    return render(request, "webadmin/editcarts.html", {'editcarts':approve_cert})
    
#This is for show all Categories in Custom Admin Panel
def allcat(request):
    cat = Category.objects.filter(parent=None).order_by('hit')
    context = {'cat':cat}
    return render(request, 'webadmin/allcat.html', context)

def allcourse(request):
    course = MainCourse.objects.all()
    context = {'course':course}
    return render(request, 'webadmin/allcourse.html', context)

def edit_post(request, id):
    if request.method == 'POST':
        posts = Post.objects.get(id=id)
        editpostForm= EditPostForm(request.POST or None, request.FILES or None, instance=posts)
        if editpostForm.is_valid():
            editpostForm.save()
        messages.success(request, "Post Update Sucessfully !!")
        return redirect('allposts')
    else:
        posts = Post.objects.get(id=id)
        editpostForm= EditPostForm(instance=posts)

    return render(request, "webadmin/editposts.html", {'editpost':editpostForm})
    
def delete_post(request, id):
    delete = Post.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Post Deleted Successfully.")
    return redirect('allposts')


#For edit the categories
def edit_cat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= CatForm(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= CatForm(instance=cat)

    return render(request, "webadmin/editcat.html", {'editcat':editcatForm})

#For delete the categories    
def delete_cat(request, id):
    delete = Category.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Category Deleted Successfully.")
    return redirect('allcat')


#For edit the course
def edit_course(request, id):
    if request.method == 'POST':
        course = MainCourse.objects.get(id=id)
        editcourse= EditMaincourse(request.POST or None, request.FILES or None, instance=course)
        if editcourse.is_valid():
            editcourse.save()
        messages.success(request, "Course Update Sucessfully !!")
        return redirect('allcat')
    else:
        cat = MainCourse.objects.get(id=id)
        editcourse= EditMaincourse(instance=cat)

    return render(request, "webadmin/editcourse.html", {'editcourse':editcourse})

#For delete the course
def delete_course(request, id):
    delete = MainCourse.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "MainCourse Deleted Successfully.")
    return redirect('allcourses')    

def add_videos(request):
    video= videoform()
    if request.method=='POST':
        video=videoform(request.POST, request.FILES)
        if video.is_valid():
            video.save()
        messages.success(request, "video Added Sucessfully !!")    
        return redirect('home')
    return render(request, "webadmin/addvideo.html", {'video':video})

def edit_videos(request, id):
    if request.method == 'POST':
        vid = video.objects.get(id=id)
        editvideoForm= videoform(request.POST or None, request.FILES or None, instance=vid)
        if editvideoForm.is_valid():
            editvideoForm.save()
        messages.success(request, "Video Update Sucessfully !!")
        return redirect('allcat')
    else:
        vid = video.objects.get(id=id)
        editvideoForm= videoform(instance=vid)

    return render(request, "webadmin/editvideo.html", {'editvideo':editvideoForm})

def allvideos(request):
    vid = video.objects.all()
    context = {'video':vid}
    return render(request, 'webadmin/allvideo.html', context)

def delete_video(request, id):
    delete = video.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "video Deleted Successfully.")
    return redirect('allcourses')   

def paid_video(request, slug):
    allpost = get_object_or_404(Post, slug=slug)
    vid = video.objects.filter(post=allpost)
    context = {'allpost':allpost, 'vid':vid}
    return render(request, 'users/video.html', context)

def allfaq(request):
    f = faq.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allfaq.html', context)

def add_faq(request):
    faq= faqForm()
    if request.method=='POST':
        faq= faqForm(request.POST, request.FILES)
        if faq.is_valid():
            faq.save()
        messages.success(request, "faq Added Sucessfully !!")    
        return redirect('allfaq')
    return render(request, "webadmin/add_faq.html", {'faq':faq})

def edit_faq(request, id):
    if request.method == 'POST':
        faqs = faq.objects.get(id=id)
        EditfaqForm= faqForm(request.POST, instance=faqs)
        if EditfaqForm.is_valid():
            EditfaqForm.save()
        messages.success(request, "FAQ Update Sucessfully !!")
        return redirect('allfaq')
    else:
        faqs = faq.objects.get(id=id)
        EditfaqForm= faqForm(instance=faqs)   

    return render(request, "webadmin/editfaq.html", {'faqForm':EditfaqForm})

def delete_faq(request, id):
    delete = faq.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "faq Deleted Successfully.")
    return redirect('allfaq') 

def alltime(request):
    f = timing.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/alltime.html', context)

def add_time(request):
    time= timingform()
    if request.method=='POST':
        time= timingform(request.POST, request.FILES)
        if time.is_valid():
            time.save()
        messages.success(request, "Timings Added Sucessfully !!")    
        return redirect('alltime')
    return render(request, "webadmin/add_time.html", {'time':time})

def edit_time(request, id):
    if request.method == 'POST':
        time = timing.objects.get(id=id)
        Edittimingform= timingform(request.POST, instance=time)
        if Edittimingform.is_valid():
            Edittimingform.save()
        messages.success(request, "Timings Update Sucessfully !!")
        return redirect('alltime')
    else:
        time = timing.objects.get(id=id)
        Edittimingform= timingform(instance=time)   

    return render(request, "webadmin/edit_time.html", {'time':Edittimingform})

def delete_time(request, id):
    delete = timing.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Timing Deleted Successfully.")
    return redirect('alltime') 

def allfeatures(request):
    f = features.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allfeatures.html', context)

def add_features(request):
    features= featuresform()
    if request.method=='POST':
        features= featuresform(request.POST, request.FILES)
        if features.is_valid():
            features.save()
        messages.success(request, "Timings Added Sucessfully !!")    
        return redirect('allfeatures')
    return render(request, "webadmin/add_features.html", {'features':features})

def edit_features(request, id):
    if request.method == 'POST':
        feat = features.objects.get(id=id)
        editfeatures = featuresform(request.POST, instance=feat)
        if editfeatures .is_valid():
            editfeatures .save()
        messages.success(request, "featuress Update Sucessfully !!")
        return redirect('allfeatures')
    else:
        feat = features.objects.get(id=id)
        editfeatures = featuresform(instance=feat)   

    return render(request, "webadmin/edit_features.html", {'features':editfeatures })

def delete_features(request, id):
    delete = features.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Features Deleted Successfully.")
    return redirect('allfeatures') 

def allcurriculam(request):
    f = Curriculam.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allcurriculam.html', context)

def add_curriculam(request):
    curr= Curriculamform()
    if request.method=='POST':
        curr= Curriculamform(request.POST, request.FILES)
        if curr.is_valid():
            curr.save()
        messages.success(request, "Curriculam Added Sucessfully !!")    
        return redirect('allcurriculam')
    return render(request, "webadmin/add_curr.html", {'curr':curr})

def edit_curriculam(request, id):
    if request.method == 'POST':
        curr = Curriculam.objects.get(id=id)
        editcurr = Curriculamform(request.POST, instance=curr)
        if editcurr.is_valid():
            editcurr.save()
        messages.success(request, "Curriculam Update Sucessfully !!")
        return redirect('allcurriculam')
    else:
        curr = Curriculam.objects.get(id=id)
        editcurr = Curriculamform(instance=curr)   

    return render(request, "webadmin/edit_curriculam.html", {'editcurr':editcurr })

def delete_curriculam(request, id):
    delete = Curriculam.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Curriculam Deleted Successfully.")
    return redirect('allcurriculam') 

def allsubcatg(request):
    f = subcat.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allsubcat.html', context)

def add_subcatg(request):
    sub= subcatg()
    if request.method=='POST':
        sub= subcatg(request.POST, request.FILES)
        if sub.is_valid():
            sub.save()
        messages.success(request, "Subcat Added Sucessfully !!")    
        return redirect('allsubcatg')
    return render(request, "webadmin/add_subcat.html", {'sub':sub})

def edit_subcatg(request, id):
    if request.method == 'POST':
        sub = subcat.objects.get(id=id)
        editsub = subcatg(request.POST, instance=sub)
        if editsub.is_valid():
            editsub.save()
        messages.success(request, "Subcat Update Sucessfully !!")
        return redirect('allsubcatg')
    else:
        sub = subcat.objects.get(id=id)
        editsub = subcatg(instance=sub)   

    return render(request, "webadmin/edit_subcat.html", {'subcat':editsub })

def delete_subcatg(request, id):
    delete = subcat.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Subcat Deleted Successfully.")
    return redirect('allsubcatg') 

def add_leftcat(request):
    category= leftmenu()
    if request.method=='POST':
        category=leftmenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addleftcat.html", {'category':category})

def add_middlecat(request):
    category= middlemenu()
    if request.method=='POST':
        category=middlemenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addmiddlecat.html", {'category':category})

def add_rightcat(request):
    category= rightmenu()
    if request.method=='POST':
        category=rightmenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addrightcat.html", {'category':category})

def admin_reviews(request):
    review= admin_reviewsform()
    if request.method=='POST':
        review = admin_reviewsform(request.POST, request.FILES)
        if review.is_valid():
            review.save()
        messages.success(request, "Review Added Sucessfully !!")    
        return redirect('alladmin_review')
    return render(request, "webadmin/add_reviews.html", {'review':review})

def delete_admin_review(request, id):
    delete = Reviews.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Admin Review Deleted Successfully.")
    return redirect('alladmin_review')   

def edit_admin_review(request, id):
    if request.method == 'POST':
        review = Reviews.objects.get(id=id)
        edit_admin_reviews = admin_reviewsform(request.POST, instance=review)
        if edit_admin_reviews .is_valid():
            edit_admin_reviews .save()
        messages.success(request, "Reviews Update Sucessfully !!")
        return redirect('alladmin_review')
    else:
        faqs = Reviews.objects.get(id=id)
        edit_admin_reviews = admin_reviewsform(instance=faqs)

    return render(request, "webadmin/edit_admin_reviews.html", {'edit':edit_admin_reviews })    

def alladmin_review(request):
    review = Reviews.objects.all()
    context = {'review':review}
    return render(request, 'webadmin/all_reviews.html', context)    

def allribbon(request):
    ribbon = offers.objects.all()
    context = {'ribbon':ribbon}
    return render(request, 'webadmin/allribbon.html', context)

def add_ribbon(request):
    ribbon= ribbonform()
    if request.method=='POST':
        ribbon = ribbonform(request.POST, request.FILES)
        if ribbon.is_valid():
            ribbon.save()
        messages.success(request, "Offers Added Sucessfully !!")    
        return redirect('allribbon')
    return render(request, "webadmin/add_ribbon.html", {'add':ribbon})

def delete_ribbon(request, id):
    delete = offers.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Offer Deleted Successfully.")
    return redirect('allribbon')   

def edit_ribbon(request, id):
    if request.method == 'POST':
        ribbon = offers.objects.get(id=id)
        ribbon = ribbonform(request.POST, instance=ribbon)
        if ribbon.is_valid():
            ribbon.save()
        messages.success(request, "Offer Update Sucessfully !!")
        return redirect('allribbon')
    else:
        ribbon = offers.objects.get(id=id)
        ribbon = ribbonform(instance=ribbon)

    return render(request, "webadmin/edit_ribbon.html", {'edit':ribbon })    
    
