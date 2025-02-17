import React, { useState } from "react";
import axios from "axios";

const AIQuery = () => {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        axios.post("http://127.0.0.1:5000/api/ask", { question })
            .then(response => {
                setAnswer(response.data.answer);
            })
            .catch(error => {
                setAnswer("I don't understand the question.");
            });
    };

    return (
        <div className="p-6 bg-white shadow-md rounded-lg mt-6">
            <h2 className="text-2xl font-bold text-gray-700 mb-4">Ask AI</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Ask about IPL stats..."
                    className="w-full p-2 border rounded-md mb-4"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />
                <button className="p-2 bg-blue-500 text-white rounded-md">Ask</button>
            </form>
            {answer && <p className="mt-4 text-lg font-semibold">{answer}</p>}
        </div>
    );
};

export default AIQuery;
