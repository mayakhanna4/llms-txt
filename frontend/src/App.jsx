import { Routes, Route } from 'react-router-dom'
import { useAuth } from '@clerk/react'
import AppLayout from './components/AppLayout'
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import GeneratedFiles from './pages/GeneratedFiles'

export default function App() {
  const { isLoaded, isSignedIn } = useAuth()

  if (!isLoaded) return null

  if (!isSignedIn) return <LandingPage />

  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/files" element={<GeneratedFiles />} />
      </Route>
    </Routes>
  )
}
