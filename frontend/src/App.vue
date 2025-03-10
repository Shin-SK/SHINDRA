<template>
  <!-- 全ページのルートをラップする要素 -->
  <div ref="swipeArea" class="app-wrapper" style="width:100vw; height: 100vh;">
    <router-view />
  </div>

</template>

<script>
import { ref, watchEffect } from 'vue'
import { useSwipe } from '@vueuse/core'

export default {
  name: 'App',
  setup() {
    const swipeArea = ref(null)

    // useSwipe でスワイプ方向や距離が取得できる
    const { isSwiping, direction, lengthX } = useSwipe(swipeArea)

    // スワイプを監視して、「右に一定以上スワイプ」なら戻る処理
    watchEffect(() => {
      // ※ direction は 'LEFT' 'RIGHT' 'UP' 'DOWN' など
      if (isSwiping.value && direction.value === 'RIGHT' && lengthX.value > 30) {
        window.history.back()
      }
    })

    return {
      swipeArea
    }
  }
}
</script>
