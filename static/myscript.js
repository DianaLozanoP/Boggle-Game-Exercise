const base_url = "http://127.0.0.1:5000/"

div_answer = $('.answer')
let SCORE = 0
let guesses = []

async function submitGuess(evt) {
    evt.preventDefault()
    //erasing previos feedback
    $(".feedback").empty()
    let guess = $('#guess').val()
    if (guesses.indexOf(guess) === -1) {
        //sending the request 
        const response = await axios({
            url: `${base_url}/verifyword/${guess}`
        })
        //getting back the answer from server
        let answer = response.data.result
        //handling the answer and give feedback to user
        if (answer === "ok") {
            guesses.push(guess)
            div_answer.prepend("<p class='feedback'>Hurray! That word is valid</p>")
            SCORE = SCORE + guess.length
            $("#score-count").text(`Current score:${SCORE}`)
        }
        else if (answer === "not-on-board") {
            div_answer.prepend("<p class='feedback'>Sorry, that word is not on the board. You can try again.</p>")
        }
        else if (answer === "not-a-word") {
            div_answer.prepend("<p class='feedback'>Sorry, that word is not in our dictionary. You can try again.</p>")

        }
    }
    else {
        div_answer.prepend("<p class='feedback'>Sorry, you already submitted that word.</p>")
    }
};

function runTimer() {
    let timeLimit = 60;
    //starting the timer
    const intervalOne = setInterval(function () {
        timeLimit = timeLimit - 1
        $(".timer").text(`Countdown ${timeLimit}`)
    }, 1000)
    //shutting down the timer and removing what is not needed
    setTimeout(function stopInterval() {
        clearInterval(intervalOne)
        $(".timer").addClass("out")
        $(".timer").text("You have run out of time. Hope you had fun! Refresh the page to start again.")
        $("#guess_form").hide()
        $("h4").hide()
        $(".feedback").hide()
        sendScoreToServer()
    }, 60000)
};

//calling out the timer function
runTimer();
//adding an Event Listener to handle clicks on the submit button of teh form
$("#submit").on("click", submitGuess)

async function sendScoreToServer() {
    await axios({
        url: `${base_url}/score/${SCORE}`,
    })
}