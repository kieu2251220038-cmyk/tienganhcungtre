import { BrowserRouter } from 'react-router-dom'

import './App.css'
import { AuthProvider } from './hooks/AuthContext'
import AppRoutes from './routes/AppRoutes'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
