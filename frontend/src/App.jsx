import { useState } from "react";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);

  const [atsResult, setAtsResult] = useState(null);
  const [careerResult, setCareerResult] = useState(null);
  const [learningResult, setLearningResult] = useState(null);
  const [matchResult, setMatchResult] = useState(null);

  const analyzeResume = async () => {
    if (!file) {
      alert("Please upload a PDF first");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Resume Upload
      const response = await fetch(
        "http://127.0.0.1:8000/upload-resume",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setResult(data);

      // ATS Score
      const atsResponse = await fetch(
        "http://127.0.0.1:8000/ats-score",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            resume_skills: data.skills,
            job_skills: [
              "Java",
              "SQL",
              "Spring Boot",
              "Git",
              "React",
            ],
          }),
        }
      );

      const atsData = await atsResponse.json();
      setAtsResult(atsData);

      // Career Recommendation
      const careerResponse = await fetch(
        "http://127.0.0.1:8000/career-recommendation",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            skills: data.skills,
          }),
        }
      );

      const careerData = await careerResponse.json();
      setCareerResult(careerData);

      // Learning Tracker
      const learningResponse = await fetch(
        "http://127.0.0.1:8000/learning-tracker",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            current_skills: data.skills,
            target_role: "Backend Developer",
          }),
        }
      );

      const learningData = await learningResponse.json();
      setLearningResult(learningData);

      // Job Match Engine
      const matchResponse = await fetch(
        "http://127.0.0.1:8000/match-job",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            skills: data.skills,
          }),
        }
      );

      const matchData = await matchResponse.json();
      setMatchResult(matchData);

    } catch (error) {
      console.error(error);
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>🚀 CareerShield AI</h1>
      <p>Workforce Intelligence for the AI Era</p>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br />
      <br />

      <button onClick={analyzeResume}>
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      {/* Resume Upload */}
      {result && (
        <div
          style={{
            marginTop: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            padding: "20px",
          }}
        >
          <h2>Resume Uploaded Successfully</h2>

          <p>
            <strong>File:</strong> {result.filename}
          </p>

          <h3>Detected Skills</h3>

          <ul>
            {result.skills.map((skill) => (
              <li key={skill}>{skill}</li>
            ))}
          </ul>

          <h3>Resume Preview</h3>

          <pre
            style={{
              whiteSpace: "pre-wrap",
              maxHeight: "250px",
              overflow: "auto",
            }}
          >
            {result.resume_text}
          </pre>
        </div>
      )}

      {/* ATS Score */}
      {atsResult && (
        <div
          style={{
            marginTop: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            padding: "20px",
          }}
        >
          <h2>ATS Score</h2>
          <h1>{atsResult.ats_score}%</h1>
        </div>
      )}

      {/* Career Recommendation */}
      {careerResult && (
        <div
          style={{
            marginTop: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            padding: "20px",
          }}
        >
          <h2>Career Recommendation</h2>

          <h3>
            {careerResult.recommended_roles?.[0]}
          </h3>
        </div>
      )}

      {/* Learning Roadmap */}
      {learningResult && (
        <div
          style={{
            marginTop: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            padding: "20px",
          }}
        >
          <h2>Learning Roadmap</h2>

          <ul>
            {learningResult.skills_to_learn?.map((skill) => (
              <li key={skill}>{skill}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Job Match */}
      {matchResult && (
        <div
          style={{
            marginTop: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            padding: "20px",
          }}
        >
          <h2>Best Job Match</h2>

          <h3>{matchResult.best_match.role}</h3>

          <h1>{matchResult.best_match.match_score}%</h1>

          <h3>Missing Skills</h3>

          <ul>
            {matchResult.best_match.missing_skills.map((skill) => (
              <li key={skill}>{skill}</li>
            ))}
          </ul>

          <h3>{matchResult.profile_level}</h3>
        </div>
      )}
    </div>
  );
}

export default App;