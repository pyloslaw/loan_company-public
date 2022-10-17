function nextStep() {
    let step1 = document.getElementById('step-1');
    let step2 = document.getElementById('step-2');

    var result = step1.classList.remove('active'); step2.classList.add('active')
    return result
}

function previousStep() {
    let step1 = document.getElementById('step-1');
    let step2 = document.getElementById('step-2');

    var result = step2.classList.remove('active'); step1.classList.add('active');
    return result
}