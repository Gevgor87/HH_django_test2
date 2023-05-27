from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, AudioRecord
from .serializers import UserSerializer, AudioRecordSerializer

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_audio(request):
    user_id = request.data.get('user_id')
    token = request.data.get('token')
    wav_file = request.FILES.get('wav_file')

    try:
        user = User.objects.get(id=user_id, token=token)
    except User.DoesNotExist:
        return Response('Invalid user ID or token', status=status.HTTP_400_BAD_REQUEST)

    audio_record = AudioRecord(user=user, wav_file=wav_file)
    audio_record.save()

    download_url = f'http://localhost:8000/record?id={audio_record.uuid}&user={user.id}'
    return Response({'download_url': download_url}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def download_audio(request):
    audio_id = request.GET.get('id')
    user_id = request.GET.get('user')

    try:
        audio_record = AudioRecord.objects.get(uuid=audio_id, user_id=user_id)
    except AudioRecord.DoesNotExist:
        return Response('Audio record not found', status=status.HTTP_404_NOT_FOUND)

    return Response({'wav_file': audio_record.wav_file.url, 'mp3_file': audio_record.mp3_file.url})
