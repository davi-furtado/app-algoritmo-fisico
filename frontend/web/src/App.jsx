/* eslint-disable no-unused-vars */
import { useState, useCallback } from 'react'
import './styles.css'
import CodeBox from './components/CodeBox'
import InsertPhotoBtn from './components/InsertPhotoBtn'
import SegmentedToggle from './components/SegmentedToggle'

const ip = import.meta.env.IP || 'localhost'
const url = `http://${ip}:8000/convert`

export default function App() {
  const [image, setImage] = useState(null)
  const [file, setFile] = useState(null)
  const [pseudocode, setPseudocode] = useState('')
  const [python, setPython] = useState('')
  const [output, setOutput] = useState('')
  const [view, setView] = useState('pseudo')
  const [loading, setLoading] = useState(false)
  const [zoom, setZoom] = useState(false)

  const sendImage = useCallback(async file => {
    setLoading(true)
    const form = new FormData()
    form.append('file', file)

    try {
      const res = await fetch(url, { method: 'POST', body: form })
      const data = await res.json()

      if (data.error) {
        setOutput(data.error)
        setPseudocode('')
        setPython('')
      } else {
        setPseudocode(data.pseudocode || '')
        setPython(data.python || '')
        setOutput(data.output || '')
      }
    } catch (e) {
      setOutput('Erro ao conectar')
    } finally {
      setLoading(false)
    }
  }, [])

  const handleFile = e => {
    const f = e.target.files[0]
    if (!f) return
    setFile(f)
    const url = URL.createObjectURL(f)
    setImage(url)
    sendImage(f)
  }

  const code = view === 'pseudo' ? pseudocode : python

  return (
    <div className='container'>
      <div className='row'>
        <InsertPhotoBtn
          text='Selecionar imagem'
          onChange={handleFile}
        />
      </div>

      {image && (
        <>
          <img
            src={image}
            className='image'
            onClick={() => setZoom(true)}
          />

          {zoom && (
            <div
              className='modal'
              onClick={() => setZoom(false)}
            >
              <img
                src={image}
                className='full'
              />
              <button className='modalBtn'>Fechar</button>
            </div>
          )}
        </>
      )}

      {loading && <p>Carregando...</p>}

      {output && (
        <CodeBox
          title='Saída'
          text={output}
        />
      )}

      {(pseudocode || python) && (
        <>
          <SegmentedToggle
            options={[
              { key: 'pseudo', label: 'Pseudocódigo' },
              { key: 'python', label: 'Python' }
            ]}
            value={view}
            onChange={setView}
          />

          <CodeBox
            title={view}
            text={code}
          />
        </>
      )}
    </div>
  )
}

