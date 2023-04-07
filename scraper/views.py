from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from . import scraper
from .models import Data, Claps, Fav
from django.http import JsonResponse
from .serializer import UserSerializer, DataSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    print("triggered the class")
    # given by murshid:

    def create(self, request):
        print("triggered the create")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            return Response({'status': 'success'})
        else:
            return Response(serializer.errors, status=400)



def index(request):
    return render(request=request, template_name='index.html')


class FavPost(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        user = request.user
        userModel = User.objects.get(email=user)
        post = Data.objects.get(id=id)
        FavItem = Fav.objects.filter(user=user, data=post)
        if not FavItem:
            print(FavItem)
            a = FavItem.create(user=user, data=post)
            userModel.favourite_posts.add(id)
            action = 1
        else:
            a = FavItem.filter(user=user, data=post).delete()
            userModel.favourite_posts.remove(id)
            action = 0
        return JsonResponse({"action": action})







class ClapPost(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        user = request.user
        post = Data.objects.get(id=id)
        current_claps = post.Claps
        Liked = Claps.objects.filter(user=user, data=post)
        if not Liked:
            liked = Claps.objects.create(user=user, data=post)
            current_claps += 1
            action = 1
        else:
            liked = Claps.objects.filter(user=user, data=post).delete()
            current_claps -= 1
            action = 0
        post.Claps = current_claps
        post.save()
        return JsonResponse({"claps": current_claps, "action": action})



def test(request):
    # currentUser = User.objects.get(email=request.user)
    # data1 = Data.objects.get(id=6)
    # print(data1)
    # currentUser.liked_posts.add(data1)
    # print(currentUser.liked_posts.all())
    user = User.objects.get(email=request.user)
    posts = user.liked_posts.all()
    posts = DataSerializer(posts, many=True)
    return JsonResponse({"res":posts.data})

class GetData(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, keyword):
        # I want to search in all data titles that may be similar to my title
        data = Data.objects.filter(Title__icontains=keyword)
        serializer = DataSerializer(data, many=True)
        # data = Data.objects.order_by("id")[10:].values()
        return JsonResponse({"Your data":(serializer.data)})




def start_scrape(request):
    print("reached at least here")
    if request.method == 'POST' and 'run_script' in request.POST:
        link = request.POST.get('link')
        if len(link) : 
            scraper.main_scraper(link)
    context = {'Data':Data.objects.all(),'link':link, 'status':'Done'}
    # return render(request=request, template_name='index.html', context={'link':link, 'status':'finished'})
    return render(request=request, template_name='index.html', context=context)



class DataView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        # Return the data for authenticated users only
        data = Data.objects.order_by('-id')[:10].values()
        return JsonResponse({"data": list(data)})