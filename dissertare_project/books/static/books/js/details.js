const amountInput = document.querySelector('.amount-input');

const increase = () => {
    if (Number(amountInput.value) - amountInput.max) {
        amountInput.value = Number(amountInput.value) + 1;
    }
}
const decrease = () => {
    if (Number(amountInput.value) > amountInput.min) {
        amountInput.value = Number(amountInput.value) - 1;
    }
}
