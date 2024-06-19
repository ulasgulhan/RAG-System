from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .serializer import UserSerializer

# Create your views here.


class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handle user registration.

        Parameters:
        request (Request): The request object containing user data.

        Returns:
        Response: A JSON response indicating success or failure of the registration.
        """

        username = request.data.get("username", None)
        user = User.objects.filter(username=username)
        if user.exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"Succsess": "User created succsessfully."},
                status=status.HTTP_201_CREATED,
            )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handle user login.

        Parameters:
        request (Request): The request object containing user credentials.

        Returns:
        Response: A JSON response indicating success or failure of the login attempt.
        """

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({"Succsessful": "Login success"}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle user logout.

        Parameters:
        request (Request): The request object.

        Returns:
        Response: A JSON response indicating the user has been logged out.
        """
        logout(request)
        return Response({"Logout": "Logout succsess"}, status=status.HTTP_200_OK)
