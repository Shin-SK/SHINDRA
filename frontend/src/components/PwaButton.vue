<template>
	<div>
	  <button @click="requestNotification">
		通知を許可する
	  </button>
	</div>
  </template>
  
  <script>
  export default {
	name: "NotificationButton",
	methods: {
	  requestNotification() {
		// OneSignalがロードされていれば呼び出す
		if (!window.OneSignal) {
		  console.log("OneSignalが読み込まれていません");
		  return;
		}
		window.OneSignal.push(() => {
		  OneSignal.registerForPushNotifications();
		});
	  }
	}
  };
  </script>
  