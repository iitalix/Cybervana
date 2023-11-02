import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { getAllVehicles } from "../../../store/vehicles";

export default function AllVehiclesPage() {

    const dispatch = useDispatch();
    const allVehicles = useSelector((state) => state.vehicles.allVehicles);
    const arrVehicles = Object.values(allVehicles);
    const vehicles = [...arrVehicles];

    useEffect(() => {
        dispatch(getAllVehicles());
    }, [dispatch]);

    return (
        <div className="parent-container" id="allVehicles-parent-container">
            <h1>All Vehicles Page</h1>
            {vehicles.map((vehicle) => (

                <div key={vehicle.id}>
                    <img src={vehicle.photoUrl} alt="vehicle"></img>
                </div>

            ))}
        </div>
    )
}
