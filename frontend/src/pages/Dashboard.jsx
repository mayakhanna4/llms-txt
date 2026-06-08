import { useState } from 'react'
import { useUser } from '@clerk/react'
import { supabase } from '../utils/supabase/client'

export default function Dashboard() {
  const { user } = useUser()
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleGenerate() {
    if (!url.trim()) return
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      })
      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || 'Something went wrong.')
      }
      const data = await res.json()
      setResult(data.llms_txt)

      // Determine next version for this user + URL
      const { data: existing } = await supabase
        .from('llms_versions')
        .select('version')
        .eq('user_id', user.id)
        .eq('site_url', url)
        .order('version', { ascending: false })
        .limit(1)

      const nextVersion = existing?.length ? existing[0].version + 1 : 1
      const storagePath = `${user.id}/${encodeURIComponent(url)}/v${nextVersion}/llms.txt`

      await supabase.storage
        .from('llms-files')
        .upload(storagePath, data.llms_txt, { contentType: 'text/plain' })

      await supabase.from('llms_versions').insert({
        user_id: user.id,
        site_url: url,
        version: nextVersion,
        storage_path: storagePath,
        change_summary: data.summary,
      })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') handleGenerate()
  }

  return (
    <div style={{ maxWidth: '720px' }}>
      <h3>Welcome, {user.firstName}</h3>
      <h3>Input a url to generate a LLMs.txt file</h3>

      <div style={{ display: 'flex', gap: '8px', margin: '24px 0' }}>
        <input
          type="url"
          placeholder="https://example.com"
          value={url}
          onChange={e => setUrl(e.target.value)}
          onKeyDown={handleKeyDown}
          style={{ flex: 1, padding: '10px 14px', fontSize: '16px', borderRadius: '6px', border: '1px solid #ccc' }}
        />
        <button onClick={handleGenerate} disabled={loading}>
          {loading ? 'Generating…' : 'Generate'}
        </button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && (
        <textarea
          readOnly
          value={result}
          style={{ width: '100%', height: '320px', fontFamily: 'monospace', fontSize: '13px', padding: '12px', borderRadius: '6px', boxSizing: 'border-box' }}
        />
      )}
    </div>
  )
}
