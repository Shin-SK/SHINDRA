<template>
	<div class="wrap">
		<div class="success">
		<div class="area">
			<h2>THANK YOU</h2>
			<p>この度はご支援いただき<br>
			本当にありがとうございます<br>
			これでまだ私は<br>
			私のセカイを見ることができます<br>
			引き続きご愛顧のほど<br>
			よろしくお願い致します
			</p>
		</div>
		</div>
	</div>
  </template>


<script>
export default {
  name: "PaymentSuccess",
  mounted() {
    // window.confetti() が使える（CDNで読み込んでいるならグローバルで定義されている）
    if (typeof window.confetti === 'function') {
      window.confetti();
    }
  }
}
</script>