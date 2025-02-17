import React, { useEffect, useState } from "react";
import axios from "axios";

const TopBatsmen = () => {
    const [batsmen, setBatsmen] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/top_batsmen")
            .then(response => {
                setBatsmen(response.data);
            })
            .catch(error => {
                console.error("Error fetching top batsmen:", error);
            });
    }, []);

    return (
        <div className="p-6 bg-white shadow-md rounded-lg mt-6">
            <h2 className="text-2xl font-bold text-gray-700 mb-4">Top Batsmen</h2>
            <ul className="space-y-2">
                {batsmen.map((batsman, index) => (
                    <li key={index} className="p-3 border rounded-md bg-gray-100">
                        {index + 1}. {batsman.player_name} - 🏏 {batsman.total_runs} runs
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TopBatsmen;
