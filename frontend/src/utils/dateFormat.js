// src/utils/dateFormat.js
import dayjs from 'dayjs'

export function formatDateTime(dateString) {
  if (!dateString) return ''
  return dayjs(dateString).format('YYYY/MM/DD HH:mm')
}

// もし「日付だけでOK」なら別関数でもOK
export function formatDateOnly(dateString) {
  if (!dateString) return ''
  return dayjs(dateString).format('YYYY/MM/DD')
}
