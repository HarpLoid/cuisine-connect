from datetime import datetime
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import current_app, url_for
from app import db, bcrypt, ALLOWED_EXTENSIONS
import os
from app.models import (
    User, Recipe,
    Ingredient, RecipeStep, RecipeIngredient,
    Collection, Comment, Category
    )


def validate_header_image(header_image):
    # Accept only None or a string (URL/path), otherwise return None
    if header_image is None or isinstance(header_image, str):
        return header_image
    return None

def add_full_recipe(new_recipe_full: dict, contributor_id: int, recipe_id=None):
    header_image_path = None
    if 'header_image' in new_recipe_full and isinstance(new_recipe_full['header_image'], FileStorage):
        header_image_path = save_image(new_recipe_full['header_image'])
    
    # Add recipe category
    new_category = Category.query.filter_by(name=new_recipe_full["recipe_category"]).first()
    if new_category is None:
        new_category = Category(name=new_recipe_full["recipe_category"])
        db.session.add(new_category)
        db.session.commit()
        
    print("add_full_recipe", new_recipe_full)
    if recipe_id is None:
        new_recipe = Recipe(
            name=new_recipe_full["name"],
            header_image=header_image_path,
            prep_time=new_recipe_full["prep_time"],
            description=new_recipe_full["description"],
            contributor_id=contributor_id,
            category_id=new_category.id,
            # category=new_recipe_full["recipe_category"],
            # difficulty=new_recipe_full["difficulty"],
            # vegetarian=new_recipe_full["vegetarian"],
            # quantity=new_recipe_full["quantity"],
        )
        db.session.add(new_recipe)
        db.session.commit()
        recipe_id = new_recipe.id
    else:
        new_recipe = Recipe(
            id=recipe_id,
            name=new_recipe_full["name"],
            prep_time=new_recipe_full["prep_time"],
            description=new_recipe_full["description"],
            header_image=header_image_path,
            contributor_id=contributor_id,
            # category=new_recipe_full["recipe_category"],
            # difficulty=new_recipe_full["difficulty"],
            # vegetarian=new_recipe_full["vegetarian"],
            # quantity=new_recipe_full["quantity"],
        )
        db.session.add(new_recipe)
        db.session.commit()

    add_recipe_steps(new_recipe_full, recipe_id)
    add_recipe_ingredients(new_recipe_full, recipe_id)    
    
    return new_recipe

def add_recipe_steps(new_recipe_full: dict, recipe_id: int):
    # Add recipe steps
    counter = 0
    for step in new_recipe_full["recipe_steps"]:
        recipeStep = RecipeStep.query.filter_by(instruction=step).first()
        if recipeStep is not None:
            # If the step already exists, skip adding it
            continue
        recipe_step = RecipeStep(
            recipe_id=recipe_id,
            serial_number= counter + 1,
            instruction=step
        )
        db.session.add(recipe_step)
        counter += 1
    db.session.commit()

def add_recipe_ingredients(new_recipe_full: dict, recipe_id: int):
    # Add recipe ingredients
    for ingredient in new_recipe_full["recipe_ingredients"]:
        new_ingredient = Ingredient.query.filter_by(name=ingredient.get("name")).first()
        recipe_ingredient = RecipeIngredient.query.filter_by(
            recipe_id=recipe_id,
            ingredient_id=new_ingredient.id if new_ingredient else None
        ).first()
        # If the ingredient does not exist, create it and add it to the database
        if new_ingredient is None:
            new_ingredient = Ingredient(name=ingredient.get("name"))
            db.session.add(new_ingredient)
            db.session.commit()
        if recipe_ingredient is None:
            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe_id,
                ingredient_id=new_ingredient.id,
                quantity=ingredient.get("quantity", 1),
                unit=ingredient.get("unit")
            )
            db.session.add(recipe_ingredient)
    db.session.commit()

# This method just deletes the old one and creates a new one in its place
def edit_recipe(new_recipe_full, recipe: Recipe, user: User):
    recipe.contributor_id = user.id
    if 'header_image' in new_recipe_full and isinstance(new_recipe_full['header_image'], FileStorage):
        header_image_path = save_image(new_recipe_full['header_image'])
        recipe.header_image = header_image_path
    if recipe.ingredients:
        add_recipe_ingredients(new_recipe_full, recipe.id)
    if recipe.steps:
        add_recipe_steps(new_recipe_full, recipe.id)

    for attrib, val in new_recipe_full.items():
        if val:
            setattr(recipe, attrib, new_recipe_full[attrib])
    db.session.add(recipe)
    db.session.commit()


def add_new_user(new_user: dict):
    new_user["password"] = bcrypt.generate_password_hash(
        new_user["password"].encode("utf-8")
    )
    user = User(**new_user)
    db.session.add(user)
    db.session.commit()
    db.session.add(Collection(**{"name": "favorites", "user_id": user.id}))
    db.session.commit()
    
    return user.to_dict()


def get_recipe_by_id(id: int) -> Recipe:
    print(id)
    return Recipe.query.get(id)


def get_recipe_category(recipe: Recipe):
    return recipe.category.name if recipe.category else None


def get_next_of(id: int) -> int:
    ids = [recipe.id for recipe in Recipe.query.all()]
    next_id = 0
    for i in ids:
        if i > id:
            next_id = i
            break
    # print(f"next of {id}: {next_id}")
    return next_id


def get_prev_of(id: int) -> int:
    ids = [recipe.id for recipe in Recipe.query.all()]
    prev_id = 0
    for i in ids:
        if i < id and i > prev_id:
            prev_id = i
        elif i >= id:
            break
    # print(f"prev of {id}: {prev_id}")
    return prev_id

def get_header_image_url(recipe: Recipe):
    header_image_url = (
        url_for('static', filename=f'uploads/{os.path.basename(recipe.header_image)}', _external=True)
        if recipe.header_image else None
    )
    return header_image_url

def get_recipe_meta(recipe_by_id: Recipe):
    if not isinstance(recipe_by_id, Recipe):
        recipe_by_id = get_recipe_by_id(recipe_by_id)
    return {
        "id": recipe_by_id.id,
        "name": recipe_by_id.name,
        "prep_time": recipe_by_id.prep_time,
        "description": recipe_by_id.description,
        # "difficulty": recipe_by_id.difficulty,
        # "vegetarian": recipe_by_id.vegetarian,
        # "quantity": recipe_by_id.quantity,
        "category": recipe_by_id.category.name if recipe_by_id.category else None,
        "contributor_id": recipe_by_id.contributor.id,
        "contributor_username": recipe_by_id.contributor.username,
        "header_image": get_header_image_url(recipe_by_id),
        "next_id": get_next_of(recipe_by_id.id),
        "prev_id": get_prev_of(recipe_by_id.id),
    }


def get_recipe_ingredients(recipe: Recipe):
    return [
        {
            "name": recipe_ingredient.ingredient.name,
            "quantity": recipe_ingredient.quantity,
            "unit": recipe_ingredient.unit,
        }
        for recipe_ingredient in recipe.ingredients
    ]


def get_recipe_steps(recipe: Recipe):
    recipe.steps.sort(key=lambda step: step.serial_number)
    return [step.instruction for step in recipe.steps]


def get_contributor(recipe: Recipe):
    return {
        "contributor_name": recipe.contributor.name,
        "contributor_username": recipe.contributor.username,
        "contributor_bio": recipe.contributor.bio,
    }


def get_recipe_full(recipe: Recipe):
    return {
        "id": recipe.id,
        "name": recipe.name,
        "prep_time": recipe.prep_time,
        "description": recipe.description,
        # "difficulty": recipe.difficulty,
        # "vegetarian": recipe.vegetarian,
        # "quantity": recipe.quantity,
        "category": recipe.category.name if recipe.category else None,
        "contributor_name": recipe.contributor.name,
        "contributor_id": recipe.contributor.id,
        "contributor_username": recipe.contributor.username,
        "contributor_bio": recipe.contributor.bio,
        "header_image": get_header_image_url(recipe),
        "recipe_category": get_recipe_category(recipe),
        "recipe_ingredients": get_recipe_ingredients(recipe),
        "recipe_steps": get_recipe_steps(recipe),
        "next_id": get_next_of(recipe.id),
        "prev_id": get_prev_of(recipe.id),
    }


def get_comments_tree_for_recipe(recipe: Recipe):
    comments = Comment.query.filter(Comment.recipe_id == recipe.id)
    coms = {
        com.id: {
            "id": com.id,
            "text": com.text,
            "commenter": User.query.filter(User.id == com.commenter_id).first().username,
            "is_reply": com.is_reply,
            "reply_to": com.original_comment_id,
            "replies": [],
        }
        for com in comments
    }
    remove_list = []
    for id, com in coms.items():
        if com["is_reply"]:
            coms[com['reply_to']]["replies"].append(com)
            remove_list.append(id)
    for id in remove_list:
        del coms[id]
    coms = [coms[id] for id in coms]
    for com in coms:
        del com['is_reply']
        del com['reply_to']
    return coms

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(image_file):
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        # Add timestamp to filename to make it unique
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        # Return relative path for database storage
        return f'/static/uploads/{filename}'
    return None

