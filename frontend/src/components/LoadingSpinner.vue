<template>
	<div class="loading-spinner">
	  <div class="spinner"></div>
	  <p>Loading...</p>
	</div>
  </template>
  
  <style scoped>
  .loading-spinner {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	min-height: 200px; /* 適宜調整 */
  }
  .spinner {
	width: 40px;
	height: 40px;
	border: 4px solid #ddd;
	border-top-color: #999;
	border-radius: 50%;
	animation: spin 1s linear infinite;
  }
  @keyframes spin {
	to {
	  transform: rotate(360deg);
	}
  }
  </style>
  