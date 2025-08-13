import React from "react";
import RecipeForm from "./recipe_form/RecipeForm";

import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { createRecipe } from "../../redux/actions/recipes";

export default function RecipeCreate() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleFormSubmit = (formData) => {
    console.log("RecipeCreate", createRecipe(formData));
    dispatch(createRecipe(formData)).then(() => {
      navigate("/dashboard");
    });
  };

  return (
    <div>
      <RecipeForm
        buttonLabel="Create"
        editMode={false}
        handleFormSubmit={handleFormSubmit}
      />
    </div>
  );
}
