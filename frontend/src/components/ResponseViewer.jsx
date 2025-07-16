export default function ResponseViewer({ html }) {
  return (
    <article style={styles.container} dangerouslySetInnerHTML={{ __html: html }} />
  );
}

const styles = {
  container: {
    background: '#ffffff',
    padding: '2rem',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(0,0,0,0.05)',
    fontFamily: 'Georgia, serif',
    lineHeight: '1.6',
    maxWidth: '800px',
    margin: '2rem auto',
    color: '#333',
  }
};