import { NavLink } from 'react-router-dom'
import { UserButton } from '@clerk/react'

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/files', label: 'Generated Files' },
]

export default function Sidebar() {
  return (
    <aside style={{
      width: '200px',
      minHeight: '100vh',
      borderRight: '1px solid #e5e4e7',
      display: 'flex',
      flexDirection: 'column',
      padding: '24px 16px',
      boxSizing: 'border-box',
      gap: '8px',
    }}>
      <h2 style={{ margin: '0 0 24px', fontSize: '18px' }}>llms.txt</h2>
      {links.map(({ to, label }) => (
        <NavLink
          key={to}
          to={to}
          end
          style={({ isActive }) => ({
            display: 'block',
            padding: '8px 12px',
            borderRadius: '6px',
            textDecoration: 'none',
            color: isActive ? '#aa3bff' : 'inherit',
            background: isActive ? 'rgba(170,59,255,0.08)' : 'transparent',
            fontWeight: isActive ? 500 : 400,
          })}
        >
          {label}
        </NavLink>
      ))}
      <div style={{ marginTop: 'auto' }}>
        <UserButton />
      </div>
    </aside>
  )
}
