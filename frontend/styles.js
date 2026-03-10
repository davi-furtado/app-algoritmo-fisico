import { StyleSheet } from 'react-native'

export default StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    padding: 12
  },
  row: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 50
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
    height: '80%',
    marginTop: 9,
    borderRadius: 8
  },
  full: {
    width: '100%',
    height: '100%',
    backgroundColor: '#000'
  },
  close: {
    color: 'invert',
    fontSize: 30,
    padding: 20,
    fontWeight: 'bold',
    marginTop: 'auto',
    marginRight: 'auto'
  },
  scroll: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center'
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
