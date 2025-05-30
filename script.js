document.querySelector('.chat-input button').addEventListener('click', () => {
  const input = document.querySelector('.chat-input input');
  if (input.value.trim()) {
    alert(`Message sent: ${input.value}`);
    input.value = '';
  }
});
