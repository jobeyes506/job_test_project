from flask import Flask, request, jsonify
import pymysql
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库连接信息（请修改为你的数据库配置）
DB_CONFIG = {
    "host": "your-database-host",
    "user": "your-username",
    "password": "your-password",
    "database": "job_test_db",
    "charset": "utf8mb4"
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

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

@app.route("/submit_test", methods=["POST"])
def submit_test():
    data = request.json
    user_id = data.get("user_id")
    answers = data.get("answers")  # 用户回答的测评数据
    
    match_score = calculate_match_score(answers)
    
    # 存入数据库
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO test_results (user_id, match_score) VALUES (%s, %s)"
    cursor.execute(sql, (user_id, match_score))
    conn.commit()
    conn.close()
    
    return jsonify({"user_id": user_id, "match_score": match_score})

@app.route("/get_results", methods=["GET"])
def get_results():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_results")
    results = cursor.fetchall()
    conn.close()
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
