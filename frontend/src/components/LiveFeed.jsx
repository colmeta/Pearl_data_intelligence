import React, { useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'

export default function LiveFeed() {
    const [jobs, setJobs] = useState([])

    useEffect(() => {
        // Initial Fetch
        fetchJobs()

        // Realtime Subscription
        const channel = supabase
            .channel('public:jobs')
            .on('postgres_changes', { event: '*', schema: 'public', table: 'jobs' }, (payload) => {
                console.log('Change received!', payload)
                fetchJobs() // Re-fetch to keep it simple and consistent
            })
            .subscribe()

        return () => {
            supabase.removeChannel(channel)
        }
    }, [])

    const fetchJobs = async () => {
        const { data, error } = await supabase
            .from('jobs')
            .select('*')
            .order('created_at', { ascending: false })
            .limit(10)

        if (!error && data) {
            setJobs(data)
        }
    }

    const getStatusColor = (status) => {
        switch (status) {
            case 'completed': return 'var(--success)'
            case 'running': return 'var(--warning)'
            case 'failed': return 'var(--danger)'
            default: return 'var(--text-muted)'
        }
    }

    return (
        <div className="glass-panel" style={{ padding: '2rem', height: '100%', overflowY: 'auto' }}>
            <h2 className="text-gradient" style={{ marginTop: 0, fontSize: '1.25rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span className="animate-pulse-slow">📡</span> LIVE FEED
            </h2>

            {jobs.length === 0 ? (
                <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)', border: '1px dashed var(--border-subtle)', borderRadius: 'var(--radius-md)' }}>
                    <div style={{ marginBottom: '0.5rem', fontSize: '1.5rem', opacity: 0.5 }}>📶</div>
                    <p style={{ margin: 0, fontStyle: 'italic' }}>Awaiting signals...</p>
                </div>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {jobs.map((job) => (
                        <div key={job.id} className="animate-slide-up" style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            padding: '1rem',
                            background: 'rgba(15, 23, 42, 0.4)',
                            borderRadius: 'var(--radius-md)',
                            border: '1px solid var(--border-subtle)',
                            transition: 'all 0.2s'
                        }}>
                            <div>
                                <div style={{ fontWeight: 600, color: 'var(--text-main)', marginBottom: '0.25rem' }}>
                                    {job.query}
                                </div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>
                                    ID: {job.id.slice(0, 8)}
                                </div>
                            </div>
                            <div className={`status-badge status-${job.status}`}>
                                {job.status}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
