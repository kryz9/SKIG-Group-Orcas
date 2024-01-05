function checkAnswer() {
    var userAnswer = document.getElementById('answer').value;
    var correctAnswer = 4;  // Change this based on the correct answer

    if (userAnswer == correctAnswer) {
        document.getElementById('result').innerText = 'Correct!';
        // Update progress in the database (will be implemented later)
    } else {
        document.getElementById('result').innerText = 'Wrong answer. Try again!';
    }
}
