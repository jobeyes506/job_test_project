from flask import Flask, request, jsonify
import psycopg2
import os
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/health', methods=['GET'])
def health_check():
    return "✅ Flask 服务器运行正常！"

@app.route('/get_results', methods=['GET'])
def get_results():
    return jsonify({"message": "测试 API 正常运行"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


# 数据库连接信息（请修改为你的数据库配置）
DB_CONFIG = {
    "host": "db.adeqlzjbkhxljhierjib.supabase.co",  # 从 Supabase 复制
    "port": "5432",  # PostgreSQL 默认端口
    "database": "postgres",  # Supabase 默认数据库名
    "user": "postgres",  # 默认用户
    "password": "huijie506"  # 你创建数据库时设置的密码
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
    data = request.get_json()
    user_id = data.get("user_id")
    match_score = data.get("match_score")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO test_results (user_id, match_score) VALUES (%s, %s)",
        (user_id, match_score)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "数据提交成功", "user_id": user_id, "match_score": match_score})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)), debug=True)


@app.route('/get_results', methods=['GET'])
def get_results():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_results")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
