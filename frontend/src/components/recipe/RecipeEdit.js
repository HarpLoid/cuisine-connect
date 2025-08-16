import React, { useEffect } from "react";
import RecipeForm from "./recipe_form/RecipeForm";

import { useParams } from "react-router-dom";

import { useDispatch, useSelector } from "react-redux";
import { editRecipe, getDetailRecipe } from "../../redux/actions/recipes";
import { useNavigate } from "react-router-dom";

export default function RecipeEdit() {
  const dispatch = useDispatch();
  const { id } = useParams();
  const navigate = useNavigate();
  
  useEffect(() => {
    dispatch(getDetailRecipe(id));
  }, [id, dispatch]);

  const { detailRecipe, is_loading } = useSelector((state) => state.recipes);

  console.log("Edit", detailRecipe, "id", id)

  const handleFormSubmit = (formData) => {
    dispatch(editRecipe(id, formData)).then(() => {
      navigate("/dashboard");
    });
  };

  if (is_loading || !detailRecipe) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <RecipeForm
        buttonLabel="Update"
        handleFormSubmit={handleFormSubmit}
        editMode={true}
        recipe={detailRecipe}
      />
    </div>
  );
}
