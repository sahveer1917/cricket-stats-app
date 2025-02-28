import React, { useEffect, useState } from "react";
import axios from "axios";

const MatchList = () => {
    const [matches, setMatches] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/matches")
            .then(response => setMatches(response.data))
            .catch(error => console.error("Error fetching matches:", error));
    }, []);

    return (
        <div className="max-w-4xl mx-auto bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-2xl font-bold text-gray-700 mb-4">🏏 IPL Matches</h2>
            <ul className="space-y-4">
                {matches.map(match => (
                    <li key={match.match_id} className="p-4 border rounded-md bg-gray-50 hover:bg-gray-200 transition">
                        <strong className="text-blue-600">{match.date}</strong> - 
                        <span className="font-semibold"> {match.team1} vs {match.team2} </span> | 
                        🏆 <span className="text-green-600">{match.winner}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default MatchList;
