import openai
from openai import OpenAI
import os
import random
from special_foods import special_foods

from flask import Flask, render_template, url_for, request, jsonify
app = Flask(__name__)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('page1.html', posts=posts)


@app.route("/ourGoals")
def goals():
    return render_template('page2.html', title='OurGoals')


@app.route("/About")
def about():
    return render_template('page3.html', title='OurGoals')


@app.route("/services")
def search_page():
    return render_template("Functional.html", title="search page")


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query.lower() in special_foods.keys():
        query = random.choice(special_foods[query.lower()])
    # Perform the search logic based on the query

    # Example: Return a JSON response
    client = OpenAI(
        api_key=""
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[{"role": "system",
                                                         "content": "You are the world's best cook. You can tell what ingredients are present in any given meal just from hearing the dish's name. When given a dish's name, you will first list out  all of it's ingredient in subsequent order with no elaboration in the format: (Ingredients: a b c (comma separated, and all on the same with no additional detail in parentheses and no comma used elsewhere)...)\
                                                             followed by a recipe to create that dish"},
                                                        {"role": "user",
                                                         "content": f"{query}"}], temperature=0)

    response = response.choices[0].message.content.splitlines()
    ingredients = response[0]
    recipe = response[2:]
    # ingredients = "Ingredients: flour, water, salt, filling of choice , soy sauce, sesame oil, ginger, garlic, green onions"
    # recipe = []
    ls = []
    for i in range(len(ingredients)):
        if ingredients[i] in ["(", ")"]:
            ls.append(i)
    while not (len(ls) % 2) and ls:
        ingredients = ingredients[:ls[0]] + ingredients[ls[1]+1:]
        ls.pop(0)
        ls.pop(0)
    ingredients = ingredients.split(",")[1:]
    ingredients = ''.join(
        [ingredient.strip()+"\n" for ingredient in ingredients])
    ingredients = f"Dish: {query}\n{ingredients}"
    print(ingredients)
    recipe = ''.join([line + "\n" for line in recipe])

    return jsonify([ingredients, recipe])


if __name__ == '__main__':
    app.run(debug=True)
