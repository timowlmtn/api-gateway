import json
import traceback
import api_layer


def parse_filename(event, context):
    """
    A function to parse the incoming file name and return a JSON object.
    :param event:
    :param context:
    :return:
    """
    try:
        file_full_path = None

        # Handle data directly from API Gateway
        if "queryStringParameters" in event:
            if "Path" in event["queryStringParameters"] and event["queryStringParameters"]["Path"] is not None:
                file_full_path = event["queryStringParameters"]["Path"]
        # Handle data from the Lambda test interface on the console
        else:
            file_full_path = event["Path"]

        if file_full_path:
            result = api_layer.parse_regexp(r"(.*)/([A-Za-z]+)_([\w_]+)_([\d]{8})([\d]{4})([\w]+)\.([\w]+)$",
                                            file_full_path,
                                            ("directory",
                                             "company",
                                             "application",
                                             "date",
                                             "time",
                                             "activity",
                                             "file_type"))
        else:
            result = f"USAGE: FILE_PATH is a required field."

    except Exception as exc:
        result = report_error(exc)

    return respond(None, result)


def report_error(exception):
    """
    Simple error report function

    :param exception:
    :return:
    """
    message = f"ERROR: {exception} {traceback.format_exc()}"
    error = {
        "isError": True,
        "type": "Unhandled Exception",
        "message": message
    }
    return error


def respond(err, res=None):
    """
    Create an HTML response

    :param err:
    :param res:
    :return:
    """
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
