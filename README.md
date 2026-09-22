# Recipe Manager

## Overview
A Streamlit-based recipe management system built with Python and Pandas. The project allows users to organize recipes, import recipes from an external API, generate shopping lists, search by ingredient, track cooking history, and interact with an AI-powered recipe assistant.

## Features

### Recipe Management
- Add new recipes to the local collection.
- Store recipe name, ingredients, preparation time, instructions, category, difficulty, rating, servings, and last cooked date.
- View saved recipes directly from the application.

### Recipe Discovery
- Generate a random recipe suggestion.
- Filter recipes by category.
- Search recipes by ingredient.
- Recommend recipes that have not been cooked recently.

### External Recipe Integration
The application integrates with **TheMealDB REST API**, allowing users to search for external recipes and import them into the local recipe collection.

Imported recipe data includes:
- Recipe name
- Category
- Ingredients and measurements
- Cooking instructions

### Shopping List Generator
Users can select a recipe and specify the required number of servings. The application calculates adjusted ingredient quantities and generates a shopping list.

### AI Recipe Assistant
The application includes an AI-powered cooking assistant connected through **OpenRouter** using the OpenAI Python SDK.

The assistant can:
- Suggest recipes based on available ingredients.
- Generate simple custom recipe ideas.
- Recommend ingredient substitutions.
- Support dietary requests such as vegan alternatives.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Interactive web interface |
| Pandas | Recipe data manipulation |
| Requests | REST API communication |
| OpenAI Python SDK | LLM client integration |
| OpenRouter | AI model access |
| TheMealDB API | External recipe data |
| CSV | Local recipe storage |


### Main Files

**`app.py`**  
Contains the Streamlit user interface and application navigation.

**`tools.py`**  
Contains the main application logic, including recipe search, CSV storage, API integration, shopping-list generation, and AI functionality.

**`recipes.csv`**  
Stores the local recipe dataset.

**`welcome.png`**  
Image displayed on the application's home page.

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Recipe-Manager
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```text
https://recipe-manager-ai.streamlit.app/
```

## Core Functions

The main application logic is implemented in `tools.py`.

| Function | Description |
|---|---|
| `get_random()` | Selects a random recipe from the dataset |
| `get_random_hist()` | Selects a recipe from those cooked least recently |
| `fetch_recipe_from_api()` | Searches TheMealDB and imports a recipe |
| `save_recipe_to_csv()` | Saves recipe information to `recipes.csv` |
| `search_recipe_by_ingredient()` | Filters recipes by ingredient |
| `create_shopping_list()` | Adjusts ingredient quantities based on servings |
| `get_llm_response()` | Sends a prompt to the AI cooking assistant |
| `get_recipes_by_category()` | Filters recipes by category |


## Future Improvements

Potential future enhancements include:

- Edit and delete recipe functionality
- Recipe images
- Favorites and bookmarks
- Improved ingredient parsing
- Nutritional information
- Advanced search and filtering
- Additional dietary preferences