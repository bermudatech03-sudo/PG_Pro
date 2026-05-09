import { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../api/axios'

export default function Dashboard() {
    const { logout } = useAuth()
    const [properties, setProperties] = useState([])
    const [unpaid, setUnpaid] = useState([])

    useEffect(() => {
        api.get('/pgs/properties/').then(r => setProperties(r.data))
        api.get('/payments/unpaid/').then(r => setUnpaid(r.data))
    }, [])

    return (
        <div style={styles.container}>
            <div style={styles.header}>
                <h1 style={styles.title}>PG Pro Dashboard</h1>
                <button onClick={logout} style={styles.logout}>Logout</button>
            </div>

            {/* Properties */}
            <section style={styles.section}>
                <h2 style={styles.sectionTitle}>My Properties ({properties.length})</h2>
                <div style={styles.grid}>
                    {properties.map(p => (
                        <div key={p.id} style={styles.card}>
                            <h3 style={styles.cardTitle}>{p.name}</h3>
                            <p style={styles.cardText}>{p.city} - {p.pincode}</p>
                            <p style={styles.cardText}>Rooms: {p.rooms.length}</p>
                            <span style={{
                                ...styles.badge,
                                backgroundColor: p.status === 'active' ? '#dcfce7' : '#fee2e2',
                                color: p.status === 'active' ? '#16a34a' : '#dc2626'
                            }}>
                                {p.status}
                            </span>
                        </div>
                    ))}
                </div>
            </section>

            {/* Unpaid */}
            <section style={styles.section}>
                <h2 style={styles.sectionTitle}>
                    Unpaid Rent ({unpaid.length})
                </h2>
                <table style={styles.table}>
                    <thead>
                        <tr>
                            <th style={styles.th}>Tenant</th>
                            <th style={styles.th}>Month</th>
                            <th style={styles.th}>Due</th>
                            <th style={styles.th}>Paid</th>
                            <th style={styles.th}>Balance</th>
                            <th style={styles.th}>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {unpaid.map(p => (
                            <tr key={p.id}>
                                <td style={styles.td}>{p.tenant_name}</td>
                                <td style={styles.td}>{p.payment_month}</td>
                                <td style={styles.td}>₹{p.amount_due}</td>
                                <td style={styles.td}>₹{p.amount_paid}</td>
                                <td style={styles.td}>₹{p.balance_due}</td>
                                <td style={styles.td}>
                                    <span style={{
                                        ...styles.badge,
                                        backgroundColor: p.status === 'overdue' ? '#fee2e2' : '#fef9c3',
                                        color: p.status === 'overdue' ? '#dc2626' : '#854d0e'
                                    }}>
                                        {p.status}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </section>
        </div>
    )
}

const styles = {
    container: { padding: '24px', fontFamily: 'sans-serif' },
    header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' },
    title: { margin: 0, fontSize: '24px' },
    logout: { padding: '8px 16px', backgroundColor: '#ef4444', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
    section: { marginBottom: '32px' },
    sectionTitle: { fontSize: '18px', marginBottom: '12px' },
    grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '16px' },
    card: { backgroundColor: 'white', padding: '16px', borderRadius: '8px', boxShadow: '0 1px 4px rgba(0,0,0,0.1)' },
    cardTitle: { margin: '0 0 8px 0', fontSize: '16px' },
    cardText: { margin: '0 0 4px 0', fontSize: '13px', color: '#666' },
    badge: { padding: '2px 8px', borderRadius: '12px', fontSize: '12px' },
    table: { width: '100%', borderCollapse: 'collapse', backgroundColor: 'white' },
    th: { padding: '10px', textAlign: 'left', borderBottom: '2px solid #e5e7eb', fontSize: '13px' },
    td: { padding: '10px', borderBottom: '1px solid #f3f4f6', fontSize: '13px' }
}