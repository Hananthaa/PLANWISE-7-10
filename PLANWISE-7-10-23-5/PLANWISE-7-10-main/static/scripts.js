//accordian
var acc = document.getElementsByClassName ("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}


//input popoup 
function showInputPopup() {
  document.getElementById("inputPopup").style.display = "block";
  // Optionally clear the input field when the popup opens
  document.getElementById("inputText").value = "";
  document.getElementById("output").textContent = "";
}

function closeInputPopup() {
  document.getElementById("inputPopup").style.display = "none";
}

function processInput() {
  const inputText = document.getElementById("inputText").value;
  document.getElementById("output").textContent = "You entered: " + inputText;
  //sending it to a server or updating other parts of your page.
  console.log("User input:", inputText);
}

window.onclick = function(event) {
  if (event.target == document.getElementById("inputPopup")) {
    closeInputPopup();
  }
}

//attempt to add things in accordian ***
function addAccordionItem() {
  const title = document.getElementById("itemTitle").value.trim();
  const content = document.getElementById("itemContent").value.trim();

  if (title && content) {
    const accordionContainer = document.getElementById("accordionContainer");

    // Create the header element
    const header = document.createElement("div");
    header.classList.add("accordion-header");
    header.textContent = title;

    // Create a toggle indicator (optional, for visual cue)
    const toggleIndicator = document.createElement("span");
    toggleIndicator.textContent = "+"; // Or an arrow icon
    header.appendChild(toggleIndicator);

    // Add event listener to toggle content
    header.addEventListener("click", function() {
      this.classList.toggle("active");
      const contentDiv = this.nextElementSibling;
      if (contentDiv.style.display === "block") {
        contentDiv.style.display = "none";
        toggleIndicator.textContent = "+"; // Update indicator
      } else {
        contentDiv.style.display = "block";
        toggleIndicator.textContent = "-"; // Update indicator
      }
    });

    // Create the content element
    const contentDiv = document.createElement("div");
    contentDiv.classList.add("accordion-content");
    contentDiv.textContent = content;

    // Append the new elements to the accordion container
    accordionContainer.appendChild(header);
    accordionContainer.appendChild(contentDiv);

    // Close the popup after adding
    closeInputPopup();
  } else {
    alert("Please enter both a title and content.");
  }
}

//progress bar 
/*
function progressBar() {
  const checkboxes = document.querySelectorAll('.task-checkbox');
  const progressFill = document.getElementById('progressFill');
  const progressText = document.getElementById('progressText');
  const totalCheckboxes = checkboxes.length;

  checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', updateProgressBar);
  });

  function updateProgressBar() {
      console.log ("Bar updated...")
      const checkedCount = document.querySelectorAll('.task-checkbox:checked').length;
      const progressPercentage = (checkedCount / totalCheckboxes) * 100;

      progressFill.style.width = progressPercentage + '%';
      progressText.textContent = Math.round(progressPercentage) + '%';
  }
} */

document.addEventListener('DOMContentLoaded', function() {
  const examLists = document.querySelectorAll('ul'); // Assuming each exam's info is within a <ul>

  examLists.forEach(examList => {
    const checkboxes = examList.querySelectorAll('.task-checkbox');
    const progressBar = examList.querySelector('.progress-bar');
    const progressFill = examList.querySelector('#progressFill');
    const progressText = examList.querySelector('#progressText');

    if (checkboxes && progressBar && progressFill && progressText) {
      checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateProgressBar);
      });

      // Initial call to set the progress if some are checked by default
      updateProgressBar();

      function updateProgressBar() {
        const checkedCount = Array.from(checkboxes).filter(checkbox => checkbox.checked).length;
        const totalCount = checkboxes.length;
        const progress = totalCount > 0 ? (checkedCount / totalCount) * 100 : 0;

        progressFill.style.width = `${progress}%`;
        progressText.textContent = `${Math.round(progress)}%`;
      }
    }
  });
});

/*details for exam*/

function showInputPopup() {
  inputPopup = document.getElementById('inputPopup');
  inputPopup.style.display = 'block';
}

function closeInputPopup() {
    inputPopup.style.display = 'none';
}

function openExamDetails(subject, date, id) {
    document.getElementById('popup-subject').textContent = subject;
    document.getElementById('popup-date').textContent = date;
    // You might want to store the ID in the popup for further actions
    showInputPopup();
}
        
/*add topics*/
document.addEventListener('DOMContentLoaded', () => {
  const addTopicButtons = document.querySelectorAll('.add-topic-btn');
  const addTopicModal = document.getElementById('addTopicModal');
  const closeButton = document.querySelector('.close-button');
  const modalSubjectIdInput = document.getElementById('modalSubjectId');
  const addTopicForm = document.getElementById('addTopicForm');

  addTopicButtons.forEach(button => {
    button.addEventListener('click', () => {
      const subjectId = button.dataset.subjectId;
      modalSubjectIdInput.value = subjectId;
      addTopicModal.style.display = 'block';
    });
  });

  closeButton.addEventListener('click', () => {
    addTopicModal.style.display = 'none';
  });

  window.addEventListener('click', (event) => {
    if (event.target === addTopicModal) {
      addTopicModal.style.display = 'none';
    }
  });
});

/*progress bar func*/

/*const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');*/

function updateProgressBar(id) { 
    console.log
    checkboxes = document.querySelectorAll('.topic_checkbox-'+ id);
    progressFill = document.getElementById('progressFill-' + id);
    progressText = document.getElementById('progressText-' + id);
    totalCheckboxes = checkboxes.length;

    console.log ("Bar updated...")
    checkedCount = document.querySelectorAll('.topic_checkbox-' + id +':checked').length;
    progressPercentage = (checkedCount / totalCheckboxes) * 100;

    progressFill.style.width = progressPercentage + '%';
    progressText.textContent = Math.round(progressPercentage) + '%';
}

//timer

const startEl = document.getElementById("start");
const stopEl = document.getElementById("stop");
const resetEl = document.getElementById("reset");
const timerEl = document.getElementById("timer");
const setEl = document.getElementById("setEl");
const inputTimerMin = document.getElementById("inputTimerMin");
const inputTimerSec = document.getElementById("inputTimerSec");

function isIntegerString(str) {
    return /^-?\d+$/.test(str);
  }

//start here work
function setTimer() {

    if (isIntegerString(inputTimerMin.value) && isIntegerString(inputTimerSec.value)) {
        timeleft = parseInt(inputTimerMin.value*60) + parseInt(inputTimerSec.value);
        
      } else {
        timerleft = 0;
      } 

    updateTimer();
}


function updateTimer() {
    console.log ("====== function called" + timeleft);
    let minutes = Math.floor(timeleft / 60);
    let seconds = timeleft % 60;
    let formattedTime = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;

    timerEl.innerHTML = formattedTime;
}

function startTimer(){
    interval = setInterval(() => {
        timeleft--;
        updateTimer();
        if(timeleft === 0) {
            clearInterval(interval);
            alert("Time's up!");
            timeLeft = 60;
        }
    }, 1000);
}

function stopTimer(){
    clearInterval(interval);
}

function resetTimer(){
    clearInterval(interval);
    setTimer();
}

startEl.addEventListener("click", startTimer);
stopEl.addEventListener("click", stopTimer);
resetEl.addEventListener("click", resetTimer);