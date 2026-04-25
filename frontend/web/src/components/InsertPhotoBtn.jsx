export default function InsertPhotoBtn({ text, onChange }) {
  return (
    <label className='btn'>
      {text}
      <input
        type='file'
        accept='image/*'
        hidden
        onChange={onChange}
      />
    </label>
  )
}
