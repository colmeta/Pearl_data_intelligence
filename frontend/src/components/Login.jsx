import React, { useState } from 'react'
import { supabase } from '../lib/supabase'

export default function Login() {
    const [loading, setLoading] = useState(false)
    const [email, setEmail] = useState('')
    const [fullName, setFullName] = useState('')
    const [companyName, setCompanyName] = useState('')
    const [sent, setSent] = useState(false)

    const handleLogin = async (e) => {
        e.preventDefault()
        setLoading(true)

        // Capture Name and Company in metadata. 
        // signInWithOtp will create the user if they don't exist and trigger handle_new_user()
        const { error } = await supabase.auth.signInWithOtp({
            email,
            options: {
                data: {
                    full_name: fullName,
                    company_name: companyName
                }
            }
        })

        if (error) {
            alert(error.error_description || error.message)
        } else {
            setSent(true)
        }
        setLoading(false)
    }

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', position: 'relative', overflow: 'hidden' }}>
            {/* Background Decor */}
            <div style={{ position: 'absolute', width: '500px', height: '500px', background: 'radial-gradient(circle, var(--primary-glow) 0%, transparent 70%)', top: '-10%', right: '-10%', opacity: 0.2 }}></div>

            <div className="glass-panel animate-slide-up" style={{ padding: '3rem', maxWidth: '400px', width: '100%', textAlign: 'center', position: 'relative', zIndex: 10 }}>
                <div style={{ marginBottom: '2rem' }}>
                    <h1 className="text-gradient" style={{ margin: 0, fontSize: '3rem', letterSpacing: '-0.08em', fontWeight: 900 }}>CLARITY <span style={{ color: '#fff', fontWeight: 200 }}>PEARL</span></h1>
                    <p style={{ color: 'var(--text-muted)', letterSpacing: '4px', textTransform: 'uppercase', fontSize: '0.75rem', marginTop: '0.5rem', fontWeight: 600 }}>
                        Sensory Access Terminal
                    </p>
                </div>

                {sent ? (
                    <div className="status-badge status-completed" style={{ textAlign: 'left', padding: '1.5rem', borderRadius: 'var(--radius-md)', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid var(--success)', display: 'block' }}>
                        <p style={{ margin: 0, color: 'var(--success)', fontWeight: 800 }}>MAPPING INITIALIZED</p>
                        <p style={{ margin: '0.5rem 0 0', fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                            A secure magic link has been dispatched to <strong>{email}</strong>.
                            Confirm your identity to enter the lattice.
                        </p>
                    </div>
                ) : (
                    <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                        <div style={{ textAlign: 'left' }}>
                            <label style={{ display: 'block', color: 'var(--text-muted)', marginBottom: '0.5rem', fontSize: '0.6rem', fontWeight: 900, textTransform: 'uppercase', letterSpacing: '1px' }}>OPERATOR ID (EMAIL)</label>
                            <input
                                className="input-cyber"
                                type="email"
                                placeholder="identity@claritypearl.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                style={{ padding: '1rem' }}
                            />
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div style={{ textAlign: 'left' }}>
                                <label style={{ display: 'block', color: 'var(--text-muted)', marginBottom: '0.5rem', fontSize: '0.6rem', fontWeight: 900, textTransform: 'uppercase', letterSpacing: '1px' }}>FULL NAME</label>
                                <input
                                    className="input-cyber"
                                    type="text"
                                    placeholder="John Doe"
                                    value={fullName}
                                    onChange={(e) => setFullName(e.target.value)}
                                    required
                                    style={{ padding: '0.75rem' }}
                                />
                            </div>
                            <div style={{ textAlign: 'left' }}>
                                <label style={{ display: 'block', color: 'var(--text-muted)', marginBottom: '0.5rem', fontSize: '0.6rem', fontWeight: 900, textTransform: 'uppercase', letterSpacing: '1px' }}>COMPANY</label>
                                <input
                                    className="input-cyber"
                                    type="text"
                                    placeholder="Acme Inc"
                                    value={companyName}
                                    onChange={(e) => setCompanyName(e.target.value)}
                                    required
                                    style={{ padding: '0.75rem' }}
                                />
                            </div>
                        </div>

                        <button className="btn-primary" disabled={loading} style={{ width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '1rem', padding: '1rem' }}>
                            {loading ? <div className="spinner"></div> : 'INITIALIZE SESSION'}
                        </button>
                    </form>
                )}

                <div style={{ marginTop: '2.5rem', fontSize: '0.6rem', color: 'var(--text-muted)', opacity: 0.5, letterSpacing: '1px' }}>
                    SYSTEM VERSION 1.0.1 (MODULAR) <br />
                    ENCRYPTED CONNECTION (AES-256) ESTABLISHED
                </div>
            </div>
        </div>
    )
}
