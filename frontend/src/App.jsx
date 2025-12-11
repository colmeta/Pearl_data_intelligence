import React, { useState } from 'react'

function App() {
    const [query, setQuery] = useState('')
    const [results, setResults] = useState([])

    const handleSearch = (e) => {
        e.preventDefault()
        // Simulated Search Result
        setResults([
            { name: "TechCorp Inc", ceo: "Alice Smith", verified: true },
            { name: "StartupOne", ceo: "Bob Jones", verified: false }
        ])
    }

    return (
        <div style={{ background: '#0f172a', minHeight: '100vh', color: 'white', fontFamily: 'sans-serif', padding: '2rem' }}>
            <header style={{ borderBottom: '1px solid #334155', paddingBottom: '1rem', marginBottom: '2rem' }}>
                <h1 style={{ color: '#38bdf8' }}>💎 Clarity Pearl</h1>
                <p style={{ color: '#94a3b8' }}>Sensory Nervous System for AI</p>
            </header>

            <main style={{ maxWidth: '800px', margin: '0 auto' }}>
                <form onSubmit={handleSearch} style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Search for Leads (e.g. 'SaaS CEOs in Austin')"
                        style={{ flex: 1, padding: '1rem', borderRadius: '8px', border: '1px solid #475569', background: '#1e293b', color: 'white' }}
                    />
                    <button type="submit" style={{ padding: '0 2rem', background: '#38bdf8', border: 'none', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer' }}>
                        Hunt
                    </button>
                </form>

                <div className="results">
                    {results.map((r, i) => (
                        <div key={i} style={{ background: '#1e293b', padding: '1.5rem', borderRadius: '12px', marginBottom: '1rem', border: '1px solid #334155', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div>
                                <h3 style={{ margin: 0 }}>{r.name}</h3>
                                <p style={{ margin: 0, color: '#94a3b8' }}>CEO: {r.ceo}</p>
                            </div>
                            {r.verified && <span style={{ background: '#059669', color: '#ecfdf5', padding: '0.25rem 0.75rem', borderRadius: '99px', fontSize: '0.875rem' }}>✓ Verified</span>}
                        </div>
                    ))}
                </div>
            </main>
        </div>
    )
}

export default App
