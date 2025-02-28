import React from "react";
import MatchList from "../components/MatchList";
import TopBatsmen from "../components/TopBatsmen";
import TopBowlers from "../components/TopBowlers";

const Home = () => {
    return (
        <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
            <h1 className="text-4xl font-extrabold text-blue-600 mb-6">🏏 IPL Cricket Stats</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl">
                <MatchList />
                <TopBatsmen />
                <TopBowlers />
            </div>
        </div>
    );
};

export default Home;
