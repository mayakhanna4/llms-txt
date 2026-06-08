import { SignInButton, SignUpButton } from '@clerk/react'

export default function LandingPage() {
  return (
    <div style={{ textAlign: 'center', marginTop: '100px' }}>
      <h1>llms.txt Generator</h1>
      <p>Automatically generate and track llms.txt for any website</p>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginTop: '32px' }}>
        <SignUpButton mode="modal">
          <button>Get Started</button>
        </SignUpButton>
        <SignInButton mode="modal">
          <button>Sign In</button>
        </SignInButton>
      </div>
    </div>
  )
}
