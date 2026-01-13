import React, { useState } from 'react'
import { supabase } from '../lib/supabase'

export default function VelocityView() {
    const [timeframe, setTimeframe] = useState('7d')

    // Mock data for visualization (would hook up to real backend velocity endpoints)
    const metrics = {
        growth: '+124%',
        newLeads: 843,
        velocity: 'High',
        displacement: 'Active'
    }

    return (
        <div className="supreme-glass animate-slide-up" style={{ padding: '2rem', marginTop: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <span style={{ color: 'hsl(var(--pearl-primary))' }}>📈</span> VELOCITY ENGINE
                </h2>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                    {['24h', '7d', '30d'].map(t => (
                        <button
                            key={t}
                            onClick={() => setTimeframe(t)}
                            style={{
                                background: timeframe === t ? 'hsl(var(--pearl-primary))' : 'rgba(255,255,255,0.05)',
                                color: timeframe === t ? '#000' : '#fff',
                                border: 'none',
                                padding: '0.5rem 1rem',
                                borderRadius: '8px',
                                fontSize: '0.75rem',
                                fontWeight: 700,
                                cursor: 'pointer'
                            }}
                        >
                            {t.toUpperCase()}
                        </button>
                    ))}
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
                <div className="glass-panel" style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.03)' }}>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Lead Velocity</div>
                    <div style={{ fontSize: '2rem', fontWeight: 900, color: '#fff' }}>{metrics.growth}</div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--success)', marginTop: '0.5rem' }}>▲ Trending Up</div>
                </div>
                <div className="glass-panel" style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.03)' }}>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '1px' }}>New Targets</div>
                    <div style={{ fontSize: '2rem', fontWeight: 900, color: '#fff' }}>{metrics.newLeads}</div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>In last {timeframe}</div>
                </div>
                <div className="glass-panel" style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.03)' }}>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Pipeline Health</div>
                    <div style={{ fontSize: '2rem', fontWeight: 900, color: 'hsl(var(--pearl-primary))' }}>{metrics.velocity}</div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>Conversion Optimal</div>
                </div>
            </div>

            <div style={{ marginTop: '2rem', padding: '2rem', background: 'rgba(255,255,255,0.02)', borderRadius: '16px', border: '1px solid var(--glass-border)' }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 800, marginBottom: '1rem', color: 'rgba(255,255,255,0.8)' }}>Predictive Growth Trajectory</h3>
                <div style={{ height: '200px', display: 'flex', alignItems: 'flex-end', gap: '1rem', paddingBottom: '1rem', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                    {/* Simple CSS Bar Chart for Visual */}
                    {[40, 55, 45, 70, 85, 95, 120].map((h, i) => (
                        <div key={i} style={{
                            flex: 1,
                            height: `${h}px`,
                            background: `linear-gradient(to top, hsla(var(--pearl-primary), 0.2), hsla(var(--pearl-primary), 0.6))`,
                            borderRadius: '4px 4px 0 0',
                            position: 'relative',
                            transition: 'all 0.3s'
                        }}>
                            <div style={{
                                position: 'absolute',
                                bottom: '-25px',
                                left: '50%',
                                transform: 'translateX(-50%)',
                                fontSize: '0.6rem',
                                color: 'rgba(255,255,255,0.4)'
                            }}>
                                {['M', 'T', 'W', 'T', 'F', 'S', 'S'][i]}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}
