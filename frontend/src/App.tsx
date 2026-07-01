import { useState } from "react"

interface SignalScore {
  score: number
  recommendation: string
  reasoning: string
}

interface IntelligenceReport {
  claude_summary: string
  signal: SignalScore
  source: string
  fetched_at: string
}

const scoreColor = (score: number) => {
  if (score >= 7) return "#22c55e"
  if (score >= 4) return "#f59e0b"
  return "#ef4444"
}

export default function App() {
  const [company, setCompany] = useState("")
  const [report, setReport] = useState<IntelligenceReport | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const research = async () => {
    if (!company.trim()) return
    setLoading(true)
    setError("")
    setReport(null)

    try {
      const res = await fetch("http://localhost:8000/research", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company_name: company }),
      })
      if (!res.ok) throw new Error("Company not found")
      const data = await res.json()
      setReport(data)
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: "40px 24px", fontFamily: "system-ui, sans-serif" }}>

      <h1 style={{ fontSize: 32, fontWeight: 700, marginBottom: 4 }}>Empower</h1>
      <p style={{ color: "#6b7280", marginBottom: 32 }}>Company intelligence for CS students</p>

      <div style={{ display: "flex", gap: 12, marginBottom: 40 }}>
        <input
          value={company}
          onChange={e => setCompany(e.target.value)}
          onKeyDown={e => e.key === "Enter" && research()}
          placeholder="Enter a company name..."
          style={{
            flex: 1, padding: "12px 16px", fontSize: 16,
            border: "1px solid #d1d5db", borderRadius: 8, outline: "none"
          }}
        />
        <button
          onClick={research}
          disabled={loading}
          style={{
            padding: "12px 24px", fontSize: 16, fontWeight: 600,
            background: loading ? "#9ca3af" : "#111827", color: "white",
            border: "none", borderRadius: 8, cursor: loading ? "not-allowed" : "pointer"
          }}
        >
          {loading ? "Researching..." : "Research"}
        </button>
      </div>

      {error && (
        <div style={{ padding: 16, background: "#fef2f2", border: "1px solid #fecaca", borderRadius: 8, color: "#dc2626", marginBottom: 24 }}>
          {error}
        </div>
      )}

      {report && (
        <div>
          {/* Signal Score */}
          <div style={{
            display: "flex", alignItems: "center", gap: 24,
            padding: 24, background: "#f9fafb", borderRadius: 12, marginBottom: 32,
            border: "1px solid #e5e7eb"
          }}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 56, fontWeight: 800, color: scoreColor(report.signal.score), lineHeight: 1 }}>
                {report.signal.score}
              </div>
              <div style={{ fontSize: 12, color: "#6b7280", marginTop: 4 }}>/ 10</div>
            </div>
            <div>
              <div style={{
                display: "inline-block", padding: "4px 12px", borderRadius: 20,
                background: scoreColor(report.signal.score), color: "white",
                fontSize: 13, fontWeight: 600, marginBottom: 8, textTransform: "uppercase"
              }}>
                {report.signal.recommendation}
              </div>
              <p style={{ margin: 0, color: "#374151", lineHeight: 1.6 }}>{report.signal.reasoning}</p>
            </div>
          </div>

          {/* Brief */}
          <div style={{
            padding: 24, background: "white", border: "1px solid #e5e7eb",
            borderRadius: 12, whiteSpace: "pre-wrap", lineHeight: 1.8,
            color: "#111827", fontSize: 15
          }}>
            {report.claude_summary}
          </div>

          <p style={{ marginTop: 16, color: "#9ca3af", fontSize: 12 }}>
            {report.source} · {new Date(report.fetched_at).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  )
}
