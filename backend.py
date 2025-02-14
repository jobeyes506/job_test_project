rom flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 默认主页，防止 404 错误
@app.route('/')
def home():
    return jsonify({"message": "Flask 服务器正常运行！"})

# 测试数据库连接 API
@app.route('/get_results', methods=['GET'])
def get_results():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "数据库连接失败"}), 500

        cur = conn.cursor()
        cur.execute("SELECT NOW();")  # 测试数据库是否可用
        result = cur.fetchone()
        conn.close()

        return jsonify({"message": "数据库连接成功", "timestamp": result[0]})
    
    except Exception as e:
        print(f"❌ API 执行失败: {e}")
        return jsonify({"error": str(e)}), 500