import {
  View,
  Text,
  Image,
  TouchableOpacity,
  ActivityIndicator,
  ScrollView,
  Modal,
  StyleSheet,
  Platform
} from 'react-native'

import { useState, useRef } from 'react'
import * as ImagePicker from 'expo-image-picker'
import WebView from 'react-native-webview'
import Asset from 'expo-asset'
import InsertPhotoBtn from './components/InsertPhotoBtn'

const url = 'http://SEU_IP_AQUI:8000/convert'
export default function App() {
  const [image, setImage] = useState(null)
  const [pseudocodigo, setPseudocodigo] = useState('')
  const [python, setPython] = useState('')
  const [saida, setSaida] = useState('')
  const [loading, setLoading] = useState(false)
  const [zoom, setZoom] = useState(false)

  const webRef = useRef(null)

  const enviarImagem = async uri => {
    setLoading(true)

    const ext = uri.split('.').pop()
    const mime =
      {
        jpg: 'image/jpeg',
        jpeg: 'image/jpeg',
        png: 'image/png',
        webp: 'image/webp'
      }[ext] || 'image/jpg'

    const form = new FormData()
    form.append('file', {
      uri,
      name: `ìmage.${ext}`,
      type: mime
    })

    try {
      const res = await fetch(url, {
        method: 'POST',
        body: form
      })

      const json = await res.json()
      if (json.erro) setSaida(json.erro)
      else {
        setPseudocodigo(json.pseudocodigo || '')
        setPython(json.python || '')
        setSaida(json.saida || '')
      }
    } catch (e) {
      setSaida(`Erro ao conectar com o servidor: ${e.message}`)
    }

    setLoading(false)
  }

  const pickImage = async camera => {
    const result = camera
      ? await ImagePicker.launchCameraAsync()
      : await ImagePicker.launchImageLibraryAsync()

    if (!result.canceled) {
      const uri = result.assets[0].uri
      setImage(uri)
      enviarImagem(uri)
    }
  }

  return (
    <ScrollView style={styles.container}>
      {/* Botões */}
      <View style={styles.row}>
        {Platform.OS !== 'web' && (
          <InsertPhotoBtn
            texto='Câmera'
            isWeb={false}
          />
        )}

        <InsertPhotoBtn
          texto='Galeria'
          isWeb={true}
        />
      </View>

      {image && (
        <>
          <TouchableOpacity onPress={() => setZoom(true)}>
            <Image
              source={{ uri: image }}
              style={styles.image}
            />
          </TouchableOpacity>

          <Modal
            visible={zoom}
            animationType='fade'
          >
            <TouchableOpacity onPress={() => setZoom(false)}>
              <Text style={styles.close}>x</Text>
            </TouchableOpacity>

            <Image
              source={{ uri: image }}
              style={styles.full}
            />
          </Modal>
        </>
      )}

      {loading && (
        <ActivityIndicator
          size='large'
          color='#fff'
          style={{ marginTop: 20 }}
        />
      )}

      {saida !== '' && <Text style={styles.saida}>{saida}</Text>}

      {python !== '' && (
        <ScrollView
          horizontal
          style={styles.codeBox}
        >
          <WebView
            ref={webRef}
            originWhitelist={['*']}
            source={{
              uri: Asset.fromModule(require('./assets/prism.html')).uri
            }}
            onLoadEnd={() => {
              webRef.current.postMessage(python)
            }}
            style={{ height: 320 }}
          />
        </ScrollView>
      )}
    </ScrollView>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    padding: 12
  },
  row: {
    flexDirection: 'row',
    gap: 8
  },
  btn: {
    backgroundColor: '#1760ff',
    padding: 12,
    flex: 1,
    borderRadius: 8
  },
  btnText: {
    color: '#fff',
    textAlign: 'center',
    fontWeight: 'bold'
  },
  image: {
    width: '100%',
    height: 220,
    marginTop: 12,
    borderRadius: 8
  },
  full: {
    width: '100%',
    height: '100%',
    backgroundColor: '#000'
  },
  close: {
    color: '#fff',
    fontSize: 30,
    padding: 20,
    position: 'absolute',
    zIndex: 10
  },
  saida: {
    color: '#0f0',
    marginTop: 12,
    fontFamily: 'monospace'
  },
  codeBox: {
    marginTop: 16
  }
})
