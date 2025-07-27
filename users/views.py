from django.shortcuts import render
import csv
import io

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from .models import User


class CSVUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")

        # Validate file presence
        if not file:
            return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate .csv extension
        if not file.name.endswith(".csv"):
            return Response({"error": "Only CSV files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        # Decode and parse CSV
        try:
            decoded_file = file.read().decode("utf-8")
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
        except Exception as e:
            return Response({"error": "Failed to read CSV file."}, status=status.HTTP_400_BAD_REQUEST)

        saved_count = 0
        rejected_count = 0
        errors = []

        for idx, row in enumerate(reader, start=1):
            serializer = UserSerializer(data=row)

            if serializer.is_valid():
                email = serializer.validated_data['email']
                # Check for duplicate email
                if not User.objects.filter(email=email).exists():
                    serializer.save()
                    saved_count += 1
                else:
                    rejected_count += 1
                    errors.append({
                        "row": idx,
                        "errors": {"email": ["Duplicate email."]}
                    })
            else:
                rejected_count += 1
                errors.append({
                    "row": idx,
                    "errors": serializer.errors
                })

        return Response({
            "saved_records": saved_count,
            "rejected_records": rejected_count,
            "validation_errors": errors
        }, status=status.HTTP_200_OK)
