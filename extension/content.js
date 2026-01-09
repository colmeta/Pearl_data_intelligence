console.log("👁️ Clarity Pearl: The Sovereign Extension Active.");

const API_BASE = "http://localhost:8000/api/bridge";

async function fetchIntelligence(name) {
    try {
        const res = await fetch(`${API_BASE}/identify?name=${encodeURIComponent(name)}`);
        return await res.json();
    } catch (e) {
        console.error("❌ Pearl Bridge Error:", e);
        return null;
    }
}

async function injectSovereignHUD() {
    const profileName = document.querySelector('.text-heading-xlarge')?.innerText;
    if (profileName) {
        console.log(`🧠 Sovereign Identity Sync Initiated: ${profileName}...`);

        const data = await fetchIntelligence(profileName);

        if (data && data.status === "found") {
            const h = document.createElement('div');
            h.id = "pearl-sovereign-hud";
            h.style.cssText = `
                position: fixed; top: 80px; right: 20px; width: 320px; 
                background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(10px);
                color: white; border-radius: 16px; z-index: 10000; padding: 20px;
                border: 1px solid rgba(59, 130, 246, 0.3); box-shadow: 0 20px 50px rgba(0,0,0,0.5);
                font-family: system-ui, -apple-system, sans-serif; transition: all 0.3s;
            `;

            h.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <span style="font-weight: 900; font-size: 0.8rem; letter-spacing: 1px; color: #3b82f6;">VAULT SYNCED</span>
                    <span style="font-size: 1.2rem;">💎</span>
                </div>
                <div style="font-size: 1.1rem; font-weight: 800; margin-bottom: 5px;">${data.full_name}</div>
                <div style="font-size: 0.8rem; opacity: 0.6; margin-bottom: 15px;">${data.company}</div>
                
                <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.7rem; margin-bottom: 5px;">
                        <span style="opacity: 0.6;">VELOCITY</span>
                        <span style="color: #22c55e; font-weight: 800;">${data.velocity}</span>
                    </div>
                    <div style="height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px;">
                        <div style="width: 85%; height: 100%; background: #3b82f6; border-radius: 2px;"></div>
                    </div>
                </div>

                <div style="font-size: 0.75rem; line-height: 1.5; color: rgba(255,255,255,0.8); border-left: 2px solid #3b82f6; padding-left: 10px;">
                    <strong>DISPLACEMENT:</strong><br/>
                    ${data.displacement_script.substring(0, 120)}...
                </div>
            `;

            document.body.appendChild(h);
        }
    }
}

// Observe for SPA changes
let lastUrl = location.href;
new MutationObserver(() => {
    const url = location.href;
    if (url !== lastUrl) {
        lastUrl = url;
        document.getElementById("pearl-sovereign-hud")?.remove();
        setTimeout(injectSovereignHUD, 3000);
    }
}).observe(document, { subtree: true, childList: true });

setTimeout(injectSovereignHUD, 3000);
