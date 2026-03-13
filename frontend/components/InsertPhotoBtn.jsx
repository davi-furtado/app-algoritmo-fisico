import { Text, TouchableOpacity } from 'react-native'
import styles from '../styles'

export default function InsertPhotoBtn({ texto, onPress, isMobile }) {
  return (
    <TouchableOpacity
      style={styles.btn}
      onPress={() => onPress(isMobile)}
      activeOpacity={0.6}
    >
      <Text style={styles.btnText}>{texto}</Text>
    </TouchableOpacity>
  )
}
