import whisper
from openai import OpenAI
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from .models import PatientInfo, PatientRecord
from rest_framework.response import Response
from django.core.files.storage import default_storage
from .serializers import PatientInfoSerializer, PatientRecordSerializer



client = OpenAI( api_key = settings.OPENAI_API_KEY)


class RegisterPatientView(APIView):
    def post(self, request):
        serializer = PatientInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Patient registered successfully!",
                    "patient_id": serializer.data["patient_id"],
                },
                status=status.HTTP_201_CREATED,
            )
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetPatientDetailsView(APIView):
    def get(self, request):
        phone = request.query_params.get('patient_phone')
        try:
            patient = PatientInfo.objects.get(phone=phone)
            serializer = PatientInfoSerializer(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PatientInfo.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)


class StorePatientMedicalRecordsView(APIView):
    def post(self, request):
        serializer = PatientRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Medical record stored successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizePatientDataView(APIView):
    def post(self, request):

        unstructured_text = request.data.get('unstructured_text')
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Extract medical information from the following text."},
                    {"role": "user", "content": unstructured_text},
                ]
            )
            
            structured_data = response.choices[0].message.content
            return Response({'structured_data': structured_data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProcessAudioRecordsView(APIView):
    def post(self, request):
        
        patient_id = request.data.get('patient')
        audio_file = request.FILES.get('audio')

        if not audio_file:
            return Response({'error': 'Audio file is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        audio_path = default_storage.save(f'audio/temp_audio{patient_id}.m4a', audio_file)
        
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        
        transcribed_text = result['text']

        return Response({'transcribed_text': transcribed_text}, status=status.HTTP_200_OK)


class GetPatientRecordsView(APIView):
    def get(self, request):
        patient_id = request.query_params.get('patient')
        try:
            records = PatientRecord.objects.filter(patient_id=patient_id)
            serializer = PatientRecordSerializer(records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PatientRecord.DoesNotExist:
            return Response({'error': 'No records found for this patient'}, status=status.HTTP_404_NOT_FOUND)
