import React from "react";
import { Navigate } from "react-router-dom";

const WithPrivateRoute = ({ children }) => {
  const token = JSON.parse(sessionStorage.getItem("access_token"));

  if (token) {
    return children;
  }

  return <Navigate to="/login" />;
};

export default WithPrivateRoute;
