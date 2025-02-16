import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 🔥 确保数据库连接代码在 backend.py 里！


DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '9I6X5qJFXWHbgm6Q',
    'host': '169.254.20.10',  # 使用 nslookup 找到的 IPv4 地址
    'port': '5432',
    'sslmode': 'require'
}

def get_db_connection():
    """ 连接 Supabase 数据库 """
    try:
        print("🔍 连接 Supabase 数据库中...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ 数据库连接成功！")
        return conn
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return None

# 默认主页
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
        cur.execute("SELECT NOW();")  # 仅测试数据库是否可用
        result = cur.fetchone()
        conn.close()

        return jsonify({"message": "数据库连接成功", "timestamp": result[0]})
    
    except Exception as e:
        print(f"❌ API 执行失败: {e}")
        return jsonify({"error": str(e)}), 500

flask run --host=0.0.0.0 --port=10000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)