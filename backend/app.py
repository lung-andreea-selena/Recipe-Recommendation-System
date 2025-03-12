from flask import Flask, jsonify
from utils.data_processing import get_cached_dataset

app = Flask(__name__)

@app.route('/')
def home():
    return "Recipe Recommendation System is running!"

@app.route('/recipes', methods=['GET'])
def get_recipes():
    df = get_cached_dataset()
    recipes = df[['title', 'NER', 'ingredients']].dropna().head(50).to_dict(orient="records")  # Limiting data
    return jsonify(recipes)

if __name__ == '__main__':
    app.run(debug=True)
