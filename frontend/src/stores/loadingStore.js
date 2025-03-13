// src/stores/loadingStore.js
import { defineStore } from 'pinia'

export const useLoadingStore = defineStore('loading', {
  state: () => ({
    loadingCount: 0,
    isLoading: false,
    loadingStartTime: null,
    minDisplayTime: 500, // ミリ秒。好みで調整
    timerId: null,
  }),
  actions: {
    increment() {
      this.loadingCount++
      if (this.loadingCount === 1) {
        // ローディング開始時刻を記録
        this.loadingStartTime = Date.now()
        // もしタイマーが残ってたらクリア
        if (this.timerId) {
          clearTimeout(this.timerId)
          this.timerId = null
        }
        // ローディング表示ON
        this.isLoading = true
      }
    },
    decrement() {
      if (this.loadingCount > 0) {
        this.loadingCount--
        // すべてのリクエストが完了したら
        if (this.loadingCount === 0) {
          // すでに経過した時間を計算
          const elapsed = Date.now() - this.loadingStartTime
          const wait = this.minDisplayTime - elapsed

          if (wait > 0) {
            // 足りない分だけ待ってからOFF
            this.timerId = setTimeout(() => {
              this.isLoading = false
              this.timerId = null
            }, wait)
          } else {
            // もう最低表示時間を超えているなら即OFF
            this.isLoading = false
          }
        }
      }
    }
  }
})
