import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Home from "./pages/Home";

const App = () => {
    return (
        <Router>
            <div className="min-h-screen bg-gray-100">
                {/* Navbar */}
                <div className="bg-blue-600 p-4 shadow-md">
                    <nav className="container mx-auto flex justify-between items-center">
                        <h1 className="text-white text-2xl font-bold">IPL Stats</h1>
                        <ul className="flex space-x-6">
                            <li>
                                <Link to="/" className="text-white text-lg hover:text-gray-300 transition">
                                    Home
                                </Link>
                            </li>
                        </ul>
                    </nav>
                </div>

                {/* Main Content */}
                <div className="container mx-auto py-6">
                    <Routes>
                        <Route path="/" element={<Home />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
};

export default App;
