import React, {useState, useEffect} from "react";
import {useDispatch} from "react-redux";
import {Route, Switch} from "react-router-dom";
import {authenticate} from "./store/session";
import SignupFormPage from "./components/SignupFormPage";
import LoginFormPage from "./components/LoginFormPage";
import AllVehiclesPage from "./components/Vehicles/AllVehiclesPage";
import Navigation from "./components/Navigation";
import Footer from "./components/Footer";
import YourVehiclesPage from "./components/Vehicles/YourVehiclesPage";
import LandingPage from "./components/LandingPage";
import VehicleDetailsPage from "./components/Vehicles/VehicleDetailsPage";
import ShopBrandPage from "./components/Vehicles/ShopBrandPage";
import ItemsPage from "./components/ShoppingCart/ItemsPage";

function App() {
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false);
  useEffect(() => {
    dispatch(authenticate()).then(() => setIsLoaded(true));
  }, [dispatch]);

  return (
    <>
      <Navigation isLoaded={isLoaded} />
      {isLoaded && (
        <>
          <Switch>
            <Route path="/items/:id">
              <ItemsPage />
            </Route>
            <Route path="/login">
              <LoginFormPage />
            </Route>
            <Route path="/signup">
              <SignupFormPage />
            </Route>
            <Route path="/vehicles/brand/:id">
              <ShopBrandPage />
            </Route>
            <Route path="/vehicles/current">
              <YourVehiclesPage />
            </Route>
            <Route path="/vehicles/all">
              <AllVehiclesPage />
            </Route>
            <Route path="/vehicles/:id">
              <VehicleDetailsPage />
            </Route>
            <Route path="/">
              <LandingPage />
            </Route>
          </Switch>
          <Footer />
        </>
      )}
    </>
  );
}

export default App;
