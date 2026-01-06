import React, { useState } from 'react'
import { supabase } from '../lib/supabase'

export default function Login() {
    const [loading, setLoading] = useState(false)
    const [email, setEmail] = useState('')
    const [sent, setSent] = useState(false)

    const handleLogin = async (e) => {
        e.preventDefault()
        setLoading(true)
        const { error } = await supabase.auth.signInWithOtp({ email })
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
                    <div className="toast-success" style={{ textAlign: 'left', padding: '1rem', borderRadius: 'var(--radius-md)', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid var(--success)' }}>
                        <p style={{ margin: 0, color: 'var(--success)' }}><strong>Link Sent.</strong></p>
                        <p style={{ margin: '0.5rem 0 0', fontSize: '0.875rem', color: 'var(--text-muted)' }}>Check your secure comms channel used for verification.</p>
                    </div>
                ) : (
                    <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        <div style={{ textAlign: 'left' }}>
                            <label style={{ display: 'block', color: 'var(--text-muted)', marginBottom: '0.5rem', fontSize: '0.75rem', fontWeight: 600, paddingLeft: '0.25rem' }}>OPERATOR ID</label>
                            <input
                                className="input-cyber"
                                type="email"
                                placeholder="identity@claritypearl.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        <button className="btn-primary" disabled={loading} style={{ width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            {loading ? <div className="spinner"></div> : 'INITIALIZE SESSION'}
                        </button>
                    </form>
                )}

                <div style={{ marginTop: '2.5rem', fontSize: '0.7rem', color: 'var(--text-muted)', opacity: 0.7 }}>
                    System Version 1.0.1 (Modular) <br />
                    Encrypted Connection (AES-256) Established
                </div>
            </div>
        </div>
    )
}
