from rest_framework.views import APIView
from rest_framework.response import Response
from video_subtitle_extractor.settings import dynamo_db_table, aws_dynamodb_client
from boto3.dynamodb.conditions import Key
import traceback

class SearchVideoText(APIView):
    def post(self, request):
        try:
            video_id = request.data.get("video_id")
            search_string = request.data.get("search_string").lower()

            response = dynamo_db_table.query(
                KeyConditionExpression=Key('VideoID').eq(video_id)
            )

            # Filter the retrieved items by the input text
            filtered_items = [item for item in response['Items'] if search_string in item['Text'].lower()]

            # Return a success response
            return Response({'items': filtered_items})
        except:
            traceback.print_exc()
            return Response({'items': []}, status=400)