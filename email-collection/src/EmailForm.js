import React, { useState } from 'react';

const EmailForm = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!email) return;
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://127.0.0.1:5000/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();
      setMessage(data.message);
      setEmail('');
    } catch (error) {
      setMessage('An error occurred. Please try again.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 3000);
    }
  };

  return (
    <div className="App-header">
      <h2>Subscribe to our Newsletter</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{
              padding: '0.5rem',
              fontSize: '1rem',
              margin: '0.5rem',
              borderRadius: '4px',
              border: '1px solid #ccc'
            }}
            required
          />
        </label>
        <button
          type="submit"
          disabled={loading}
          className="email-button"
        >
          {loading ? 'Submitting...' : 'Subscribe'}
        </button>

      </form>
      {message && (
        <p style={{ marginTop: '1rem', fontWeight: 'bold', color: '#4caf50' }}>
          {message}
        </p>
      )}
    </div>
  );
};

export default EmailForm;
