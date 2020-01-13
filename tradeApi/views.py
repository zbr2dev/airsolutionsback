from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, generics, status
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from datetime import date, datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# ...

# Add this view to your views.py file


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        username = User.objects.get(email=email.lower()).username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(
            data={
                "error": True,
                "message": "Неверный логин или пароль"
            },
            status=status.HTTP_200_OK
        )


class ChangePasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        oldPassword = request.data.get("oldPassword", "")
        newPassword = request.data.get("newPassword", "")
        username = User.objects.get(email=email.lower()).username
        user = authenticate(request, username=username, password=oldPassword)
        if user is not None:
            user.set_password(newPassword)
            user.save()
            return Response(
                data={
                    "status": 'ok'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data={
                "error": True,
                "message": "Пароль неверный"
            },
            status=status.HTTP_200_OK
        )


class RegisterUsersView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        phone = request.data.get("phone", "")
        if not username or not password or not email:
            return Response(
                data={
                    "error": True,
                    "message": "Заполните все поля"
                },
                status=status.HTTP_200_OK
            )
        try:
            new_user = User.objects.create_user(
                username=username, password=password, email=email
            )
        except IntegrityError:
            return Response(
                data={
                    "error": True,
                    "message": "Пользователь с таким логином или email уже существует"
                },
                status=status.HTTP_200_OK
            )

        new_profile = Profile.objects.create(user=User.objects.get(username=username), password=password, phone=phone)
        return Response(
            data={
                "username": username,
                "email": email
            },
            status=status.HTTP_201_CREATED
        )


class ProfileCreateView(generics.CreateAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()


class ProfileRudView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Profile.objects.all()


class ProfileGetByUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    lookup_field = 'user'

    def get_queryset(self):
        return Profile.objects.all()


class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class PackageCreateView(generics.CreateAPIView):
    serializer_class = PackageSerializer

    def get_queryset(self):
        return Package.objects.all()


class PackageRudView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PackageSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Package.objects.all()


class PackageListView(generics.ListAPIView):
    serializer_class = PackageSerializer

    def get_queryset(self):
        return Package.objects.all()


class TransactionCreateView(generics.CreateAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all()


class TransactionRudView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Transaction.objects.all()


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all()


class GetUserByTokenView(APIView):

    def post(self, request):
        data = {'token': request.data['token']}
        try:
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = {
                'id': valid_data['user'].id,
                'username': valid_data['user'].username,
                'email': valid_data['user'].email
            }
        except ValidationError:
            return Response(
                data={
                    "error": True,
                    "message": "Пользователь не найден"
                },
                status=status.HTTP_200_OK
            )
        return Response({'user': user})


# class GetProfileByUser(APIView):
#
#     def post(self, request):
#         user = request.data.get("user", "")
#         try:
#             profile_id
#         except ValidationError:
#             return Response(
#                 data={
#                     "error_code": 1,
#                     "message": "Пользователь не найден"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         return Response({'user': user})


class RobotBuyView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    queryset = Package.objects.all()

    def post(self, request, *args, **kwargs):
        name = request.data.get("name", "")
        robot_type = request.data.get("type", "")
        control = request.data.get("control", "")
        user = request.data.get("user", "")
        cost = request.data.get("cost", "")
        daily_profit = request.data.get("dailyProfit", "")
        robot_term = request.data.get("robotTerm", "")
        end_date = date.today() + timedelta(days=int(robot_term))
        if not cost or not daily_profit or not robot_term or not robot_type or not name or not user:
            return Response(
                data={
                    "error": True,
                    "message": "Заполните все поля"
                },
                status=status.HTTP_200_OK
            )

        try:
            find_profile = Profile.objects.get(user=user)
            if find_profile.money < cost:
                return Response(
                    data={
                        "error": True,
                        "message": "Недостаточно средств на счету"
                    },
                    status=status.HTTP_200_OK
                )
            find_profile.money -= cost
            find_profile.save()
        except ObjectDoesNotExist:
            return Response(
                data={
                    "error": True,
                    "message": "Пользователь не найден"
                },
                status=status.HTTP_200_OK
            )

        try:
            new_package = Package.objects.create(
                    name=name,
                    status=1,
                    type=robot_type,
                    control=int(control),
                    user=User.objects.get(pk=user),
                    capital=cost,
                    dailyProfit=daily_profit,
                    endDate=end_date
                )
            new_transaction = Transaction.objects.create(
                amount=cost,
                sender=str(user),
                paymentSystem='AirSolutions',
                status='Обработано',
                recipient=name
            )
        except IntegrityError:
            print(IntegrityError)
            return Response(
                data={
                    "error": True,
                    "message": "Ошибка при создании пакета"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            data={
                'id': new_transaction.id,
                'name': name,
                'status': 1,
                'type': robot_type,
                'control': control,
                'user': user,
                'capital': cost,
                'dailyProfit': daily_profit,
                'startDate': datetime.now() + timedelta(hours=2),
                'endDate': end_date,
                'transactionId': new_transaction.id
            })


class RobotFinishedView(APIView):

    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        sender = request.data.get("sender", "")
        user = request.data.get("user", "")
        capital = request.data.get("capital", "")
        daily_profit = request.data.get("dailyProfit", "")
        term = request.data.get("term", "")
        amount = (capital * daily_profit * float(term+1) / 100) + capital
        print(str(capital) + ' ' + str(amount))
        if not user or not capital:
            return Response(
                data={
                    "error": True,
                    "message": "Заполните все поля"
                },
                status=status.HTTP_200_OK
            )
        try:
            new_transaction = Transaction.objects.create(
                amount=amount,
                sender=sender,
                status='Обработано',
                paymentSystem='AirSolutions',
                recipient=str(user)
            )
            recipient_profile = Profile.objects.get(user=User.objects.get(pk=user))
            recipient_profile.money += amount
            recipient_profile.save()
        except ValueError:
            return Response(
                data={
                    "error": True,
                    "message": "Ошибка"
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data={
                "status": "ok",
            },
            status=status.HTTP_201_CREATED
        )


class SendEmailView(APIView):

    def post(self, request):
        message = request.data['message']
        # try:
        #
        # except ValidationError:
        #     return Response(
        #         data={
        #             "error_code": 1,
        #             "message": "Пользователь не найден"
        #         },
        #         status=status.HTTP_404_NOT_FOUND
        #     )
        send_mail(
            'AirSolutions',
            message,
            'support@airsolutions.com',
            ['support@airsolutions.com'],
            fail_silently=True,
        )
        return Response({'sent': True})
