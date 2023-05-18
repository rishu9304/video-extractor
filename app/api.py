from rest_framework.views import APIView
from rest_framework.response import Response
from video_subtitle_extractor.settings import dynamo_db_table, aws_dynamodb_client
from boto3.dynamodb.conditions import Key
import traceback

class SearchVideoText(APIView):
    def post(self, request):
        try:
            print("test")
            video_id = request.data.get("video_id")
            search_string = request.data.get("search_string")
            print("v", video_id, search_string)

            # Retrieve the items matching the VideoID
            # response = aws_dynamodb_client.query(
            #     aws_dynamodb_client='Subtitles',
            #     KeyConditionExpression=key_condition_expression,
            #     ExpressionAttributeValues=expression_attribute_values
            # )
            response = dynamo_db_table.query(
                KeyConditionExpression=Key('VideoID').eq(video_id)
            )

            # Filter the retrieved items by the input text
            filtered_items = [item for item in response['Items'] if search_string in item['Text']]

            # Return a success response
            return Response({'items': filtered_items})
        except:
            traceback.print_exc()
            return Response({'items': []}, status=400)