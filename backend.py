from flask import Flask, request, jsonify
import psycopg2
import os
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求


DB_CONFIG = {
    'dbname': 'postgres',  # Supabase 默认数据库名称
    'user': 'postgres',  # Supabase 默认用户
    'password': '9I6X5qJFXWHbgm6Q',  
    'host': 'db.adeqlzjbkhxljhierjib.supabase.co',  # 你的 Supabase DB Host
    'port': '5432'
}

def get_db_connection():
    try:
        print("🔍 正在连接 Supabase 数据库...")
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='9I6X5qJFXWHbgm6Q',
            host='db.adeqlzjbkhxljhierjib.supabase.co',
            port='5432',
            sslmode='require'  # 🔥 关键：强制使用 SSL 连接
        )
        print("✅ 数据库连接成功！")
        return conn
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return None