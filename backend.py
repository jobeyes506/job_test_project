from flask import Flask, request, jsonify
import psycopg2
import os
import numpy as np
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["https://job-test-project.vercel.app"]}})
 #CORS(app)  # 允许跨域请求


# 数据库连接信息（请修改为你的数据库配置）
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres.adeqlzjbkhxljhierjib',
    'password': 'TPeSe71FEdKKtJP3',
    'host': 'aws-0-ap-southeast-1.pooler.supabase.com',  # 使用 nslookup 找到的 IPv4 地址
    'port': '5432',
    'sslmode': 'require'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


# 评分权重配置
WEIGHTS = {
    "关键问题": 0.4,
    "倾向性问题": 0.3,
    "细化调整问题": 0.2,
    "二次确认问题": 0.1
}


# 计算匹配度
def calculate_match_score(user_answers):
    scores = []
    for category, weight in WEIGHTS.items():
        category_score = np.mean(user_answers.get(category, [0])) * weight
        scores.append(category_score)
    return sum(scores) * 100  # 最终得分百分制


@app.route('/submit_test', methods=['POST'])
def submit_test():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "无效的请求"}), 400

        user_id = data.get("user_id")
        key_score = data.get("key_score")
        tendency_score = data.get("tendency_score")
        detailed_score = data.get("detailed_score")
        confirm_score = data.get("confirm_score")

        if not user_id:
            return jsonify({"error": "缺少 user_id"}), 400

        # ✅ 确保数据库表结构正确
        conn = get_db_connection()
        cursor = conn.cursor()

        # **检查数据库表的字段是否正确**
        cursor.execute("""
            INSERT INTO test_results (user_id, key_score, tendency_score, detailed_score, confirm_score)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, key_score, tendency_score, detailed_score, confirm_score))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "测试提交成功"}), 200
    except Exception as e:
        print(f"❌ 服务器错误: {e}")
        return jsonify({"error": "服务器内部错误"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)), debug=True)