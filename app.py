import pandas as pd
import streamlit as st
import tools
import requests

recipes = pd.read_csv("recipes.csv")

st.header("Welcome to the *Recipe Manager!* 🍳", text_alignment= "center")

home, add, view_all, history, search, shooping_list,ai = st.tabs(["Home", "Add", "View", "History", "Search", "Shopping list","AI Assistant"], on_change="rerun")

if home.open:
    with home:
        st.image("welcome.png", width=800)
        clicked = st.button("Get a random recipe 🤩")
        if clicked:
            res = tools.get_random(recipes)
            st.write(res)
            st.markdown("### Bon Appétit 🤤✨")

        st.write("--------------------------------------------")

        st.markdown("### Choose recipes by category")
        category = st.selectbox( "Choose a category", ["Breakfast", "Lunch", "Dinner", "Dessert"])
        show_category = st.button("Show Recipes")
        if show_category:
            result = tools.get_recipes_by_category(recipes, category)

            if not result.empty:
                st.write(result[["recipe_name", "prep_time_minutes", "difficulty", "category"]])

            else:
                st.warning("No recipes found in this category.")
#------------------------------------------------------------------------------------------------------

if add.open:
    with add:
        st.markdown("### To add a new recipe to your collection", text_alignment= "center")
        with st.form("my_form"):
            name = st.text_input("Enter recipe name:")
            ingredients = st.text_area("Enter the ingredients", height="content", max_chars=5000, placeholder="Enter ingredients separated by commas...")
            time = st.number_input("Preparation time in minutes", step = 1)
            Cooking_instructions = st.text_area("Enter the Cooking instructions", height="content", max_chars=5000,
                                                placeholder="Enter instructions steps saperated by dot...")
            category  = st.selectbox("Category", ["Breakfast", "Lunch", "Dinner", "Dessert"])
            difficulty  = st.selectbox("Difficulty level", ["Easy", "Medium", "Hard"])
            sentiment_mapping = ["one", "two", "three", "four", "five"]
            date = st.date_input("Date")
            st.write("Rate the recipe")
            rate = st.feedback("stars")
            submitted = st.form_submit_button("Submit")
        
        if submitted:
            tools.save_recipe_to_csv( name=name, ingredients=ingredients, prep_time=time, category=category,
                    instructions=Cooking_instructions, difficulty=difficulty, rating=rate, last_cooked_date=str(date))
            st.markdown("### New recipe was added successfully 🎉🍽️")
        
        
#------------------------------------------------------------------------------------------------------

if view_all.open:
    with view_all:
        st.markdown("### View all recipes", text_alignment= "center")
        st.markdown("#### My Recipes")
        st.dataframe(recipes[["recipe_name", "prep_time_minutes"]])

        st.markdown("#### External Recipes")
        tools.fetch_recipe_from_api()


#------------------------------------------------------------------------------------------------------

if history.open:
    with history:
        st.markdown("#### To get a recipe you did not do in a while...", text_alignment= "center")
        clicked_hist = st.button("Get a recipe")
        
        if clicked_hist:
            res_hist = tools.get_random_hist(recipes, "last_cooked_date")
            st.write(res_hist)
            st.markdown("### Bon Appétit 🤤✨")

        st.write("---------------------------------------------------------------------------------------------------------")
        st.markdown("#### To Track and view recipes you've made", text_alignment= "center")
        recipes[["recipe_name", "ingredients", "prep_time_minutes", "cooking_instructions", "rating", "last_cooked_date"]]
        
#------------------------------------------------------------------------------------------------------

if search.open:
    with search:
        st.markdown("### Search for a recipe by ingredient", text_alignment="center")
        ingredient = st.text_input("Enter an ingredient:")
        
        if st.button("Search"):
            if ingredient:
                result = tools.search_recipe_by_ingredient(recipes, ingredient)
                if not result.empty:
                    st.write(f"Recipes containing '{ingredient}'")
                    st.dataframe(result[
                            [
                                "recipe_name",
                                "ingredients",
                                "prep_time_minutes",
                                "difficulty",
                                "category"
                            ]])
                else:
                    st.markdown("### No recipes found with this ingredient.😔")
        
#------------------------------------------------------------------------------------------------------

if shooping_list.open:
    with shooping_list:
        st.markdown("### Create your shopping list 🛒", text_alignment="center")
        recipe_name = st.text_input("Enter recipe name:")
        quantity = st.number_input("How many servings do you want to make from this recipe?", min_value=1, step=1)
        clicked = st.button("Create shopping list")

        if clicked:
            result = tools.create_shopping_list(recipes, recipe_name, quantity)
            if result:
                st.markdown("### Shopping List")
                for ingredient in result:
                    st.write(f"- {ingredient}")

            else:
                st.write("Recipe not found")

# ---------------------------------------------------------------------------------------------------
if ai.open:
    with ai:
        st.markdown("### AI Recipe Assistant 🤖🍳", text_alignment="center")
        question = st.text_input("Ask something about cooking or recipes:")
        clicked = st.button("Ask AI")
        if clicked:
            if question:
                answer = tools.get_llm_response(question)
                st.write(answer)
            else:
                st.warning("Please enter a question.")