// Buggy JavaScript Demo File
// This file contains common JavaScript issues for the agent to find

// Issue 1: Using var instead of let/const
var globalCounter = 0;

// Issue 2: Using console.log instead of proper logging
function calculateTotal(items) {
    console.log("Calculating total...");
    let total = 0;
    
    for (var i = 0; i < items.length; i++) {
        total += items[i].price;
    }
    
    return total;
}

// Issue 3: Using loose equality
function checkEqual(a, b) {
    if (a == b) {
        return true;
    }
    return false;
}

// Issue 4: Potential XSS with innerHTML
function displayUserName(userInput) {
    var element = document.getElementById('output');
    element.innerHTML = "Welcome, " + userInput;
}

// Issue 5: Using eval (security risk)
function executeCode(code) {
    eval(code);
}

// Issue 6: Any type in TypeScript
function processData(data: any): any {
    return data.map((item: any) => item.value);
}

// TODO: Refactor this function
async function fetchData(url) {
    const response = await fetch(url);
    const json = await response.json();
    return json;
}

// Missing async/await issue
// function badAsync() {
//     const result = await doSomething(); // This will fail!
// }

module.exports = {
    calculateTotal,
    checkEqual,
    displayUserName,
    executeCode,
    processData,
    fetchData
};
