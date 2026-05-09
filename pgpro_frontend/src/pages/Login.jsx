import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

export default function Login() {
    const { login } = useAuth()
    const navigate = useNavigate()
    const [form, setForm] = useState({ username: '', password: '' })
    const [error, setError] = useState('')

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            await login(form.username, form.password)
            navigate('/dashboard')
        } catch (err) {
            setError('Invalid username or password')
        }
    }

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <h2 style={styles.title}>PG Pro</h2>
                <p style={styles.subtitle}>Owner Login</p>
                {error && <p style={styles.error}>{error}</p>}
                <form onSubmit={handleSubmit}>
                    <input
                        style={styles.input}
                        placeholder="Username"
                        value={form.username}
                        onChange={e => setForm({ ...form, username: e.target.value })}
                    />
                    <input
                        style={styles.input}
                        type="password"
                        placeholder="Password"
                        value={form.password}
                        onChange={e => setForm({ ...form, password: e.target.value })}
                    />
                    <button style={styles.button} type="submit">
                        Login
                    </button>
                </form>
            </div>
        </div>
    )
}

const styles = {
    container: {
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f5f5f5'
    },
    card: {
        backgroundColor: 'white',
        padding: '40px',
        borderRadius: '8px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
        width: '360px'
    },
    title: {
        margin: '0 0 4px 0',
        fontSize: '24px',
        color: '#1a1a1a'
    },
    subtitle: {
        margin: '0 0 24px 0',
        color: '#666'
    },
    input: {
        width: '100%',
        padding: '10px',
        marginBottom: '12px',
        border: '1px solid #ddd',
        borderRadius: '4px',
        fontSize: '14px',
        boxSizing: 'border-box'
    },
    button: {
        width: '100%',
        padding: '10px',
        backgroundColor: '#2563eb',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        fontSize: '14px',
        cursor: 'pointer'
    },
    error: {
        color: 'red',
        fontSize: '13px',
        marginBottom: '12px'
    }
}