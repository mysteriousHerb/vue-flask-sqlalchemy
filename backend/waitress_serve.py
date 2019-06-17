from waitress import serve
# import app
import wsgi

serve(wsgi.app, host='0.0.0.0', port=5000)
# for production
# serve(wsgi.app, unix_socket='/path/to/unix.sock')

# command line:  waitress-serve --port=5000 wsgi:app
