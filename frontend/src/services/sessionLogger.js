import axios from 'axios';

export async function logSession(data) {
  try {
    await axios.post('/api/logSession', {
      ...data,
      timestamp: new Date().toISOString(),
    });
    console.log('✅ Session logged');
  } catch (err) {
    console.error('❌ Logging failed:', err.message);
  }
}
