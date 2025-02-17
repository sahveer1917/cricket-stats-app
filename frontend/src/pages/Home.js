import React from "react";
import MatchList from "../components/MatchList";
import TopBatsmen from "../components/TopBatsmen";
import TopBowlers from "../components/TopBowlers";

const Home = () => {
    return (
        <div>
            <h1>IPL Cricket Stats</h1>
            <MatchList />
            <TopBatsmen />
            <TopBowlers />
        </div>
    );
};

export default Home;
