import { Text, TouchableOpacity } from 'react-native'
import { pickImage } from './App'

export default function InsertPhotoBtn({ texto, isWeb }) {
  return (
    <TouchableOpacity
      style={styles.btn}
      onPress={() => pickImage(~isWeb)}
      activeOpacity={0.75}
    >
      <Text style={styles.btnText}>{texto}</Text>
    </TouchableOpacity>
  )
}
