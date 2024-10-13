from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .utils import scrape_postcode_data
from .serializers import AddressSerializer

@api_view(['GET'])
def scrape_postcode(request):
    # Get postcode from query params
    postcode = request.query_params.get('postcode', None)
    
    if not postcode:
        return Response({'error': 'No postcode provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Scrape the data
        data = scrape_postcode_data(postcode)

        # Serialize the data
        serializer = AddressSerializer(data=data, many=True)
        serializer.is_valid()

        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
