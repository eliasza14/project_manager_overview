function animateCounter(elementId, startValue, endValue, duration) {
    let current = startValue;
    const range = endValue - startValue;
    const increment = endValue > startValue ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / range));
    const element = document.getElementById(elementId);
    const timer = setInterval(() => {
        current += increment;
        element.textContent = current;
        if (current === endValue) {
            clearInterval(timer);
        }
    }, stepTime);
}


function animateCounter2(elementId, startValue, endValue, duration) {
    let current = startValue;
    const range = endValue - startValue;
    const increment = endValue > startValue ? 0.1 : -0.1;
    const stepTime = Math.abs(Math.floor(duration / Math.abs(range)));
    const decimalPlaces = (endValue.toString().split('.')[1] || []).length;
    const element = document.getElementById(elementId);
    const timer = setInterval(() => {
        current += increment;
        element.textContent = current.toFixed(decimalPlaces);
        if ((increment > 0 && current >= endValue) || (increment < 0 && current <= endValue)) {
            clearInterval(timer);
        }
    }, stepTime);
}

function animateCounter3(elementId, startValue, endValue, duration) {
    let current = startValue;
    const range = endValue - startValue;
    const increment = endValue > startValue ? 0.1 : -0.1;
    const stepTime = Math.abs(Math.floor(duration / Math.abs(range)));
    const decimalPlaces = (endValue.toString().split('.')[1] || []).length;
    const element = document.getElementById(elementId);
    const timer = setInterval(() => {
        current += increment;
        element.textContent =current.toFixed(decimalPlaces)+ ' €';
        if ((increment > 0 && current >= endValue) || (increment < 0 && current <= endValue)) {
            clearInterval(timer);
        }
    }, stepTime);
}

// function animateCounter_v2span(className, duration) {
//     const elements = Array.from(document.getElementsByClassName(className));
    
//     elements.forEach((element) => {
//         const startValue = parseInt(element.getAttribute('data-val'), 10);
//         const endValue = parseInt(element.textContent, 10);
//         let current = startValue;
//         const range = endValue - startValue;
//         const increment = endValue > startValue ? 1 : -1;
//         const stepTime = Math.abs(Math.floor(duration / range));
    
//         const timer = setInterval(() => {
//         current += increment;
//         element.textContent = current;
//         if (current === endValue) {
//             clearInterval(timer);
//         }
//         }, stepTime);
//     });
//     }

function animateCounter3test(elementId, startValue, endValue, duration, intervalFactor) {
    let current = startValue;
    const range = endValue - startValue;
    const increment = endValue > startValue ? 0.1 : -0.1;
    const stepTime = Math.abs(Math.floor(duration / Math.abs(range))) * intervalFactor;
    const decimalPlaces = (endValue.toString().split('.')[1] || []).length;
    const element = document.getElementById(elementId);
    const timer = setInterval(() => {
        current += increment;
        element.textContent = current.toFixed(decimalPlaces) + ' €';
        if ((increment > 0 && current >= endValue) || (increment < 0 && current <= endValue)) {
            clearInterval(timer);
        }
    }, stepTime);
}
function animateCounter3test3(elementId, startValue, endValue, duration, interval) {
    let current = startValue;
    const range = endValue - startValue;
    const increment = endValue > startValue ? 0.1 : -0.1;
    const decimalPlaces = (endValue.toString().split('.')[1] || []).length;
    const element = document.getElementById(elementId);
    const iterations = Math.ceil(duration / interval);
    const valuePerIteration = range / iterations;
    let iteration = 0;
    
    const timer = setInterval(() => {
        current += increment * valuePerIteration;
        element.textContent = current.toFixed(decimalPlaces) + '€';
        iteration++;

        if ((increment > 0 && current >= endValue) || (increment < 0 && current <= endValue) || iteration >= iterations) {
            clearInterval(timer);
        }
    }, interval);
}
//Put sign on the number of delta
document.addEventListener('DOMContentLoaded', function() {
    const numberDiv = document.querySelector('.number');
    const number = parseFloat(numberDiv.textContent);

    if (number < 0) {
      numberDiv.classList.add('negative');
      numberDiv.setAttribute('data-sign', '-');
    } else {
      numberDiv.classList.add('positive');
      numberDiv.setAttribute('data-sign', '+');
    }
  });
/*
  function animateCounter3test2(elementId, startValue, endValue, duration, interval) {
    let current = startValue;
    const range = endValue - startValue;
    const decimalPlaces = (endValue.toString().split('.')[1] || []).length;
    const element = document.getElementById(elementId);
    const iterations = Math.ceil(duration / interval);
    const increment = range / iterations;
    let iteration = 0;

    const timer = setInterval(() => {
        current += increment;
        element.textContent = current.toFixed(decimalPlaces) + '€';
        iteration++;

        if ((increment > 0 && current >= endValue) || (increment < 0 && current <= endValue) || iteration >= iterations) {
            clearInterval(timer);
        }
    }, interval);
}
*/
function animateCounter3test2noEuro(elementId, startValue, endValue, duration, interval) {
    let current = startValue;
    const range = endValue - startValue;
    const decimalPlaces = (endValue.toString().split('.')[1] || []).length;
    const element = document.getElementById(elementId);
    const iterations = Math.ceil(duration / interval);
    const increment = range / iterations;
    let iteration = 0;

    const timer = setInterval(() => {
        current += increment;
        element.textContent = current.toFixed(decimalPlaces);
        iteration++;

        if ((increment > 0 && current >= endValue) || (increment < 0 && current <= endValue) || iteration >= iterations) {
            clearInterval(timer);
        }
    }, interval);
}

function animateCounter3test2WithEuro(elementId, startValue, endValue, duration, interval) {
    let current = startValue;
    let formattedVal2 = float(endValue).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const range = formattedVal2 - startValue;
    const decimalPlaces = (formattedVal2.toString().split('.')[1] || []).length;
    const element = document.getElementById(elementId);
    const iterations = Math.ceil(duration / interval);
    const increment = range / iterations;
    let iteration = 0;

    const timer = setInterval(() => {
        current += increment;
        element.textContent = current.toFixed(decimalPlaces) + "€";
        iteration++;

        if ((increment > 0 && current >= formattedVal2) || (increment < 0 && current <= formattedVal2) || iteration >= iterations) {
            clearInterval(timer);
        }
    }, interval);
}


function animateCounter3test3(elementId, startValue, endValue, duration, interval) {
    let current = startValue;
    const range = endValue - startValue;
    const decimalPlaces = (endValue.toString().split('.')[1] || []).length;
    const element = document.getElementById(elementId);
    const iterations = Math.ceil(duration / interval);
    const increment = range / iterations;
    let iteration = 0;
  
    const timer = setInterval(() => {
      current += increment;
  
      // Format the number with thousands and decimal separators using numeral.js
      const formattedNumber = numeral(current).format('0,0.00');
  
      element.textContent = formattedNumber + '€';
      iteration++;
  
      if (
        (increment > 0 && current >= endValue) ||
        (increment < 0 && current <= endValue) ||
        iteration >= iterations
      ) {
        clearInterval(timer);
      }
    }, interval);
  }

  
