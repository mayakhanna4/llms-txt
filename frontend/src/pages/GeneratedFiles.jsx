import { useEffect, useState } from 'react'
import { useUser } from '@clerk/react'
import { supabase } from '../utils/supabase/client'

export default function GeneratedFiles() {
  const { user } = useUser()
  const [files, setFiles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchFiles() {
      const { data, error } = await supabase
        .from('llms_versions')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })

      if (error) setError(error.message)
      else setFiles(data)
      setLoading(false)
    }

    fetchFiles()
  }, [user.id])

  if (loading) return <p>Loading…</p>
  if (error) return <p style={{ color: 'red' }}>{error}</p>

  return (
    <div>
      <h2>Generated Files</h2>
      {files.length === 0 ? (
        <p style={{ color: '#6b6375' }}>No files generated yet.</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #e5e4e7', color: '#6b6375', fontSize: '12px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              <th style={{ padding: '10px 16px', fontWeight: 500 }}>URL</th>
              <th style={{ padding: '10px 16px', fontWeight: 500, width: '80px' }}>Version</th>
              <th style={{ padding: '10px 16px', fontWeight: 500, width: '180px' }}>Created</th>
              <th style={{ padding: '10px 16px', fontWeight: 500, width: '160px' }}>Summary</th>
            </tr>
          </thead>
          <tbody>
            {files.map(file => (
              <tr key={file.id} style={{ borderBottom: '1px solid #e5e4e7' }}>
                <td style={{ padding: '12px 16px', maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {file.site_url}
                </td>
                <td style={{ padding: '12px 16px' }}>v{file.version}</td>
                <td style={{ padding: '12px 16px', whiteSpace: 'nowrap', color: '#6b6375' }}>
                  {new Date(file.created_at).toLocaleString()}
                </td>
                <td style={{ padding: '12px 16px', color: '#6b6375' }}>
                  {file.change_summary ?? '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
