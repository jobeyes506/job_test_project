from flask import Flask, request, jsonify
import psycopg2
import os
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求



DB_CONFIG = {
    'dbname': 'postgres',  # 默认数据库名称
    'user': 'postgres',  # 默认用户
    'password': '9I6X5qJFXWHbgm6Q',  
    'host': 'pool.supabase.co',  # Supabase 服务器地址
    'port': '5432',
    'sslmode': 'require'  # 关键！Supabase 可能要求 SSL 加密
}

def get_db_connection():
    try:
        print("🔍 连接 Supabase 数据库中...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ 数据库连接成功！")
        return conn
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return None

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)


