from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, OR ,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from  django.shortcuts import  get_object_or_404
from rest_framework import status
from .serializers import RegisterUserSerializer ,LoginUserSerializer ,CustomUserSerializer
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.db.models import Q  # Import Q for filtering
from rest_framework.pagination import PageNumberPagination

# Create your views here.
User = get_user_model()


# Custom Pagination Class
# Custom Pagination Class
class CustomPagination(PageNumberPagination):
    page_size = 10  # Default items per page
    page_size_query_param = "limit"
    max_page_size = 100  # Limit max items per page

    def get_paginated_response(self, data):
        total = self.page.paginator.count
        limit = self.get_page_size(self.request)
        totalPages = self.page.paginator.num_pages
        page = self.page.number

        meta = {
            "total": total,
            "limit": limit,
            "page": page,
            "totalPages": totalPages,
        }

        return Response({
            "meta": meta,
            "data": data
        })


class UserInfoView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        # Restrict queryset to only the authenticated user
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        # Return the authenticated user instance directly
        return self.request.user
    
class UserRegistrationView(CreateAPIView):
    permission_classes = [AllowAny]  # Override IsAuthenticated
    serializer_class = RegisterUserSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]  # Override IsAuthenticated
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            response = Response({
                "user": CustomUserSerializer(user).data},
                                status=status.HTTP_200_OK)
            
            response.set_cookie(key="access_token", 
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="None")
            
            response.set_cookie(key="refresh_token",
                                value=str(refresh),
                                httponly=True,
                                secure=True,
                                samesite="None")
            return response
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class UserView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination()

    def get(self, request):
        query = request.GET.get("query", None)
        users = CustomUser.objects.all()

        if query:
            users = users.filter(Q(email__icontains=query) | Q(username__icontains=query))

        # Apply Pagination
        paginator = self.pagination_class
        paginated_users = paginator.paginate_queryset(users, request)
        
        serializer = CustomUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)