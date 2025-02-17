import React, { useEffect, useState } from "react";
import axios from "axios";

const TopBowlers = () => {
    const [bowlers, setBowlers] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/top_bowlers")
            .then(response => {
                setBowlers(response.data);
            })
            .catch(error => {
                console.error("Error fetching top bowlers:", error);
            });
    }, []);

    return (
        <div>
            <h2>Top Bowlers</h2>
            <ul>
                {bowlers.map((bowler, index) => (
                    <li key={index}>
                        {bowler.player_name} - {bowler.total_wickets} wickets
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TopBowlers;
