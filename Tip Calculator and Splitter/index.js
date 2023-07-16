const buttons = document.querySelectorAll('.btn1');
const customButton = document.getElementById('btn-special');
let previousButton = null;
const billInput = document.getElementById("bill");
let selectedTipPercentage = null;
const peopleInput = document.getElementById("people");
const tipMoney = document.querySelector(".amount.tipmoney");
const billMoney = document.querySelector(".amount.billmoney");
const resetButton = document.querySelector('.reset-btn');
const warning = document.querySelector('.warning');

buttons.forEach(button => {
  button.addEventListener('click', () => {
    if (previousButton) {
      previousButton.style.backgroundColor = '';
    }

    button.style.backgroundColor = 'skyblue';
    previousButton = button;
    selectedTipPercentage = button.value; // Store the tip percentage value
  });
});

customButton.addEventListener('click', () => {
  if (previousButton != null){
    previousButton.style.backgroundColor = '';
  }
  customButton.style.backgroundColor = 'skyblue';
  selectedTipPercentage = customButton.textContent.trim(); // Store the custom tip percentage value
});

// Splitter Code
billInput.addEventListener('input', handleInput);
peopleInput.addEventListener('input', handleInput);

function handleInput() {
  const billAmount = parseFloat(billInput.value);
  const totalPeople = parseFloat(peopleInput.value);

  if (!isNaN(billAmount) && !isNaN(totalPeople) && selectedTipPercentage !== null && totalPeople > 0) {
    warning.style.display = 'none';
    let tip;
    if (selectedTipPercentage === 'Custom') {
      const customTipInput = parseFloat(customButton.textContent.trim());
      tip = !isNaN(customTipInput) ? customTipInput : 0;
    } else {
      tip = parseFloat(selectedTipPercentage.replace(/%/g, ''));
    }
    calculateTip(billAmount, totalPeople, tip);
  }else if (isNaN(totalPeople)) {
    warning.style.display = 'inline';
    warning.style.color = 'red';
  }
}

function calculateTip(billAmount, totalPeople, tip) {
    const tipAmount = (billAmount * tip) / 100;
    const totalAmount = billAmount + tipAmount;
    const tipPerPerson = (tipAmount / totalPeople).toFixed(2);
    const billPerPerson = (totalAmount / totalPeople).toFixed(2);

    tipMoney.textContent = '₹' + tipPerPerson;
    billMoney.textContent = '₹' + billPerPerson;
}

resetButton.addEventListener('click', () => {
  // Reset input fields
  billInput.value = '';
  peopleInput.value = '';

  // Reset tip buttons
  if (previousButton) {
    previousButton.style.backgroundColor = '';
  }
  previousButton = null;
  selectedTipPercentage = null;

  // Reset custom button
  customButton.style.backgroundColor = '';
  customButton.textContent = 'Custom';

  // Reset displayed tip and bill amounts
  tipMoney.textContent = '₹0.00';
  billMoney.textContent = '₹0.00';
});
