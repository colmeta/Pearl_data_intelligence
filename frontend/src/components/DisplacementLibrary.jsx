import React, { useState } from 'react'
import { supabase } from '../lib/supabase'

export default function DisplacementLibrary() {
    const [selectedScript, setSelectedScript] = useState(null)
    const [copySuccess, setCopySuccess] = useState('')

    // Mock data for displacement scripts
    const scripts = [
        {
            id: 1,
            title: 'The "Trojan Horse" Intro',
            category: 'Cold Outreach',
            content: "Hi {{firstName}},\n\nI noticed you're using {{competitor}} for your data needs. Just wanted to share a quick report we ran on your site showing 3 missed opportunities...\n\nWould you be open to seeing the full data set?",
            effectiveness: '94%'
        },
        {
            id: 2,
            title: 'Value-Add Follow Up',
            category: 'Nurture',
            content: "Hey {{firstName}},\n\nThinking about our chat regarding {{painPoint}}. I found this case study relevant to your situation with {{company}}...\n\nLet me know if this resonates.",
            effectiveness: '88%'
        },
        {
            id: 3,
            title: 'The "Break Up" Email',
            category: 'Re-engagement',
            content: "Hi {{firstName}},\n\nI haven't heard back, so I assume you're all set with {{currentSolution}} or busy scaling {{company}}.\n\nI'll close your file for now, but feel free to reach out if priorities change.",
            effectiveness: '76%'
        }
    ]

    const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text)
        setCopySuccess('Copied!')
        setTimeout(() => setCopySuccess(''), 2000)
    }

    return (
        <div className="supreme-glass animate-slide-up" style={{ padding: '2rem', marginTop: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <span style={{ color: 'hsl(var(--pearl-primary))' }}>⚡</span> SOVEREIGN DISPLACEMENT LIBRARY
                </h2>
                <button className="btn-primary" style={{ padding: '0.5rem 1rem', fontSize: '0.75rem' }}>
                    + NEW SCRIPT
                </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '2rem' }}>
                {/* Sidebar List */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {scripts.map(script => (
                        <div
                            key={script.id}
                            onClick={() => setSelectedScript(script)}
                            className="glass-panel"
                            style={{
                                padding: '1rem',
                                cursor: 'pointer',
                                background: selectedScript?.id === script.id ? 'rgba(6, 182, 212, 0.1)' : 'rgba(255,255,255,0.03)',
                                borderColor: selectedScript?.id === script.id ? 'hsl(var(--pearl-primary))' : 'transparent',
                                transition: 'all 0.2s'
                            }}
                        >
                            <div style={{ fontSize: '0.9rem', fontWeight: 700, color: '#fff', marginBottom: '0.3rem' }}>{script.title}</div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', background: 'rgba(255,255,255,0.05)', padding: '2px 6px', borderRadius: '4px' }}>
                                    {script.category.toUpperCase()}
                                </span>
                                <span style={{ fontSize: '0.65rem', color: 'var(--success)', fontWeight: 700 }}>{script.effectiveness} Win Rate</span>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Content Viewer */}
                <div className="glass-panel" style={{ padding: '2rem', minHeight: '400px', display: 'flex', flexDirection: 'column', background: 'rgba(0,0,0,0.2)' }}>
                    {selectedScript ? (
                        <>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1rem' }}>
                                <div>
                                    <h3 style={{ margin: 0, fontSize: '1.2rem', fontWeight: 800, color: '#fff' }}>{selectedScript.title}</h3>
                                    <p style={{ margin: '0.5rem 0 0', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Category: {selectedScript.category}</p>
                                </div>
                                <button
                                    onClick={() => copyToClipboard(selectedScript.content)}
                                    className="btn-ghost"
                                    style={{
                                        background: 'rgba(255,255,255,0.05)',
                                        border: '1px solid rgba(255,255,255,0.1)',
                                        padding: '0.5rem 1rem',
                                        fontSize: '0.75rem',
                                        borderRadius: '8px'
                                    }}
                                >
                                    {copySuccess || '📋 COPY SCRIPT'}
                                </button>
                            </div>
                            <div style={{
                                flex: 1,
                                background: 'rgba(0,0,0,0.3)',
                                borderRadius: '12px',
                                padding: '1.5rem',
                                fontFamily: 'monospace',
                                color: 'rgba(255,255,255,0.8)',
                                lineHeight: '1.6',
                                whiteSpace: 'pre-wrap',
                                fontSize: '0.9rem'
                            }}>
                                {selectedScript.content}
                            </div>
                            <div style={{ marginTop: '1.5rem', fontSize: '0.75rem', color: 'rgba(255,255,255,0.4)', fontStyle: 'italic' }}>
                                Tip: Variables like {'{{firstName}}'} will be auto-replaced when using the Forge.
                            </div>
                        </>
                    ) : (
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)', flexDirection: 'column', gap: '1rem' }}>
                            <div style={{ fontSize: '2rem', opacity: 0.3 }}>⚡</div>
                            <p>Select a script to view details</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
