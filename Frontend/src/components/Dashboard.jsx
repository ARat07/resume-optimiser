import React, { useState } from 'react';

export default function Dashboard() {
    const [file, setFile] = useState(null);
    const [jobText, setJobText] = useState("");
    const [jobUrl, setJobUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);

    const handleAnalyze = async (e) => {
        e.preventDefault();
        setLoading(true);

        const formData = new FormData();
        formData.append("file", file);
        if (jobUrl) formData.append("job_url", jobUrl);
        if (jobText) formData.append("job_description", jobText);

        try {
            const response = await fetch("http://localhost:8000/api/analyze", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            if (response.ok) {
                setResults(data.data);
            } else {
                alert(data.detail);
            }
        } catch (err) {
            console.error(err);
            alert("Error connecting to server.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 p-8 font-sans text-gray-800">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-blue-600">Resume Optimizer Pro</h1>
                <p className="text-sm text-gray-500">AI-Powered ATS Analysis and Rewriting</p>
            </header>

            <main className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Input Section */}
                <div className="bg-white p-6 rounded-lg shadow-sm border">
                    <form onSubmit={handleAnalyze} className="space-y-6">
                        <div>
                            <label className="block font-medium mb-2">1. Upload Resume (PDF/DOCX)</label>
                            <input 
                                type="file" 
                                accept=".pdf,.docx" 
                                onChange={(e) => setFile(e.target.files[0])}
                                className="w-full border p-2 rounded"
                                required 
                            />
                        </div>
                        
                        <div>
                            <label className="block font-medium mb-2">2. Target Job Listing</label>
                            <input 
                                type="url" 
                                placeholder="Paste LinkedIn or Indeed URL..." 
                                value={jobUrl}
                                onChange={(e) => setJobUrl(e.target.value)}
                                className="w-full border p-2 rounded mb-2"
                            />
                            <div className="text-center text-sm text-gray-400 mb-2">- OR -</div>
                            <textarea 
                                placeholder="Paste Job Description here..." 
                                value={jobText}
                                onChange={(e) => setJobText(e.target.value)}
                                className="w-full border p-2 rounded h-32"
                            />
                        </div>

                        <button 
                            type="submit" 
                            disabled={loading}
                            className="w-full bg-blue-600 text-white py-3 rounded-lg font-bold hover:bg-blue-700 disabled:opacity-50"
                        >
                            {loading ? "Analyzing via AI..." : "Optimize Resume"}
                        </button>
                    </form>
                </div>

                {/* Results Section */}
                {results && (
                    <div className="bg-white p-6 rounded-lg shadow-sm border flex flex-col gap-6">
                        <div className="flex items-center justify-between border-b pb-4">
                            <h2 className="text-xl font-bold">Analysis Results</h2>
                            <div className="text-center">
                                <span className={`text-3xl font-bold ${results.ats_score > 75 ? 'text-green-500' : 'text-red-500'}`}>
                                    {results.ats_score}
                                </span>
                                <p className="text-xs text-gray-500">ATS Score</p>
                            </div>
                        </div>

                        <div>
                            <h3 className="font-semibold text-red-500 mb-2">Missing Keywords</h3>
                            <div className="flex flex-wrap gap-2">
                                {results.missing_keywords.map((kw, i) => (
                                    <span key={i} className="bg-red-50 text-red-600 px-2 py-1 text-xs rounded border border-red-200">
                                        {kw}
                                    </span>
                                ))}
                            </div>
                        </div>

                        <div>
                            <h3 className="font-semibold mb-2">Gap Analysis</h3>
                            <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded">{results.gap_analysis}</p>
                        </div>

                        <div className="flex-1">
                            <h3 className="font-semibold mb-2">Optimized Content</h3>
                            <textarea 
                                className="w-full h-64 border p-3 rounded text-sm font-mono bg-gray-50" 
                                defaultValue={results.optimized_resume_text}
                            />
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}