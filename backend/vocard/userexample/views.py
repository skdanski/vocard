import pyrebase
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

# firebase initialization 
firebase = pyrebase.initialize_app(getattr(settings, "FIREBASE_CONFIG"))
authen = firebase.auth()
db = firebase.database()

# @extend_schema(
#     methods='POST',
#     request=inline_serializer(
#         name='requestSerializer',
#         fields={
#             'sentence': serializers.CharField()
#         }
#     ),
#     description="Add the provided sentence to the user's user_example entry",
#     responses={
#         201: 
#     }
# )

@api_view(['GET', 'POST'])
def user_example_list(request, usr_id):
    # Authentication
    if not hasattr(request.user, 'usr_id'):
        return Response({'error': 'anonuser cannot access user_example'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        request_usr_id = str(request.user.usr_id)
    if request_usr_id != usr_id:
        return Response({'error': request_usr_id}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        is_user = db.child('users').child(usr_id).get().val()
        usr_ex = db.child('user_example').child(usr_id).get().val()
        # User with usr_id does not exist
        if is_user is None:
            return Response({'usr_id': usr_id, 'error': 'no such user in database'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # User with usr_id exists, but no associated information in user_example
        elif is_user is not None and usr_ex is None:
            return Response({'usr_id': usr_id, 'error': 'user has no entries in user_example!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: 
            return Response(usr_ex, status=status.HTTP_200_OK)
     
    elif request.method == 'POST':
        try:
            word_name = list(request.data)
            data = {
                'sentence': request.data[word_name[0]]['sentence']
            }
            db.child('user_example').child(usr_id).child(word_name[0]).set(data)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error': 'Failed to POST!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
def user_example_detail(request, word, usr_id):
    # Authentication
    if not hasattr(request.user, 'usr_id'):
        return Response({'error': 'anonuser cannot access user_example'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        request_usr_id = str(request.user.usr_id)
    if request_usr_id != usr_id:
        return Response({'error': request_usr_id}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == "GET":
        usr_ex_entry = db.child('user_example').child(usr_id).child(word).get().val()
        # User with entry does not exist
        if usr_ex_entry is None:
            return Response({'error': f'user has no entry ({word}) in user_example!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: 
            return Response(usr_ex_entry, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        try:
            data = {
                'sentence': request.data['sentence']
            }
            print(data)
            db.child('user_example').child(usr_id).child(word).update(data)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'unable to update'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == "DELETE":
        try:
            db.child('user_example').child(usr_id).child(word).remove()
            return Response({'entry': f'"{word}"s example removed'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
