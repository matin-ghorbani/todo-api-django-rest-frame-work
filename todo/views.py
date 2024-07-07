from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Todo
from .serializers import TodoSerializer, UserSerializer

User = get_user_model()


# Create your views here.

# region function base view
@api_view(['GET', 'POST'])
def all_todos(request: Request) -> Response:
    if request.method == 'GET':
        todos = Todo.objects.order_by('priority').all()
        serializer = TodoSerializer(todos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(None, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request: Request, todo_id: int) -> Response:
    try:
        todo: Todo = Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todo, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        todo.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    return Response(None, status=status.HTTP_400_BAD_REQUEST)


# endregion

# region class base view

class TodosListApiView(APIView):
    def get(self, request: Request) -> Response:
        todos: Todo = Todo.objects.order_by('priority').all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)


class TodosDetailApiView(APIView):
    @staticmethod
    def get_todo(todo_id: int) -> Todo | Response:
        try:
            return Todo.objects.get(pk=todo_id)
        except Todo.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, todo_id: int) -> Response:
        serializer = TodoSerializer(TodosDetailApiView.get_todo(todo_id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, todo_id: int) -> Response:
        todo = TodosDetailApiView.get_todo(todo_id)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, todo_id: int) -> Response:
        TodosDetailApiView.get_todo(todo_id).delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


# endregion

# region mixins

class TodosListMixinApiView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

    def get(self, request: Request) -> Response:
        return self.list(request)

    def post(self, request: Request) -> Response:
        return self.create(request)


class TodosDetailMixinApiView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                              generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

    def get(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)

    def put(self, request: Request, pk: int) -> Response:
        return self.update(request, pk)

    def delete(self, request: Request, pk: int) -> Response:
        return self.destroy(request, pk)


# endregion

# region generics

class TodosListGenericApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class TodosDetailGenericApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer


# endregion

# region viewsets

class TodosViewSetApiView(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = LimitOffsetPagination


# endregion

# region users

class UserGenericApiViewPagination(PageNumberPagination):
    page_size = 1


class UsersGenericApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class = PageNumberPagination
    pagination_class = UserGenericApiViewPagination

# endregion
