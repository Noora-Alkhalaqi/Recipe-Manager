import pandas as pd
import requests
import streamlit as st
from datetime import date
from openai import OpenAI
# from dotenv import load_dotenv
import os

# # Load API key from .env file
# load_dotenv(".env")

# openai_api_key = os.getenv("api_key")

openai_api_key = st.secrets["OPENAI_API_KEY"]
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY")

# Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openai_api_key
)
# -------------------------------------------------------------------------------------------------------
def get_random (df):
    '''
    Returns a random row from the given DataFrame.'''
    return df.sample()
# -------------------------------------------------------------------------------------------------------
 
def get_random_hist(df, name_of_col):
    '''
    Returns a random row from the given DataFrame sorted by the specified column (date).
    '''
    data = df.sort_values(by= name_of_col).head(3)
    return data.sample()
# -------------------------------------------------------------------------------------------------------
    
def fetch_recipe_from_api():
    """
    Fetches recipe details from the free TheMealDB REST API.
    """
    query = st.text_input("Enter a dish name to fetch (e.g., Arrabiata, Omelette):")
    if st.button("Fetch from API"):
        if query:
            url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['meals']:
                    meal = data['meals'][0]
                    name = meal['strMeal']
                    category = meal.get('strCategory', 'Uncategorized')
                    instructions = meal['strInstructions']

                    # Extract non-empty ingredients
                    ingredients_list = []

                    for i in range(1, 21):
                    
                        ingredient = meal.get(f"strIngredient{i}")
                        measure = meal.get(f"strMeasure{i}")
                    
                        if ingredient and ingredient.strip():                    
                            ingredient = ingredient.strip()                   
                            if measure and measure.strip():
                                ingredients_list.append(f"{measure.strip()} {ingredient}")
                            else:
                                ingredients_list.append(ingredient)
                    
                    
                    # Convert the list into one string
                    ingredients_str = ", ".join(ingredients_list)

                    save_recipe_to_csv(
                        name=name,
                        ingredients=ingredients_str,
                        prep_time=20,  # Default fallback
                        instructions=instructions,
                        difficulty="Medium",
                        category=category
                    )
                    st.write(f"Successfully imported '{name}' to your local recipes!")
                else:
                    st.write("No recipes found matching that query.")
            else:
                st.write("Failed to connect to the external API.")
# -------------------------------------------------------------------------------------------------------

def save_recipe_to_csv(name, ingredients, prep_time, instructions, difficulty,
                        category, rating = None, servings = 1, last_cooked_date = date.today()):
    '''
    Saves a new recipe to the local CSV file.'''

    new_recipe = pd.DataFrame([{
        "recipe_name": name,
        "ingredients": ingredients,
        "prep_time_minutes": prep_time,
        "cooking_instructions": instructions,
        "difficulty": difficulty,
        "category": category,
        "servings": servings,
        "rating": rating,
        "last_cooked_date": last_cooked_date
    }])

    new_recipe.to_csv("recipes.csv", mode="a", header=False, index=False, encoding="utf-8")

# -------------------------------------------------------------------------------------------------------

def search_recipe_by_ingredient(df, ingredient):
    '''
    Searches for recipes containing the specified ingredient in the DataFrame.
    '''

    result = df[df["ingredients"].str.contains(ingredient, case=False, na=False)]

    return result

# -------------------------------------------------------------------------------------------------------

def create_shopping_list(df, recipe_name, quantity):
    '''
    Creates a shopping list based on the specified recipe and quantity.'''

    # Search for the recipe
    recipe = df[df["recipe_name"].str.lower() == recipe_name.lower()]

    if recipe.empty:
        return []

    ingredients = recipe.iloc[0]["ingredients"]
    ingredients_list = ingredients.split(",")
    shopping_list = []

    for ingredient in ingredients_list:

        ingredient = ingredient.strip()
        parts = ingredient.split(" ", 1)
        if len(parts) == 2:

            amount = parts[0]
            ingredient_name = parts[1]
            try:
                if "/" in amount:
                    fraction = amount.split("/")
                    amount = (float(fraction[0]) / float(fraction[1]))

                else:
                    amount = float(amount)

                new_amount = amount * quantity

                if new_amount.is_integer():
                    new_amount = int(new_amount)

                shopping_list.append(f"{new_amount} {ingredient_name}")

            except:
                shopping_list.append(ingredient)

        else:
            shopping_list.append(ingredient)

    return shopping_list

# -------------------------------------------------------------------------------------------------------

def get_llm_response(prompt):
    '''
    Gets a response from the LLM based on the provided prompt.
    '''

    completion = client.chat.completions.create(

        model="cohere/north-mini-code:free",

        messages=[
            { "role": "system",
                "content": "You are a Smart Chef assistant."
                " Based on the ingredients the user provides,"
                " suggest a simple custom recipe. If the user asks "
                "for a dietary change such as vegan,"
                "suggest suitable ingredient substitutions." },

            {"role": "user", "content": prompt}],

        temperature=0.0
    )

    response = completion.choices[0].message.content

    return response

# -------------------------------------------------------------------------------------------------------

def get_recipes_by_category(df, category):
    '''
    Returns recipes from the DataFrame that match the specified category.
    '''
    result = df[df["category"] == category]
    return result