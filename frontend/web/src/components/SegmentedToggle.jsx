export default function SegmentedToggle({ options, value, onChange }) {
  return (
    <div style={{ display: 'flex', marginTop: 16 }}>
      {options.map(opt => (
        <button
          key={opt.key}
          onClick={() => onChange(opt.key)}
          style={{
            flex: 1,
            padding: 10,
            background: value === opt.key ? '#2c2c2c' : '#1a1a1a',
            color: '#fff',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          {opt.label}
        </button>
      ))}
    </div>
  )
}
