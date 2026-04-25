export default function CodeBox({ title, text }) {
  return (
    <div className='codeBox'>
      {title && <div className='codeTitle'>{title}</div>}
      <pre className='code'>{text}</pre>
    </div>
  )
}
