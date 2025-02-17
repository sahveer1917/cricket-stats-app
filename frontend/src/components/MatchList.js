import React, { useEffect, useState } from "react";
import axios from "axios";

const MatchList = () => {
    const [matches, setMatches] = useState([]);
    const [search, setSearch] = useState("");

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/matches")
            .then(response => {
                setMatches(response.data);
            })
            .catch(error => {
                console.error("Error fetching matches:", error);
            });
    }, []);

    const filteredMatches = matches.filter(match =>
        match.team1.toLowerCase().includes(search.toLowerCase()) ||
        match.team2.toLowerCase().includes(search.toLowerCase()) ||
        match.date.includes(search)
    );

    return (
        <div className="p-6 bg-white shadow-md rounded-lg">
            <h2 className="text-2xl font-bold text-gray-700 mb-4">IPL Matches</h2>
            <input
                type="text"
                placeholder="Search by team or date..."
                className="w-full p-2 border rounded-md mb-4"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />
            <ul className="space-y-2">
                {filteredMatches.map(match => (
                    <li key={match.match_id} className="p-3 border rounded-md bg-gray-100">
                        <strong>{match.date}</strong> - {match.team1} vs {match.team2} | 🏆 Winner: {match.winner}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default MatchList;
