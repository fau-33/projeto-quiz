let score = 0;
let currentTopic = "";
let currentCorrectAnswer = "";
let questionsAttempted = 0;

const setupScreen = document.getElementById('setup-screen');
const loadingScreen = document.getElementById('loading-screen');
const quizScreen = document.getElementById('quiz-screen');
const finishScreen = document.getElementById('finish-screen');

const topicInput = document.getElementById('topic-input');
const startBtn = document.getElementById('start-btn');
const nextBtn = document.getElementById('next-btn');
const restartBtn = document.getElementById('restart-btn');

const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options-container');
const feedback = document.getElementById('feedback');
const scoreVal = document.getElementById('score-val');
const progressFill = document.getElementById('progress-fill');

// Event Listeners
startBtn.addEventListener('click', startQuiz);
nextBtn.addEventListener('click', generateQuestion);
restartBtn.addEventListener('click', () => {
  score = 0;
  questionsAttempted = 0;
  updateUI();
  showScreen(setupScreen);
});

topicInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') startQuiz();
});

async function startQuiz() {
  currentTopic = topicInput.value.trim() || "Conhecimentos Gerais";
  score = 0;
  questionsAttempted = 0;
  updateUI();
  await generateQuestion();
}

async function generateQuestion() {
  showScreen(loadingScreen);
  feedback.innerHTML = "";
  nextBtn.classList.add('hidden');

  try {
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topico: currentTopic })
    });

    const data = await response.json();

    if (data.error) {
      alert("Erro ao gerar pergunta: " + data.error);
      showScreen(setupScreen);
      return;
    }

    displayQuestion(data);
  } catch (err) {
    console.error(err);
    alert("Erro de conexão com o servidor.");
    showScreen(setupScreen);
  }
}

function displayQuestion(data) {
  showScreen(quizScreen);
  questionText.textContent = data.enunciado;
  currentCorrectAnswer = data.certa;

  optionsContainer.innerHTML = "";
  data.opcoes.forEach((opcao, index) => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.textContent = `${opcao}`;
    btn.addEventListener('click', () => checkAnswer(opcao, btn));
    optionsContainer.appendChild(btn);
  });
}

function checkAnswer(selected, btn) {
  const allButtons = optionsContainer.querySelectorAll('.option-btn');
  allButtons.forEach(b => b.disabled = true);

  questionsAttempted++;

  if (selected === currentCorrectAnswer) {
    btn.classList.add('correct');
    score += 100;
    feedback.innerHTML = `<span style="color: #2ecc71; font-weight: 600;">✨ Correto! +100 pontos</span>`;
  } else {
    btn.classList.add('wrong');
    feedback.innerHTML = `<span style="color: #e74c3c; font-weight: 600;">❌ Incorreto. A resposta era: ${currentCorrectAnswer}</span>`;

    // Mostrar a correta
    allButtons.forEach(b => {
      if (b.textContent === currentCorrectAnswer) {
        b.classList.add('correct');
      }
    });
  }

  updateUI();
  nextBtn.classList.remove('hidden');

  if (questionsAttempted >= 5) {
    nextBtn.textContent = "Finalizar Quiz";
    nextBtn.onclick = showFinalScore;
  } else {
    nextBtn.textContent = "Próxima Pergunta";
    nextBtn.onclick = generateQuestion;
  }
}

function updateUI() {
  scoreVal.textContent = score;
  const progress = (questionsAttempted / 5) * 100;
  progressFill.style.width = `${progress}%`;
}

function showScreen(screen) {
  [setupScreen, loadingScreen, quizScreen, finishScreen].forEach(s => s.classList.remove('active'));
  screen.classList.add('active');
}

function showFinalScore() {
  document.getElementById('final-score-val').textContent = score;
  const finalMsg = document.getElementById('final-msg');

  if (score >= 400) finalMsg.textContent = "Incrível! Você é um mestre nesse assunto! 🏆";
  else if (score >= 200) finalMsg.textContent = "Bom trabalho! Você tem um ótimo conhecimento. 👍";
  else finalMsg.textContent = "Continue praticando! O importante é aprender sempre. 📚";

  showScreen(finishScreen);
}
