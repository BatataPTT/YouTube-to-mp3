from main import app

def handler(request):
    from io import BytesIO
    from gunicorn.http.wsgi import WSGIHandler

    wsgi_handler = WSGIHandler()
    environ = {
        'REQUEST_METHOD': request.method,
        'PATH_INFO': request.path,
        'QUERY_STRING': request.query_string,
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '80',
        'wsgi.input': BytesIO(request.body),
    }
    response = wsgi_handler.run(app, environ)

    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.body.decode('utf-8')
    }