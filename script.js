const $=(s)=>document.querySelector(s);const $$=(s)=>document.querySelectorAll(s);
const menuBtn=$('.menu-btn'),navLinks=$('.nav-links');
menuBtn?.addEventListener('click',()=>{const open=navLinks.classList.toggle('open');menuBtn.setAttribute('aria-expanded',open)});
navLinks?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>navLinks.classList.remove('open')));

const subjectData={
'Computer Science':{icon:'💻',topics:['Data Structures & Algorithms','DBMS','Operating Systems','Computer Networks','Python','Software Engineering']},
'Mathematics':{icon:'📐',topics:['Algebra','Calculus','Geometry','Probability','Statistics','Discrete Mathematics']},
'General Studies':{icon:'🧠',topics:['Indian Polity','History','Geography','Economy','Science & Technology','Static GK']},
'Generative AI':{icon:'🤖',topics:['LLMs','Prompt Engineering','RAG','AI Agents','Embeddings','GenAI Applications']}
};
$$('.subject-open').forEach(btn=>btn.addEventListener('click',()=>{const card=btn.closest('.subject-card'),name=card.dataset.subject,data=subjectData[name];const panel=$('#subject-panel');panel.innerHTML=`<div class="panel-head"><div><span class="eyebrow">${data.icon} ${name.toUpperCase()}</span><h3>Choose a topic</h3></div><button class="close-panel" aria-label="Close">×</button></div><div class="topic-list">${data.topics.map((t,i)=>`<button class="topic-item"><span>${String(i+1).padStart(2,'0')}</span>${t}<b>→</b></button>`).join('')}</div>`;panel.classList.remove('hidden');panel.scrollIntoView({behavior:'smooth',block:'nearest'});panel.querySelector('.close-panel').onclick=()=>panel.classList.add('hidden');panel.querySelectorAll('.topic-item').forEach(t=>t.onclick=()=>{alert(`${t.textContent.trim().replace(/^\d+/, '')} content will be added in the next module.`)})}));

$$('.exam-open').forEach(btn=>btn.addEventListener('click',()=>{const exam=btn.dataset.exam;document.querySelector('#practice').scrollIntoView({behavior:'smooth'});setTimeout(()=>{alert(`${exam} preparation module selected. Practice questions are ready below.`)},500)}));
$$('.resource-btn').forEach(btn=>btn.addEventListener('click',()=>alert(`${btn.dataset.resource} module selected. This section is ready for content integration.`)));

const questions=[
{q:'Which data structure follows LIFO?',o:['Queue','Stack','Linked List','Tree'],a:1,t:'Data Structures',d:'Easy'},
{q:'Which language is primarily used to style web pages?',o:['HTML','CSS','Python','SQL'],a:1,t:'Web Basics',d:'Easy'},
{q:'What does DBMS stand for?',o:['Data Backup Management System','Database Management System','Digital Base Memory Service','Database Machine Software'],a:1,t:'DBMS',d:'Easy'},
{q:'Which protocol is used for secure web communication?',o:['HTTP','FTP','HTTPS','SMTP'],a:2,t:'Computer Networks',d:'Easy'},
{q:'What is the output type of a Python function with no return statement?',o:['None','0','False','Empty string'],a:0,t:'Python',d:'Easy'},
{q:'Which SQL command is used to retrieve data?',o:['INSERT','UPDATE','SELECT','DELETE'],a:2,t:'SQL',d:'Easy'},
{q:'Which OS component manages processes and memory?',o:['Kernel','Compiler','Browser','Editor'],a:0,t:'Operating Systems',d:'Medium'},
{q:'What is the time complexity of binary search on a sorted array?',o:['O(n)','O(log n)','O(n²)','O(1)'],a:1,t:'Algorithms',d:'Medium'},
{q:'In AI, what does LLM commonly mean?',o:['Large Language Model','Linear Logic Machine','Learning Layer Module','Long Learning Memory'],a:0,t:'Generative AI',d:'Easy'},
{q:'Which data structure is commonly used for BFS?',o:['Stack','Queue','Heap','Array only'],a:1,t:'Algorithms',d:'Medium'}
];
let current=0,score=0,answered=false;
function renderQuestion(){const q=questions[current];$('#question-count').textContent=`Question ${current+1} / ${questions.length}`;$('#quiz-question').textContent=q.q;$('#topic-label').textContent=`Topic: ${q.t}`;$('#difficulty-label').textContent=`Difficulty: ${q.d}`;$('#score').textContent=score;$('#next-btn').disabled=true;answered=false;$('#quiz-result').classList.add('hidden');$('#options').innerHTML=q.o.map((x,i)=>`<button data-index="${i}">${x}</button>`).join('');$$('#options button').forEach(btn=>btn.onclick=()=>selectAnswer(Number(btn.dataset.index)))}
function selectAnswer(i){if(answered)return;answered=true;const q=questions[current];const buttons=$$('#options button');buttons.forEach((b,n)=>{b.disabled=true;if(n===q.a)b.classList.add('correct');if(n===i&&i!==q.a)b.classList.add('wrong')});if(i===q.a)score++;$('#score').textContent=score;$('#next-btn').disabled=false}
$('#next-btn')?.addEventListener('click',()=>{if(current<questions.length-1){current++;renderQuestion()}else{const result=$('#quiz-result');result.innerHTML=`<strong>Quiz complete!</strong><p>You scored <b>${score}/${questions.length}</b>. ${score>=8?'Excellent work! 🎉':score>=5?'Good progress. Revise the weak topics and try again.':'Keep practicing. Review the explainers and retry.'}</p>`;result.classList.remove('hidden');$('#next-btn').disabled=true}});
$('#restart-btn')?.addEventListener('click',()=>{current=0;score=0;renderQuestion();document.querySelector('#practice').scrollIntoView({behavior:'smooth'})});
renderQuestion();
