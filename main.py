
from flask import Flask, jsonify, make_response, request
from src.db_filter import DbFilter

app = Flask(__name__)

@app.route('/weibo/topdata', methods=['GET'])
def topdata():
    if request.method == 'GET':
        try:
            if 'by' in request.args:
                database_filter = DbFilter(request.args)
                rst = make_response(jsonify(database_filter.get_data()))
                del database_filter
            else:
                rst = make_response(DbFilter().set_error(4))
        except Exception as e:
            print(e)
            return rst, 400
        else:
            rst.headers['Access-Control-Allow-Origin'] = '*'    # 允许跨域访问
            return rst, 200


@app.route('/', methods=['GET'])
def index():
    header = {
        'Access-Control-Allow-Origin' : '*',
        'location': 'https://github.com/liyi3889/weibo_api'
    }
    if request.method == 'GET':
        rst = make_response()
        rst.headers = header
        return rst, 302


if __name__ == '__main__':
    app.debug = True
    app.run()


