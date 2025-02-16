from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Настройки подключения к PostgreSQL
DB_CONFIG = {
    'dbname': 'yaroslav',
    'user': 'yaroslav',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

# Функция для подключения к базе данных
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Получение плана с событиями и маршрутом
@app.route('/plans/<int:plan_id>', methods=['GET'])
def get_plan(plan_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Получаем план
        cur.execute("SELECT id, name, created_at FROM plan WHERE id = %s", (plan_id,))
        plan = cur.fetchone()
        if not plan:
            return jsonify({"error": "Plan not found"}), 404

        # Получаем события для плана
        cur.execute("""
            SELECT e.id, e.name, e.city_id, e.latitude, e.langitude, e.description, e.adress, e.country_id, e.region_id, e.created_at, e.image
            FROM events e
            JOIN plan_events pe ON e.id = pe.event_id
            WHERE pe.plan_id = %s
        """, (plan_id,))
        events = cur.fetchall()

        # Формируем ответ
        result = {
            "plan": {
                "id": plan[0],
                "name": plan[1],
                "created_at": plan[2].isoformat()
            },
            "events": [
                {
                    "id": event[0],
                    "name": event[1],
                    "city_id": event[2],
                    "latitude": float(event[3]),
                    "langitude": float(event[4]),
                    "description": event[5],
                    "adress": event[6],
                    "country_id": event[7],
                    "region_id": event[8],
                    "created_at": event[9].isoformat(),
                    "images": event[10]
                } for event in events
            ]
        }

        cur.close()
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)