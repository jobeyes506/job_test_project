import React, { useState } from "react";

const JobTest = () => {
  const [answers, setAnswers] = useState({
    "关键问题": [],
    "倾向性问题": [],
    "细化调整问题": [],
    "二次确认问题": []
  });
  const [matchScore, setMatchScore] = useState(null);

  const handleChange = (category, value) => {
    setAnswers((prev) => ({
      ...prev,
      [category]: [parseFloat(value)]
    }));
  };

  const handleSubmit = async () => {
    const response = await fetch("http://your-backend-url:5000/submit_test", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ user_id: "test_user", answers })
    });

    const data = await response.json();
    setMatchScore(data.match_score);
  };

  return (
    <div className="p-5 max-w-lg mx-auto">
      <h2 className="text-xl font-bold mb-4">求职测评</h2>
      {Object.keys(answers).map((category) => (
        <div key={category} className="mb-3">
          <label className="block mb-1">{category}</label>
          <input
            type="number"
            className="border rounded p-2 w-full"
            onChange={(e) => handleChange(category, e.target.value)}
          />
        </div>
      ))}
      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white p-2 rounded w-full"
      >
        提交测评
      </button>
      {matchScore !== null && (
        <div className="mt-4 p-4 border rounded bg-gray-100">
          <h3 className="text-lg font-semibold">匹配分数: {matchScore}</h3>
        </div>
      )}
    </div>
  );
};

export default JobTest;
